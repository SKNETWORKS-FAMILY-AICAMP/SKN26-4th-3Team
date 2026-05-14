"""LLM JSON mode 스타일 프로파일 서비스.

이 파일은 Facade, Adapter, Parser 역할 클래스를 조합해 향수, 상품,
VLM 키워드 입력을 구조화된 스타일 프로파일로 분류합니다.
"""

from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError

from models.style_profile_prompt import (
    FEW_SHOT_EXAMPLES,
    STYLE_CATEGORIES,
    StyleProfileInputNormalizer,
    StylePromptBuilder,
    build_style_prompt,
    normalize_profile_input,
)
from models.style_profile_schema import (
    ChatCompletionRequesterProtocol,
    ChatCompletionsClient,
    FewShotExample,
    PromptMessage,
    StyleCategory,
    StyleProfile,
    StyleProfileParserProtocol,
    StylePromptBuilderProtocol,
    VLMStyleInput,
)


class ChatCompletionRequester:
    """Adapter 패턴으로 OpenAI 호환 클라이언트 호출 방식을 캡슐화합니다."""

    def __init__(self, client: ChatCompletionsClient, model: str = "gpt-4o-mini") -> None:
        self.client = client
        self.model = model

    def request(self, messages: list[PromptMessage]) -> str:
        """LLM에 메시지를 전달하고 assistant content만 반환합니다."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        return self.extract_message_content(response)

    @staticmethod
    def extract_message_content(response: Any) -> str:
        """OpenAI SDK 객체 또는 테스트용 dict 응답에서 assistant content를 추출합니다."""
        if isinstance(response, dict):
            return response["choices"][0]["message"]["content"]
        return response.choices[0].message.content


class StyleProfileResponseParser:
    """Parser 역할로 LLM JSON 응답 파싱과 스키마 검증을 담당합니다."""

    def parse(self, raw_content: str) -> StyleProfile:
        """LLM 원문 JSON 응답을 파싱하고 Pydantic 스키마로 검증합니다."""
        parsed = json.loads(raw_content)
        return StyleProfile.model_validate(parsed)


class RetryPromptComposer:
    """LLM 재시도 시 이전 실패와 교정 지시를 메시지에 누적합니다."""

    def append_retry_instruction(
        self,
        messages: list[PromptMessage],
        raw_content: str,
        attempt: int,
        max_retries: int,
    ) -> None:
        """파싱 실패 응답과 다음 시도 지시를 Chat 메시지 목록에 추가합니다."""
        messages.append({"role": "assistant", "content": raw_content})
        messages.append(
            {
                "role": "user",
                "content": (
                    "Previous output failed JSON parsing or Pydantic schema validation. "
                    "Retry with only a JSON object containing exactly style, mood, color. "
                    "Use one of the seven allowed style values. "
                    f"Attempt {attempt + 1} of {max_retries}."
                ),
            }
        )


class KeywordStructureService:
    """Facade 패턴으로 프롬프트 생성, LLM 호출, 응답 파싱 흐름을 조율합니다."""

    def __init__(
        self,
        client: ChatCompletionsClient,
        model: str = "gpt-4o-mini",
        max_retries: int = 3,
        prompt_builder: StylePromptBuilderProtocol | None = None,
        requester: ChatCompletionRequesterProtocol | None = None,
        parser: StyleProfileParserProtocol | None = None,
        retry_prompt_composer: RetryPromptComposer | None = None,
    ) -> None:
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")
        self.client = client
        self.model = model
        self.max_retries = max_retries
        self.prompt_builder = prompt_builder or StylePromptBuilder()
        self.requester = requester or ChatCompletionRequester(client=client, model=model)
        self.parser = parser or StyleProfileResponseParser()
        self.retry_prompt_composer = retry_prompt_composer or RetryPromptComposer()

    def classify(self, profile_input: str | VLMStyleInput) -> StyleProfile:
        """텍스트 또는 VLM 구조화 출력을 `{style, mood, color}`로 분류합니다."""
        messages = self.prompt_builder.build(profile_input)
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            raw_content = self.requester.request(messages)
            try:
                return self.parser.parse(raw_content)
            except (json.JSONDecodeError, TypeError, ValidationError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    self.retry_prompt_composer.append_retry_instruction(
                        messages=messages,
                        raw_content=raw_content,
                        attempt=attempt,
                        max_retries=self.max_retries,
                    )

        raise ValueError(f"Failed to parse and validate style profile after {self.max_retries} attempts") from last_error

    def generate(self, profile_input: str | VLMStyleInput) -> StyleProfile:
        """기존 호출부 호환을 위한 `classify` 별칭입니다."""
        return self.classify(profile_input)


def _extract_message_content(response: Any) -> str:
    """기존 테스트 호환을 위해 Adapter의 assistant content 추출 규칙을 사용합니다."""
    return ChatCompletionRequester.extract_message_content(response)


def _parse_and_validate(raw_content: str) -> StyleProfile:
    """기존 테스트 호환을 위해 기본 Parser 객체로 JSON 응답을 검증합니다."""
    return StyleProfileResponseParser().parse(raw_content)


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
    "ChatCompletionRequester",
    "ChatCompletionsClient",
    "FewShotExample",
    "KeywordStructureService",
    "PromptMessage",
    "RetryPromptComposer",
    "StyleCategory",
    "StyleProfile",
    "StyleProfileInputNormalizer",
    "StyleProfileResponseParser",
    "StylePromptBuilder",
    "VLMStyleInput",
    "build_style_prompt",
    "classify_style_profile",
    "normalize_profile_input",
]


# File History
# 2026-05-14: 스타일 프로파일 서비스에서 스키마와 프롬프트 생성 로직을 분리했습니다. (S4P-55)
# 2026-05-14: Facade, Adapter, Parser 클래스로 LLM 분류 책임을 세분화했습니다. (S4P-55)
