"""스타일 프로파일 분류 스키마.

이 파일은 LLM 스타일 분류 입력과 출력에 사용하는 타입, Pydantic 모델,
클라이언트 프로토콜을 정의합니다.
"""

from __future__ import annotations

from typing import Any, Literal, Protocol, TypedDict

from pydantic import BaseModel, ConfigDict, Field, field_validator

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
    """VLM 이미지 키워드 출력을 스타일 분류 입력으로 받기 위한 구조입니다."""

    visual_summary: str
    colors: list[str]
    objects: list[str]
    scene: list[str]
    mood: list[str]
    season: list[str]
    time: list[str]
    raw_keywords: list[str]


class FewShotExample(TypedDict):
    """스타일 카테고리별 few-shot 예시 구조입니다."""

    input: str
    output: str


class StyleProfile(BaseModel):
    """LLM 스타일 분류 결과를 검증하는 엄격한 출력 스키마입니다."""

    model_config = ConfigDict(extra="forbid")

    style: StyleCategory = Field(description="사전에 정의된 7개 스타일 카테고리 중 하나입니다.")
    mood: str = Field(min_length=1, max_length=60, description="짧은 분위기 표현입니다.")
    color: str = Field(min_length=1, max_length=40, description="대표 색상 표현입니다.")

    @field_validator("mood", "color")
    @classmethod
    def normalize_short_text(cls, value: str) -> str:
        """LLM이 반환한 짧은 텍스트 필드의 공백을 정리합니다."""
        normalized_value = " ".join(value.strip().split())
        if not normalized_value:
            raise ValueError("value must not be empty")
        return normalized_value


class ChatCompletionsClient(Protocol):
    """OpenAI 호환 Chat Completions 클라이언트 프로토콜입니다."""

    chat: Any


__all__ = [
    "ChatCompletionsClient",
    "FewShotExample",
    "StyleCategory",
    "StyleProfile",
    "VLMStyleInput",
]


# File History
# 2026-05-14: 스타일 프로파일 분류 스키마를 별도 파일로 분리했습니다. (S4P-55)
