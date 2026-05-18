# 데이터 정규화 및 전처리 파이프라인 (Data Ingestion Pipeline)

외부 소스에서 수집된 향수 데이터를 시스템 표준 스키마로 변환하고 아우라 프로필을 생성하여 데이터베이스 및 검색 엔진에 적재하는 오프라인 공정을 정의합니다.

## 1. 데이터 파이프라인 흐름

![data_ingestion_pipeline](../../assets/backend/pipeline/data_ingestion_pipeline.png)

1. **Raw Data Ingestion**: JSON 형태의 브랜드별 원본 데이터 수집
2. **Schema Standardizing**: 브랜드마다 다른 필드명을 표준 필드(Name, Brand, Notes 등)로 매핑
3. **Aura Profiling**: 텍스트 분석(NLP)을 통해 해당 향수의 5대 계열 점수를 자동 할당 및 대칭형 RAG 문서 생성
4. **Validation**: 필수 필드 누락 및 이미지 URL 유효성 검증
5. **DB Upsert**: `Perfume`, `PerfumeDetail`, `PerfumeRawData` 테이블에 적재
6. **Vector Indexing**: 가공된 데이터를 Pinecone 벡터 데이터베이스에 동기화 (`index_to_pinecone`)

## 2. 핵심 전처리 로직 (Core Preprocessing)

### 2.1 휴리스틱 노트 피라미드 분류 (Heuristic Note Splitting)
수집된 향수 데이터 중 Top/Middle/Base 구분이 없는 경우, `utils.py`의 `split_notes_heuristic` 함수를 통해 자동으로 분류합니다.

- **분류 방식**:
  - **Top**: 시트러스, 그린, 허벌 계열 지표(`TOP_INDICATORS`) 포함 시 할당.
  - **Base**: 우디, 머스크, 오리엔탈 계열 지표(`BASE_INDICATORS`) 포함 시 할당.
  - **Middle**: 위 두 범주에 속하지 않는 성분(주로 플로럴, 스파이시)을 할당.
- **보정 로직**: 특정 층에만 데이터가 쏠리지 않도록 최소 1개 이상의 성분이 각 층에 배분되도록 자동 재배치 로직이 포함되어 있습니다.

### 2.2 아우라 프로필 및 점수 산출 (Aura Profiling)
`load_perfumes` 커맨드 실행 시, 향수 도메인 지식 맵(`master_fragrance_map.json`)을 기반으로 5축 점수를 산출합니다.

- **가중치 정책**:
  - **Main Accords**: 향수의 전체 인상을 결정하는 어코드 매칭 시 **+2.0점**.
  - **Individual Notes**: 세부 뉘앙스를 보강하는 개별 성분 매칭 시 **+1.0점**.
- **정규화**: 산출된 원천 점수 벡터는 코사인 유사도 연산을 위해 **L2 정규화(L2 Norm)** 과정을 거쳐 크기가 1인 벡터로 변환됩니다.

### 2.3 대칭형 RAG 임베딩 문서 생성 (Symmetric Embedding)
검색 성능 극대화를 위해 사용자의 검색 쿼리 구조와 대칭을 이루는 자연어 문서를 생성하여 `embedding_doc` 필드에 저장합니다.
- **구조**: `[브랜드] [상품명]. [설명]. [어코드] 분위기의 [성분] 향이 느껴지는 [계열] 향수. [상위2개축] 분위기가 느껴지는 제품입니다. #[키워드]`

## 3. 이미지 및 통화 처리
- **환율 환산**: `convert_to_krw` 함수를 통해 다양한 외화 가격(USD, EUR, GBP)을 2026년 5월 기준 고정 환율로 원화로 변환하여 저장합니다.
- **이미지 관리**: 원본 URL을 보존하면서 `PerfumeImage` 테이블을 통해 로컬 처리 경로와 Base64 데이터를 관리합니다.
