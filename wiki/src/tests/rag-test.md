# RAG 테스트 계획

## 1. 목적

RAG 테스트는 단순히 화면에 결과가 표시되는지 확인하는 테스트와 검색 품질을 평가하는 테스트를 분리해서 관리한다.

이미지 업로드 후 추천 결과가 나온다면 파이프라인은 동작한 것이다. 하지만 그 결과가 사용자의 query 의도와 얼마나 잘 맞는지는 별도의 검색 정확도 테스트로 판단해야 한다.

## 2. 테스트 관점

| 구분 | 목적 | 판단 기준 |
|---|---|---|
| 파이프라인 테스트 | 이미지 분석, query 생성, 검색, 추천 응답까지 끊기지 않는지 확인 | 시나리오가 정상 완료되는지 |
| 검색 품질 테스트 | 생성된 query와 검색된 document가 의미적으로 잘 맞는지 확인 | 평가 점수, hit rate, top-k 포함 여부 |

## 3. 파이프라인 테스트

파이프라인 테스트는 RAG가 기술적으로 연결되어 있는지 확인한다.

| ID | 시나리오 | 입력 | 통과 기준 |
|---|---|---|---|
| RAG-PIPE-001 | 이미지 업로드 후 RAG query 생성 | 사용자 이미지, 선택 노트 | `query_text`가 생성된다 |
| RAG-PIPE-002 | query 기반 검색 요청 | `query_text` | vector search 또는 fallback 검색이 호출된다 |
| RAG-PIPE-003 | 검색 결과 재정렬 | 검색 후보군, aura vector, selected notes | 최종 추천 top 5가 생성된다 |
| RAG-PIPE-004 | 프론트 응답 표시 | backend recommendation response | 추천 카드와 상세 정보가 화면에 표시된다 |

파이프라인 테스트의 통과 기준은 “사진대로 결과 화면이 나오는지”에 가깝다. 즉, 검색 품질보다는 전체 흐름이 끊기지 않는지를 확인한다.

## 4. 검색 품질 테스트

검색 품질 테스트는 query와 검색된 document의 관련성을 평가한다. 파이프라인이 정상 동작하더라도 검색 결과가 부정확하면 RAG 품질은 낮은 것으로 본다.

검색 품질은 두 가지 방식으로 평가한다.

| 평가 방식 | 설명 | 장점 | 한계 |
|---|---|---|---|
| LLM 평가 | query와 검색된 document를 평가자 LLM에 제공하고 기준표로 점수를 매긴다 | 정성적 관련성 판단 가능 | 평가 기준과 프롬프트 품질에 영향받음 |
| 정답셋 기반 hit rate | 특정 query에 대해 반드시 top 5 안에 들어야 하는 향수를 정답으로 지정하고 포함률을 측정한다 | 수치화와 회귀 비교가 쉬움 | 정답셋 구축 비용이 있음 |

## 5. LLM 평가 방식

### 입력

평가자 LLM에는 다음 데이터를 그대로 전달한다.

| 항목 | 설명 |
|---|---|
| query | `AuraService`가 생성한 RAG 검색 문장 |
| retrieved documents | vector DB 또는 검색 엔진이 반환한 후보 document |
| perfume metadata | 브랜드, 상품명, notes, accords, family, description |
| user context | 이미지 요약, 선택 노트, aura score |

### 평가 기준

| 기준 | 점수 | 설명 |
|---|---:|---|
| Query Intent Match | 0-5 | 검색 결과가 query의 분위기, 노트, 계열 의도와 맞는지 |
| Note Relevance | 0-5 | 선택 노트 또는 분석 노트와 향수 노트가 관련 있는지 |
| Aura Match | 0-5 | query의 주요 계열과 향수의 aura profile이 맞는지 |
| Description Consistency | 0-5 | 향수 설명이 query의 감성 표현과 충돌하지 않는지 |
| Diversity | 0-5 | top-k 결과가 지나치게 같은 브랜드/계열로만 쏠리지 않는지 |

### 통과 기준

| 항목 | 기준 |
|---|---|
| 평균 점수 | 3.5 / 5 이상 |
| Top 5 중 관련 결과 | 3개 이상 |
| 명백한 오답 | Top 5 안에 1개 이하 |

### 평가 프롬프트 초안

