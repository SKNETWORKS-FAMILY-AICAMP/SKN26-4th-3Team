# Tests

Olfit 테스트 문서는 계획과 실행 결과를 분리해서 관리한다.

## 문서 구조

| 문서 | 목적 |
|---|---|
| [Test Plan](./test-plan.md) | Frontend, Backend, 통합, RAG 테스트 범위와 통과 기준 정의 |
| [RAG Test](./rag-test.md) | RAG 파이프라인과 검색 품질 평가 방식 정의 |
| [Test Results](./test-results.md) | 테스트 실행 일자, 명령, 결과, 실패 원인, 후속 조치 기록 |

## 관리 원칙

- 테스트 계획은 기능 범위, 시나리오, 통과 기준을 정의한다.
- 테스트 결과는 실행한 명령과 실제 결과만 기록한다.
- 실패 테스트는 기능 결함, 테스트 기대값 노후화, 환경 문제로 분류한다.
- 비기능 시간 측정은 이번 테스트 범위에서 제외한다.
- RAG 관련 테스트는 `query_text`, `embedding_doc`, vector metadata, 추천 재정렬 입력값을 중심으로 추적한다.
