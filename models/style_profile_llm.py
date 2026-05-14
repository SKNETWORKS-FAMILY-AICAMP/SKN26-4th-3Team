"""LLM JSON mode style profile service.

This model-layer file classifies fragrance, product, or VLM keyword input
into a structured style profile for downstream recommendation logic.
"""

from __future__ import annotations

import json
from typing import Any, Final, Literal, Protocol, TypedDict

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

# Restrict LLM style output to the seven supported style categories.
StyleCategory = Literal[
    "fresh_clean",
    "floral_romantic",
    "woody_earthy",
    "amber_warm",
    "spicy_oriental",
    "gourmand_sweet",
    "aquatic_marine",
]


class VLMStyleInput(TypedDict, total=False):
    """Structured VLM keyword payload accepted by the style profiler."""

    # Korean sentence summarizing the overall visual atmosphere.
    visual_summary: str
    # Fashion-item colors extracted from the image.
    colors: list[str]
    # Object or material keywords detected in the image.
    objects: list[str]
    # Scene or location keywords for the image context.
    scene: list[str]
    # Mood keywords describing the image impression.
    mood: list[str]
    # Seasonal keyword when the image has a clear seasonal signal.
    season: list[str]
    # Time-of-day keyword when the image has a clear time signal.
    time: list[str]
    # Auxiliary raw keywords produced by the VLM.
    raw_keywords: list[str]


class FewShotExample(TypedDict):
    """Few-shot prompt example for one style category."""

    # Example input shown to the LLM.
    input: str
    # JSON output shape the LLM should follow.
    output: str


# Category descriptions injected into the prompt to prevent arbitrary style values.
STYLE_CATEGORIES: Final[dict[str, str]] = {
    "fresh_clean": "산뜻함, 깨끗함, 시트러스/화이트 머스크 계열",
    "floral_romantic": "플로럴, 부드러움, 로맨틱 계열",
    "woody_earthy": "우디, 흙내음, 차분한 자연감",
    "amber_warm": "앰버, 바닐라, 따뜻하고 관능적인 계열",
    "spicy_oriental": "스파이시, 오리엔탈, 이국적이고 강렬한 계열",
    "gourmand_sweet": "달콤함, 디저트/캔디/크리미 계열",
    "aquatic_marine": "물, 바다, 투명하고 시원한 계열",
}

# Only these VLM fields are allowed to enter the style-classification prompt.
# Unknown keys are rejected to avoid prompt pollution from unexpected payloads.
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

# Seven few-shot examples, one for each supported style category.
# Each example demonstrates the required {style, mood, color} JSON schema.
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


class StyleProfile(BaseModel):
    """Strict output schema for LLM classification."""

    # Reject extra keys so the model cannot add unplanned response fields.
    model_config = ConfigDict(extra="forbid")

    # Literal validation blocks style values outside the seven categories.
    style: StyleCategory = Field(description="One of the seven predefined style categories.")
    # Keep mood as a short phrase for downstream display and ranking use.
    mood: str = Field(min_length=1, max_length=60, description="Short mood phrase.")
    # Keep color as a compact representative color phrase.
    color: str = Field(min_length=1, max_length=40, description="Representative color phrase.")

    @field_validator("mood", "color")
    @classmethod
    def normalize_short_text(cls, value: str) -> str:
        # Trim surrounding whitespace and collapse repeated spaces from LLM output.
        normalized_value = " ".join(value.strip().split())
        if not normalized_value:
            raise ValueError("value must not be empty")
        return normalized_value


class ChatCompletionsClient(Protocol):
    """Protocol for OpenAI-compatible `client.chat.completions.create`."""

    # Allows both the real OpenAI SDK client and fake test clients to be injected.
    chat: Any


def _json_dumps(data: VLMStyleInput) -> str:
    # Keep Korean keywords unescaped and compact the JSON for prompt readability.
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def normalize_profile_input(profile_input: str | VLMStyleInput) -> str:
    """Normalize raw text or structured VLM output into prompt input text."""
    # Raw text input only needs whitespace normalization before classification.
    if isinstance(profile_input, str):
        description = " ".join(profile_input.strip().split())
        if not description:
            raise ValueError("description must not be empty")
        return description

    if not isinstance(profile_input, dict):
        # Reject unsupported input types before an LLM call is attempted.
        raise TypeError("profile_input must be a string description or VLM output dict")

    # Accept only known VLM fields. Add new fields to ALLOWED_VLM_KEYS first.
    unknown_keys = set(profile_input) - set(ALLOWED_VLM_KEYS)
    if unknown_keys:
        raise ValueError(f"VLM output contains unsupported keys: {sorted(unknown_keys)}")

    # Convert VLM fields into a readable one-line prompt input.
    parts: list[str] = []
    visual_summary = profile_input.get("visual_summary")
    if visual_summary:
        # Put the overall visual summary first because it carries the broad context.
        parts.append(f"visual_summary: {visual_summary}")

    for key in ALLOWED_VLM_KEYS[1:]:
        value = profile_input.get(key)
        if not value:
            # Skip empty fields to reduce prompt noise.
            continue
        if isinstance(value, list):
            # Join keyword lists into a readable comma-separated phrase.
            parts.append(f"{key}: {', '.join(str(item) for item in value)}")
        else:
            # Preserve single string values in the same key-value format.
            parts.append(f"{key}: {value}")

    description = " | ".join(parts).strip()
    if not description:
        # A dict without usable values cannot produce a meaningful classification.
        raise ValueError("VLM output must contain at least one non-empty field")
    return description