```text
너는 향수 추천 RAG 검색 결과를 평가하는 심사자다.

아래 query는 사용자의 이미지 분석 결과와 선택 노트를 바탕으로 생성된 검색 문장이다.
retrieved documents는 RAG 검색으로 반환된 향수 후보들이다.

평가 기준:
1. Query Intent Match: query의 분위기, 노트, 계열 의도와 검색 결과가 맞는가?
2. Note Relevance: 선택/분석 노트와 향수 노트가 관련 있는가?
3. Aura Match: query의 주요 계열과 향수 aura profile이 맞는가?
4. Description Consistency: 향수 설명이 query의 감성 표현과 충돌하지 않는가?
5. Diversity: top-k 결과가 지나치게 한쪽으로 쏠리지 않는가?

각 기준을 0-5점으로 평가하고, 최종적으로 PASS 또는 FAIL을 판단해라.
명백한 오답이 있으면 이유를 짧게 적어라.
```

## 6. 정답셋 기반 Hit Rate 평가

정답셋 기반 평가는 “이런 query를 날리면 이 향수는 반드시 top 5 안에 들어야 한다”는 기준 데이터를 만든 뒤 hit rate를 계산한다.

### 정답셋 예시 형식

| ID | Query 조건 | 반드시 포함되어야 하는 향수 | 기준 |
|---|---|---|---|
| GOLD-001 | 시트러스, 밝은 이미지, 프레시 계열 | BVLGARI Aqva Amara | top 5 포함 |
| GOLD-002 | 장미, 우아한 분위기, 플로럴 계열 | Jo Malone Red Roses | top 5 포함 |
| GOLD-003 | 바닐라, 포근함, 구르망 계열 | Lush Vanillary | top 5 포함 |
| GOLD-004 | 우디, 차분함, 샌달우드 선호 | Le Labo Santal 계열 | top 5 포함 |

실제 정답셋은 DB에 존재하는 향수명 기준으로 확정해야 한다.

### 지표

| 지표 | 계산 방식 | 의미 |
|---|---|---|
| Hit@5 | 정답 향수가 top 5 안에 포함된 query 수 / 전체 query 수 | 핵심 추천 성공률 |
| Hit@3 | 정답 향수가 top 3 안에 포함된 query 수 / 전체 query 수 | 상위 노출 품질 |
| MRR | 1 / 정답 향수 순위의 평균 | 정답이 얼마나 위에 나오는지 |
| No-hit Count | 정답 향수가 top-k에 없는 query 수 | 실패 케이스 수 |

### 통과 기준

| 지표 | 기준 |
|---|---|
| Hit@5 | 80% 이상 |
| Hit@3 | 60% 이상 |
| MRR | 0.5 이상 |
| No-hit Count | 핵심 query set에서 0건 목표 |

## 7. 테스트 데이터 관리

RAG 품질 테스트를 위해 별도 gold set을 관리한다.

권장 파일:

```text
backend/app/perfumes/tests/fixtures/rag_gold_set.json
```

문서만 관리하는 단계에서는 아래 형식을 기준으로 준비한다.

```json
[
  {
    "id": "GOLD-001",
    "query": "밝고 산뜻한 시트러스 분위기의 오렌지, 베르가못 향이 느껴지는 프레시 계열 향수.",
    "expected_top5": ["Aqva Amara"],
    "required_notes": ["오렌지", "베르가못"],
    "required_family": "프레시"
  }
]
```

## 8. 결과 기록 양식

| 일자 | 평가 방식 | Query 수 | Hit@5 | Hit@3 | 평균 LLM 점수 | 결과 | 비고 |
|---|---|---:|---:|---:|---:|---|---|
| YYYY-MM-DD | Gold Set | 20 | 0.00 | 0.00 | - | 미실행 | 최초 기준선 작성 전 |
| YYYY-MM-DD | LLM Judge | 20 | - | - | 0.0 | 미실행 | 평가 프롬프트 확정 전 |

## 9. 결론

RAG 테스트는 다음 순서로 진행한다.

1. 파이프라인이 끝까지 동작하는지 확인한다.
2. query와 retrieved document를 저장한다.
3. LLM 평가로 의미적 관련성을 점수화한다.
4. 유명 향수 또는 대표 향수 기반 gold set으로 Hit@5를 측정한다.
5. 결과를 `test-results.md`에 누적 기록한다.
