"""LLM JSON mode 스타일 프로파일 서비스.

이 파일은 스타일 분류 프롬프트와 스키마를 사용해 향수, 상품, VLM 키워드
입력을 구조화된 스타일 프로파일로 분류합니다.
"""

from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError

from models.style_profile_prompt import (
    FEW_SHOT_EXAMPLES,
    STYLE_CATEGORIES,
    build_style_prompt,
    normalize_profile_input,
)
from models.style_profile_schema import (
    ChatCompletionsClient,
    FewShotExample,
    StyleCategory,
    StyleProfile,
    VLMStyleInput,
)


def _extract_message_content(response: Any) -> str:
    """OpenAI SDK 객체 또는 테스트용 dict 응답에서 assistant content를 추출합니다."""
    if isinstance(response, dict):
        return response["choices"][0]["message"]["content"]
    return response.choices[0].message.content


def _parse_and_validate(raw_content: str) -> StyleProfile:
    """LLM 원문 JSON 응답을 파싱하고 Pydantic 스키마로 검증합니다."""
    parsed = json.loads(raw_content)
    return StyleProfile.model_validate(parsed)


class KeywordStructureService:
    """LLM 기반 스타일 프로파일 분류 서비스입니다."""

    def __init__(
        self,
        client: ChatCompletionsClient,
        model: str = "gpt-4o-mini",
        max_retries: int = 3,
    ) -> None:
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")
        self.client = client
        self.model = model
        self.max_retries = max_retries

    def classify(self, profile_input: str | VLMStyleInput) -> StyleProfile:
        """텍스트 또는 VLM 구조화 출력을 `{style, mood, color}`로 분류합니다."""
        messages = build_style_prompt(profile_input)
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            raw_content = _extract_message_content(response)
            try:
                return _parse_and_validate(raw_content)
            except (json.JSONDecodeError, TypeError, ValidationError) as exc:
                last_error = exc
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

        raise ValueError(f"Failed to parse and validate style profile after {self.max_retries} attempts") from last_error

    def generate(self, profile_input: str | VLMStyleInput) -> StyleProfile:
        """기존 호출부 호환을 위한 `classify` 별칭입니다."""
        return self.classify(profile_input)


def classify_style_profile(
    profile_input: str | VLMStyleInput,
    client: ChatCompletionsClient,
    model: str = "gpt-4o-mini",
    max_retries: int = 3,
) -> StyleProfile:
    """입력을 최대 3회 검증 재시도로 `{style, mood, color}` 형태로 분류합니다."""
    return KeywordStructureService(client=client, model=model, max_retries=max_retries).classify(profile_input)


__all__ = [
    "FEW_SHOT_EXAMPLES",
    "STYLE_CATEGORIES",
    "ChatCompletionsClient",
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
# 2026-05-14: 스타일 프로파일 서비스에서 스키마와 프롬프트 생성 로직을 분리했습니다. (S4P-55)