def build_style_prompt(profile_input: str | VLMStyleInput) -> list[dict[str, str]]:
    """Build few-shot prompt messages for JSON mode classification."""
    description = normalize_profile_input(profile_input)
    # The system message defines allowed styles and JSON-only constraints.
    # The user message supplies the few-shot examples plus the current input.
    categories = "\n".join(f"- {key}: {desc}" for key, desc in STYLE_CATEGORIES.items())
    shots = "\n".join(
        # Repeating Input/Output pairs makes the target JSON shape explicit.
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


def _extract_message_content(response: Any) -> str:
    """Extract assistant content from OpenAI SDK object or dict response."""
    if isinstance(response, dict):
        # Fake clients in tests return dict responses.
        return response["choices"][0]["message"]["content"]
    # Real OpenAI SDK responses expose content through the object path.
    return response.choices[0].message.content


def _parse_and_validate(raw_content: str) -> StyleProfile:
    """Parse raw JSON content and validate it with Pydantic."""
    # JSON mode can still return schema-invalid JSON, so validate with Pydantic.
    parsed = json.loads(raw_content)
    return StyleProfile.model_validate(parsed)


class KeywordStructureService:
    """LLM-backed keyword structure service for style profile classification."""

    def __init__(
        self,
        client: ChatCompletionsClient,
        model: str = "gpt-4o-mini",
        max_retries: int = 3,
    ) -> None:
        if max_retries < 1:
            # At least one attempt is required for a meaningful classification call.
            raise ValueError("max_retries must be at least 1")
        # Injecting client and model keeps the service testable and environment-agnostic.
        self.client = client
        self.model = model
        self.max_retries = max_retries

    def classify(self, profile_input: str | VLMStyleInput) -> StyleProfile:
        """Classify text or structured VLM output into `{style, mood, color}`."""
        messages = build_style_prompt(profile_input)
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            # OpenAI-compatible Chat Completions JSON mode call site.
            # The injected client may be a real OpenAI client or a fake test client.
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            raw_content = _extract_message_content(response)
            try:
                # Valid JSON and valid schema return immediately.
                return _parse_and_validate(raw_content)
            except (json.JSONDecodeError, TypeError, ValidationError) as exc:
                # Retry only parse/schema failures. Network/API exceptions bubble up.
                last_error = exc
                # Keep the failed response in context so the next attempt can correct it.
                messages.append({"role": "assistant", "content": raw_content})
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Previous output failed JSON parsing or Pydantic schema validation. "
                            "Retry with only a JSON object containing exactly style, mood, color. "
                            "Use one of the seven allowed style values. "
                            f"Attempt {attempt + 1} of {self.max_retries}."
                        ),
                    }
                )

        # Preserve the final parse/validation exception as the failure cause.
        raise ValueError(f"Failed to parse and validate style profile after {self.max_retries} attempts") from last_error

    def generate(self, profile_input: str | VLMStyleInput) -> StyleProfile:
        """Backward-compatible alias for `classify`."""
        return self.classify(profile_input)


def classify_style_profile(
    profile_input: str | VLMStyleInput,
    client: ChatCompletionsClient,
    model: str = "gpt-4o-mini",
    max_retries: int = 3,
) -> StyleProfile:
    """Classify input into `{style, mood, color}` with up to 3 validation retries."""
    # Provide a function-style wrapper for callers that do not need a service instance.
    return KeywordStructureService(client=client, model=model, max_retries=max_retries).classify(profile_input)


__all__ = [
    "FEW_SHOT_EXAMPLES",
    "STYLE_CATEGORIES",
    "FewShotExample",
    "KeywordStructureService",
    "StyleCategory",
    "StyleProfile",
    "VLMStyleInput",
    "build_style_prompt",
    "classify_style_profile",
    "normalize_profile_input",
]

# File History
# 2026-05-14: Created LLM JSON mode style profile service. (S4P-55)
