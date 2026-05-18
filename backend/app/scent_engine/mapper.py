"""
@file scent_engine/mapper.py
@role
VLM에서 추출된 시각적 키워드(색상, 사물, 무드 등)를 향수 도메인의 전문적인 속성(5축 스코어, 향료 성분, 분위기 묘사 등)으로 매핑하고 점수를 산출하는 모듈입니다.
분석된 데이터를 정규화된 키워드와 정량적 수치로 변환하여 상위 엔진(AuraService 등)이 추천 로직 및 쿼리 생성을 수행할 수 있도록 기초 데이터를 제공합니다.
"""

# ----------------------------------------------------------------
# Update History
# 2026-05-14: 그루망 계열 점수 계산 로직 복구 (worker: Gloveman)
# ----------------------------------------------------------------

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .aliases import normalize_note_keyword, to_korean_note
from .rules import VISUAL_TO_FRAGRANCE_RULES, KOREAN_VISUAL_TRIGGERS

# -----------------------------------------------------
# 그루망(Gourmand) 트리거 정의
# -----------------------------------------------------
GOURMAND_TRIGGERS = {
    "components": ["Vanilla", "Berry, Apple, Peach", "Tropical Fruit"],
    "subs": ["Fruity", "Soft Amber"],
    "descriptors": ["달콤한", "포근한", "감미로운"],
}


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


def _calculate_gourmand_score(
    component_scores: defaultdict[str, float],
    sub_scores: defaultdict[str, float],
    descriptor_scores: defaultdict[str, float],
) -> float:
    gourmand_score = 0.0

    # 1. Components (원료 가중치 x 1.0)
    for comp in GOURMAND_TRIGGERS["components"]:
        norm_comp = normalize_note_keyword(comp)
        if norm_comp and norm_comp in component_scores:
            gourmand_score += component_scores[norm_comp] * 1.0

    # 2. Subs (서브 계열 가중치 x 0.7)
    for sub in GOURMAND_TRIGGERS["subs"]:
        if sub in sub_scores:
            gourmand_score += sub_scores[sub] * 0.7

    # 3. Descriptors (분위기 묘사 가중치 x 0.5)
    for desc in GOURMAND_TRIGGERS["descriptors"]:
        if desc in descriptor_scores:
            gourmand_score += descriptor_scores[desc] * 0.5

    return gourmand_score


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
    """
    VLM에서 추출된 시각적 키워드 딕셔너리를 향수 도메인의 키워드 및 점수로 변환합니다.

    이 함수는 다음과 같은 과정을 거칩니다:
    1. 시각 키워드(색상, 사물, 장면 등) 수집 및 정규화.
    2. VISUAL_TO_FRAGRANCE_RULES에 따라 향수 계열(Family), 서브(Sub), 성분(Component), 묘사(Descriptor) 점수 계산.
    3. 중복 매칭에 따른 가중치(Multiplier) 적용.
    4. 이미지 전체 문맥(패션, 시간대, 어두움 등)에 따른 추가 보정 작업 수행.
    5. 최종 하위 속성 데이터를 기반으로 구르망(Gourmand) 점수 산출 및 병합.
    6. 각 카테고리별 상위 N개의 결과를 추출하여 최종 딕셔너리 구성.

    Args:
        image_keywords (dict[str, Any]): VLM 분석 결과물.
            필수 키: 'colors', 'objects', 'scene', 'mood', 'season', 'time', 'raw_keywords' 등.

    Returns:
        dict[str, Any]: 향수 매칭 결과물.
            - matched_triggers: 매칭된 원본 시각 트리거 목록
            - scores: 각 카테고리별 상세 점수 (name, score 쌍)
            - fragrance_families: 상위 향수 계열 명칭 목록
            - fragrance_subs: 상위 서브 계열 명칭 목록
            - components: 상위 성분 영문 명칭 목록
            - components_ko: 상위 성분 한국어 명칭 목록
            - descriptors: 상위 묘사 키워드 목록
    """
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

    # 1. 기존 문맥 보정 적용
    _apply_context_adjustments(
        source_keywords=source_keywords,
        matched_triggers=matched_triggers,
        family_scores=family_scores,
        sub_scores=sub_scores,
        component_scores=component_scores,
        descriptor_scores=descriptor_scores,
    )

    # 2. 보정이 끝난 최종 하위 데이터를 바탕으로 그루망(Gourmand) 스코어 계산 및 병합
    gourmand_score = _calculate_gourmand_score(
        component_scores=component_scores,
        sub_scores=sub_scores,
        descriptor_scores=descriptor_scores,
    )
    if gourmand_score > 0:
        family_scores["GOURMAND"] += gourmand_score

    component_ko_scores = _build_component_ko_scores(component_scores)

    # 3. 최종 정렬
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
        "raw_keywords": [
            "체크무늬",
            "드레스",
            "여성",
            "실내",
            "포즈",
            "손가방",
            "목걸이",
        ],
    }

    result = map_image_to_fragrance_keywords(sample)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# EOF: scent_engine/mapper.py
