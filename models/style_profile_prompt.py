"""스타일 프로파일 few-shot 프롬프트 생성기.

이 파일은 Strategy와 Builder 패턴을 사용해 VLM 또는 텍스트 입력을
정규화하고, LLM JSON mode 분류에 사용할 few-shot 메시지를 생성합니다.
"""

from __future__ import annotations

from typing import Final

from models.style_profile_schema import FewShotExample, PromptMessage, VLMStyleInput

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


class StyleProfileInputNormalizer:
    """Strategy 패턴으로 스타일 프로파일 입력 정규화 책임을 담당합니다."""

    def __init__(self, allowed_vlm_keys: tuple[str, ...] = ALLOWED_VLM_KEYS) -> None:
        self.allowed_vlm_keys = allowed_vlm_keys

    def normalize(self, profile_input: str | VLMStyleInput) -> str:
        """텍스트 또는 VLM 구조화 출력을 분류 프롬프트 입력문으로 정규화합니다."""
        if isinstance(profile_input, str):
            return self._normalize_text(profile_input)

        if isinstance(profile_input, dict):
            return self._normalize_vlm_output(profile_input)

        raise TypeError("profile_input must be a string description or VLM output dict")

    def _normalize_text(self, profile_input: str) -> str:
        """일반 텍스트 입력의 공백을 정리합니다."""
        description = " ".join(profile_input.strip().split())
        if not description:
            raise ValueError("description must not be empty")
        return description

    def _normalize_vlm_output(self, profile_input: VLMStyleInput) -> str:
        """VLM 구조화 출력을 키 순서가 고정된 설명문으로 변환합니다."""
        unknown_keys = set(profile_input) - set(self.allowed_vlm_keys)
        if unknown_keys:
            raise ValueError(f"VLM output contains unsupported keys: {sorted(unknown_keys)}")

        parts: list[str] = []
        visual_summary = profile_input.get("visual_summary")
        if visual_summary:
            parts.append(f"visual_summary: {visual_summary}")

        for key in self.allowed_vlm_keys[1:]:
            value = profile_input.get(key)
            if not value:
                continue
            parts.append(self._format_vlm_field(key, value))

        description = " | ".join(parts).strip()
        if not description:
            raise ValueError("VLM output must contain at least one non-empty field")
        return description

    def _format_vlm_field(self, key: str, value: object) -> str:
        """VLM 필드 값을 프롬프트에 넣기 좋은 문자열로 변환합니다."""
        if isinstance(value, list):
            return f"{key}: {', '.join(str(item) for item in value)}"
        return f"{key}: {value}"


class StylePromptBuilder:
    """Builder 패턴으로 스타일 분류용 Chat 메시지를 조립합니다."""

    def __init__(
        self,
        categories: dict[str, str] | None = None,
        examples: list[FewShotExample] | None = None,
        normalizer: StyleProfileInputNormalizer | None = None,
    ) -> None:
        self.categories = STYLE_CATEGORIES if categories is None else categories
        self.examples = FEW_SHOT_EXAMPLES if examples is None else examples
        self.normalizer = normalizer or StyleProfileInputNormalizer()

    def build(self, profile_input: str | VLMStyleInput) -> list[PromptMessage]:
        """JSON mode 스타일 분류에 사용할 few-shot 메시지를 생성합니다."""
        description = self.normalizer.normalize(profile_input)
        return [
            self._build_system_message(),
            self._build_user_message(description),
        ]

    def _build_system_message(self) -> PromptMessage:
        """허용 스타일과 출력 제약을 담은 system 메시지를 생성합니다."""
        categories = "\n".join(f"- {key}: {desc}" for key, desc in self.categories.items())
        return {
            "role": "system",
            "content": (
                "You classify fragrance/product/image style descriptions. "
                "Return only a valid JSON object with exactly these keys: style, mood, color. "
                "Do not include markdown, comments, arrays, or extra keys.\n\n"
                f"Allowed style values:\n{categories}"
            ),
        }

    def _build_user_message(self, description: str) -> PromptMessage:
        """few-shot 예시와 실제 입력을 담은 user 메시지를 생성합니다."""
        shots = "\n".join(
            f"Input: {example['input']}\nOutput: {example['output']}"
            for example in self.examples
        )
        return {
            "role": "user",
            "content": (
                "Few-shot examples for the seven style categories:\n"
                f"{shots}\n\n"
                "Now classify this input. Return JSON only.\n"
                f"Input: {description}"
            ),
        }


def normalize_profile_input(profile_input: str | VLMStyleInput) -> str:
    """기존 호출부 호환을 위해 기본 Strategy 객체로 입력을 정규화합니다."""
    return StyleProfileInputNormalizer().normalize(profile_input)


def build_style_prompt(profile_input: str | VLMStyleInput) -> list[PromptMessage]:
    """기존 호출부 호환을 위해 기본 Builder 객체로 프롬프트를 생성합니다."""
    return StylePromptBuilder().build(profile_input)


__all__ = [
    "ALLOWED_VLM_KEYS",
    "FEW_SHOT_EXAMPLES",
    "STYLE_CATEGORIES",
    "StyleProfileInputNormalizer",
    "StylePromptBuilder",
    "build_style_prompt",
    "normalize_profile_input",
]


# File History
# 2026-05-14: 스타일 프로파일 프롬프트 생성 로직을 별도 파일로 분리했습니다. (S4P-55)
# 2026-05-14: 입력 정규화 Strategy와 프롬프트 Builder 클래스로 책임을 분리했습니다. (S4P-55)
