"""스타일 프로파일 few-shot 프롬프트 생성기.

이 파일은 VLM 또는 텍스트 입력을 정규화하고, LLM JSON mode 분류에
사용할 스타일 카테고리와 few-shot 메시지를 생성합니다.
"""

from __future__ import annotations

import json
from typing import Final

from models.style_profile_schema import FewShotExample, VLMStyleInput

STYLE_CATEGORIES: Final[dict[str, str]] = {
    "fresh_clean": "산뜻함, 깨끗함, 시트러스/화이트 머스크 계열",
    "floral_romantic": "플로럴, 부드러움, 로맨틱 계열",
    "woody_earthy": "우디, 흙내음, 차분한 자연감",
    "amber_warm": "앰버, 바닐라, 따뜻하고 관능적인 계열",
    "spicy_oriental": "스파이시, 오리엔탈, 이국적이고 강렬한 계열",
    "gourmand_sweet": "달콤함, 디저트/캔디/크리미 계열",
    "aquatic_marine": "물, 바다, 투명하고 시원한 계열",
}

ALLOWED_VLM_KEYS: Final[tuple[str, ...]] = (
    "visual_summary",
    "colors",
    "objects",
    "scene",
    "mood",
    "season",
    "time",
    "raw_keywords",
)

FEW_SHOT_EXAMPLES: Final[list[FewShotExample]] = [
    {
        "input": "Sparkling bergamot, clean white musk, crisp cotton, and a transparent citrus trail.",
        "output": '{"style":"fresh_clean","mood":"crisp and polished","color":"clear white"}',
    },
    {
        "input": "A bouquet of rose and jasmine with soft powdery petals and a romantic aura.",
        "output": '{"style":"floral_romantic","mood":"soft romantic","color":"blush pink"}',
    },
    {
        "input": "Dry cedarwood, earthy patchouli, vetiver, and a grounded forest-like depth.",
        "output": '{"style":"woody_earthy","mood":"calm grounded","color":"deep brown"}',
    },
    {
        "input": "Warm amber, vanilla, benzoin, and labdanum create a sensual evening glow.",
        "output": '{"style":"amber_warm","mood":"sensual warm","color":"golden amber"}',
    },
    {
        "input": "Saffron, cinnamon, oud wood, and pepper form an exotic intense signature.",
        "output": '{"style":"spicy_oriental","mood":"bold mysterious","color":"dark burgundy"}',
    },
    {
        "input": "Tutti-frutti candy, creamy musk, pear, and a playful edible sweetness.",
        "output": '{"style":"gourmand_sweet","mood":"playful sweet","color":"candy peach"}',
    },
    {
        "input": "Marine breeze, watery freshness, salt air, and a transparent blue trail.",
        "output": '{"style":"aquatic_marine","mood":"cool airy","color":"aqua blue"}',
    },
]


def _json_dumps(data: VLMStyleInput) -> str:
    """한글 키워드를 유지한 채 VLM 입력을 프롬프트용 JSON 문자열로 변환합니다."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def normalize_profile_input(profile_input: str | VLMStyleInput) -> str:
    """텍스트 또는 VLM 구조화 출력을 분류 프롬프트 입력문으로 정규화합니다."""
    if isinstance(profile_input, str):
        description = " ".join(profile_input.strip().split())
        if not description:
            raise ValueError("description must not be empty")
        return description

    if not isinstance(profile_input, dict):
        raise TypeError("profile_input must be a string description or VLM output dict")

    unknown_keys = set(profile_input) - set(ALLOWED_VLM_KEYS)
    if unknown_keys:
        raise ValueError(f"VLM output contains unsupported keys: {sorted(unknown_keys)}")

    parts: list[str] = []
    visual_summary = profile_input.get("visual_summary")
    if visual_summary:
        parts.append(f"visual_summary: {visual_summary}")

    for key in ALLOWED_VLM_KEYS[1:]:
        value = profile_input.get(key)
        if not value:
            continue
        if isinstance(value, list):
            parts.append(f"{key}: {', '.join(str(item) for item in value)}")
        else:
            parts.append(f"{key}: {value}")

    description = " | ".join(parts).strip()
    if not description:
        raise ValueError("VLM output must contain at least one non-empty field")
    return description


def build_style_prompt(profile_input: str | VLMStyleInput) -> list[dict[str, str]]:
    """JSON mode 스타일 분류에 사용할 few-shot 메시지를 생성합니다."""
    description = normalize_profile_input(profile_input)
    categories = "\n".join(f"- {key}: {desc}" for key, desc in STYLE_CATEGORIES.items())
    shots = "\n".join(
        f"Input: {example['input']}\nOutput: {example['output']}"
        for example in FEW_SHOT_EXAMPLES
    )
    return [
        {
            "role": "system",
            "content": (
                "You classify fragrance/product/image style descriptions. "
                "Return only a valid JSON object with exactly these keys: style, mood, color. "
                "Do not include markdown, comments, arrays, or extra keys.\n\n"
                f"Allowed style values:\n{categories}"
            ),
        },
        {
            "role": "user",
            "content": (
                "Few-shot examples for the seven style categories:\n"
                f"{shots}\n\n"
                "Now classify this input. Return JSON only.\n"
                f"Input: {description}"
            ),
        },
    ]


__all__ = [
    "ALLOWED_VLM_KEYS",
    "FEW_SHOT_EXAMPLES",
    "STYLE_CATEGORIES",
    "build_style_prompt",
    "normalize_profile_input",
]


# File History
# 2026-05-14: 스타일 프로파일 프롬프트 생성 로직을 별도 파일로 분리했습니다. (S4P-55)
