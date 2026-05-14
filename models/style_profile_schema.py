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


class PromptMessage(TypedDict):
    """Chat Completions API에 전달할 단일 메시지 구조입니다."""

    role: str
    content: str


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


class ProfileInputNormalizer(Protocol):
    """입력 정규화 전략 객체가 따라야 하는 인터페이스입니다."""

    def normalize(self, profile_input: str | VLMStyleInput) -> str:
        """텍스트 또는 VLM 출력을 프롬프트용 설명문으로 변환합니다."""
        ...


class StylePromptBuilderProtocol(Protocol):
    """스타일 분류 프롬프트 빌더가 따라야 하는 인터페이스입니다."""

    def build(self, profile_input: str | VLMStyleInput) -> list[PromptMessage]:
        """스타일 분류에 사용할 Chat 메시지를 생성합니다."""
        ...


class StyleProfileParserProtocol(Protocol):
    """LLM 응답 파서가 따라야 하는 인터페이스입니다."""

    def parse(self, raw_content: str) -> StyleProfile:
        """LLM 원문 응답을 스타일 프로파일로 변환합니다."""
        ...


class ChatCompletionRequesterProtocol(Protocol):
    """Chat Completions 호출 어댑터가 따라야 하는 인터페이스입니다."""

    def request(self, messages: list[PromptMessage]) -> str:
        """LLM에 메시지를 전달하고 assistant content를 반환합니다."""
        ...


__all__ = [
    "ChatCompletionRequesterProtocol",
    "ChatCompletionsClient",
    "FewShotExample",
    "ProfileInputNormalizer",
    "PromptMessage",
    "StyleCategory",
    "StyleProfile",
    "StyleProfileParserProtocol",
    "StylePromptBuilderProtocol",
    "VLMStyleInput",
]


# File History
# 2026-05-14: 스타일 프로파일 분류 스키마를 별도 파일로 분리했습니다. (S4P-55)
# 2026-05-14: 디자인 패턴 기반 분리를 위해 빌더, 파서, 어댑터 프로토콜을 추가했습니다. (S4P-55)
