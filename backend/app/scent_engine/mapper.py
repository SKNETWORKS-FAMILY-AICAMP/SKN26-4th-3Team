"""
image_to_fragrance_mapper.py
----------------------------
이미지 시각 키워드를 향수 도메인 키워드로 변환한다.

역할:
1. 이미지 키워드 colors / objects / scene / mood / raw_keywords를 수집
2. 시각 키워드를 향수 family / sub / component / descriptor로 점수화
3. 패션/봄/오후/여성적 이미지에서는 Fresh/Floral 쪽을 보정
4. black 단독으로 Leather/Oud/Incense가 과하게 올라가지 않도록 보정
5. 최종 query_text를 생성해 RAG 검색 질의로 사용

중요:
- query_text는 RAG 검색용이며 prefix를 붙인다.
  예: visual_color:green / fragrance_sub:Green
- readable_query_text는 사람이 보기 좋은 디버깅용이다.
- query_sections는 나중에 가중치 조정/로그 분석용으로 사용한다.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .aliases import normalize_note_keyword, to_korean_note
from .rules import VISUAL_TO_FRAGRANCE_RULES, KOREAN_VISUAL_TRIGGERS


def _collect_source_keywords(image_keywords: dict[str, Any]) -> list[str]:
    source: list[str] = []

    for key in ["colors", "objects", "scene", "mood", "season", "time", "raw_keywords"]:
        values = image_keywords.get(key, [])

        if isinstance(values, list):
            source.extend([str(v).strip().lower() for v in values if str(v).strip()])
        elif isinstance(values, str) and values.strip():
            source.append(values.strip().lower())

    summary = str(image_keywords.get("visual_summary", "")).strip().lower()
    if summary:
        source.append(summary)

    return source


def _detect_triggers(source_keywords: list[str]) -> list[str]:
    joined = " ".join(source_keywords).lower()
    detected: list[str] = []

    for trigger in VISUAL_TO_FRAGRANCE_RULES:
        if trigger in joined:
            detected.append(trigger)

    for ko_trigger, en_trigger in KOREAN_VISUAL_TRIGGERS.items():
        if ko_trigger in joined:
            detected.append(en_trigger)

    return detected


def _add_scores(
    target: defaultdict[str, float],
    score_map: dict[str, float],
    multiplier: float = 1.0,
    normalize_component: bool = False,
) -> None:
    for key, score in score_map.items():
        normalized_key = normalize_note_keyword(key) if normalize_component else key
        if not normalized_key:
            continue
        target[normalized_key] += score * multiplier


def _subtract_score(
    target: defaultdict[str, float],
    key: str,
    amount: float,
    normalize_component: bool = False,
) -> None:
    normalized_key = normalize_note_keyword(key) if normalize_component else key
    if not normalized_key:
        return
    target[normalized_key] = max(0.0, target.get(normalized_key, 0.0) - amount)


def _build_component_ko_scores(component_scores: dict[str, float]) -> dict[str, float]:
    result: dict[str, float] = {}

    for component, score in component_scores.items():
        kor = to_korean_note(component)
        result[kor] = result.get(kor, 0.0) + score

    return result


def _rank_scores(
    score_dict: dict[str, float],
    top_n: int | None = None,
) -> list[dict[str, float | str]]:
    ranked = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

    if top_n:
        ranked = ranked[:top_n]

    return [
        {
            "name": name,
            "score": round(score, 3),
        }
        for name, score in ranked
        if score > 0
    ]


def _names_only(ranked_items: list[dict[str, float | str]]) -> list[str]:
    return [str(item["name"]) for item in ranked_items]


def _has_any(source_keywords: list[str], candidates: list[str]) -> bool:
    joined = " ".join(source_keywords).lower()
    return any(candidate.lower() in joined for candidate in candidates)


def _apply_context_adjustments(
    source_keywords: list[str],
    matched_triggers: list[str],
    family_scores: defaultdict[str, float],
    sub_scores: defaultdict[str, float],
    component_scores: defaultdict[str, float],
    descriptor_scores: defaultdict[str, float],
) -> None:
    """
    단순 trigger 매핑 이후, 이미지 전체 문맥에 따라 점수를 보정한다.

    핵심:
    - black 단독은 무거운 향으로 과도하게 해석하지 않는다.
    - black + dark/night/bar/leather 조합이면 그때 Dry Woods / Leather / Incense를 강화한다.
    - fashion/feminine/elegant/spring/afternoon 문맥이면 Fresh/Floral을 강화하고 무거운 노트를 낮춘다.
    """

    fashion_context = _has_any(
        source_keywords,
        [
            "fashion",
            "style",
            "feminine",
            "elegant",
            "contemporary",
            "dress",
            "handbag",
            "necklace",
            "spring",
            "afternoon",
            "modern",
            "패션",
            "여성",
            "우아",
            "드레스",
            "봄",
            "오후",
        ],
    )

    dark_context = _has_any(
        source_keywords,
        [
            "dark",
            "night",
            "bar",
            "leather",
            "black leather",
            "smoke",
            "candle",
            "어두",
            "밤",
            "가죽",
            "술집",
            "스모키",
        ],
    )

    if "black" in matched_triggers and not dark_context:
        _subtract_score(component_scores, "Leather", 0.6, normalize_component=True)
        _subtract_score(component_scores, "Incense", 0.5, normalize_component=True)
        _subtract_score(component_scores, "Oud", 0.5, normalize_component=True)
        _subtract_score(sub_scores, "Dry Woods", 0.5)
        _subtract_score(descriptor_scores, "스모키한", 0.5)
        _subtract_score(descriptor_scores, "묵직한", 0.4)

        descriptor_scores["세련된"] += 0.8
        descriptor_scores["차분한"] += 0.4
        component_scores[normalize_note_keyword("Musk")] += 0.5

    if "black" in matched_triggers and dark_context:
        family_scores["WOODY"] += 0.8
        family_scores["AMBERY"] += 0.6
        sub_scores["Dry Woods"] += 0.9
        component_scores[normalize_note_keyword("Leather")] += 1.0
        component_scores[normalize_note_keyword("Incense")] += 0.8
        component_scores[normalize_note_keyword("Oud")] += 0.8
        descriptor_scores["스모키한"] += 0.9
        descriptor_scores["묵직한"] += 0.8
        descriptor_scores["깊은"] += 0.8

    if fashion_context:
        family_scores["FRESH"] += 1.2
        family_scores["FLORAL"] += 1.3

        sub_scores["Soft Floral"] += 1.0
        sub_scores["Floral"] += 0.8
        sub_scores["Green"] += 0.7
        sub_scores["Citrus"] += 0.5

        component_scores[normalize_note_keyword("Musk")] += 1.0
        component_scores[normalize_note_keyword("Iris")] += 0.9
        component_scores[normalize_note_keyword("Peony")] += 0.9
        component_scores[normalize_note_keyword("Absolute Rose")] += 0.8
        component_scores[normalize_note_keyword("Bergamot")] += 0.7
        component_scores[normalize_note_keyword("Green Note")] += 0.6

        descriptor_scores["우아한"] += 1.2
        descriptor_scores["세련된"] += 1.1
        descriptor_scores["부드러운"] += 0.9
        descriptor_scores["밝은"] += 0.8
        descriptor_scores["상쾌한"] += 0.7

        if not dark_context:
            _subtract_score(component_scores, "Leather", 0.5, normalize_component=True)
            _subtract_score(component_scores, "Incense", 0.5, normalize_component=True)
            _subtract_score(component_scores, "Oud", 0.5, normalize_component=True)
            _subtract_score(sub_scores, "Dry Woods", 0.5)
            _subtract_score(descriptor_scores, "스모키한", 0.5)
            _subtract_score(descriptor_scores, "묵직한", 0.4)


def map_image_to_fragrance_keywords(image_keywords: dict[str, Any]) -> dict[str, Any]:
    source_keywords = _collect_source_keywords(image_keywords)
    matched_triggers = _detect_triggers(source_keywords)

    family_scores: defaultdict[str, float] = defaultdict(float)
    sub_scores: defaultdict[str, float] = defaultdict(float)
    component_scores: defaultdict[str, float] = defaultdict(float)
    descriptor_scores: defaultdict[str, float] = defaultdict(float)

    trigger_counter = Counter(matched_triggers)

    for trigger, count in trigger_counter.items():
        mapping = VISUAL_TO_FRAGRANCE_RULES.get(trigger)
        if not mapping:
            continue

        multiplier = min(1.0 + (count - 1) * 0.25, 1.5)

        _add_scores(family_scores, mapping.get("families", {}), multiplier)
        _add_scores(sub_scores, mapping.get("subs", {}), multiplier)
        _add_scores(
            component_scores,
            mapping.get("components", {}),
            multiplier,
            normalize_component=True,
        )
        _add_scores(descriptor_scores, mapping.get("descriptors", {}), multiplier)

    _apply_context_adjustments(
        source_keywords=source_keywords,
        matched_triggers=matched_triggers,
        family_scores=family_scores,
        sub_scores=sub_scores,
        component_scores=component_scores,
        descriptor_scores=descriptor_scores,
    )

    component_ko_scores = _build_component_ko_scores(component_scores)

    ranked_families = _rank_scores(family_scores, top_n=3)
    ranked_subs = _rank_scores(sub_scores, top_n=6)
    ranked_components = _rank_scores(component_scores, top_n=10)
    ranked_components_ko = _rank_scores(component_ko_scores, top_n=10)
    ranked_descriptors = _rank_scores(descriptor_scores, top_n=10)

    result: dict[str, Any] = {
        "matched_triggers": list(dict.fromkeys(matched_triggers)),

        "scores": {
            "families": ranked_families,
            "subs": ranked_subs,
            "components": ranked_components,
            "components_ko": ranked_components_ko,
            "descriptors": ranked_descriptors,
        },

        "fragrance_families": _names_only(ranked_families),
        "fragrance_subs": _names_only(ranked_subs),
        "components": _names_only(ranked_components),
        "components_ko": _names_only(ranked_components_ko),
        "descriptors": _names_only(ranked_descriptors),
    }

    return result


if __name__ == "__main__":
    import json

    sample = {
        "visual_summary": "청록색과 검은색 체크무늬 드레스를 입은 여성이 실내에서 포즈를 취하고 있습니다.",
        "colors": ["black", "green", "blue", "pink", "red"],
        "objects": ["handbag", "dress", "necklace"],
        "scene": ["indoor"],
        "mood": ["soft", "romantic"],
        "season": ["spring"],
        "time": ["afternoon"],
        "raw_keywords": ["체크무늬", "드레스", "여성", "실내", "포즈", "손가방", "목걸이"],
    }

    result = map_image_to_fragrance_keywords(sample)
    print(json.dumps(result, ensure_ascii=False, indent=2))
