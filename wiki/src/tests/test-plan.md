# Olfit 테스트 기획서

## 1. 목적

Olfit의 프론트엔드와 백엔드에 존재하는 테스트 코드를 기준으로 단위 테스트부터 통합 테스트까지 수행하여, 주요 사용자 시나리오와 API/서비스 동작이 의도한 흐름대로 유지되는지 검증한다.

이번 테스트의 통과 기준은 성능 수치가 아니라 "정의한 시나리오대로 동작했는지"이다. 비기능 테스트 중 응답 시간, 처리 시간, 부하 측정은 이번 범위에서 제외한다.

## 2. 테스트 범위

| 구분 | 대상 | 도구 | 주요 기준 |
|---|---|---|---|
| Frontend UT | 컴포넌트, 훅, 서비스 함수, 메타데이터 | Vitest, Testing Library, jsdom | 화면 상태, 사용자 이벤트, 데이터 변환 결과가 기대값과 일치 |
| Frontend E2E | 이미지 업로드 및 분석 요청 흐름 | Playwright | 실제 브라우저에서 업로드 시나리오가 기대 횟수대로 API를 호출 |
| Backend UT | parser, extractor, recommendation service | Django TestCase, mock | 함수/서비스 결과가 기대 데이터 구조와 일치 |
| Backend 통합 테스트 | analyze API, management command, DB 모델 저장 | Django TestCase, DRF APIClient | API 응답, DB 저장, raw/detail/image 동기화가 시나리오와 일치 |
| Backend RAG 테스트 | query 생성, embedding document, vector metadata | Django TestCase, mock | RAG 검색 입력값과 vector indexing 데이터가 의도한 구조와 일치 |
| Frontend-Backend 통합 | 이미지 업로드 후 분석 API 응답을 화면에 반영하는 흐름 | 수동 시나리오 또는 Docker 실행 환경 | 실제 서비스 실행 상태에서 사용자 흐름이 끊기지 않음 |

## 3. 제외 범위

- 응답 시간 SLA 측정
- 부하 테스트 및 동시 접속 테스트
- 장시간 안정성 테스트
- 실제 외부 이미지 호스팅, S3, 크롤링 사이트의 가용성 검증
- 실사용 VLM 모델의 품질 평가

외부 의존성은 기존 테스트 코드처럼 mock, fixture, 라우트 가로채기 방식으로 대체한다.

## 4. 테스트 환경

| 영역 | 환경 |
|---|---|
| Frontend | Vite, React, Vitest, Testing Library, jsdom, Playwright Chromium |
| Backend | Django, Django REST Framework, Django TestCase, pytest-django 의존성 |
| 실행 기준 | 로컬 개발 환경 또는 Docker Compose 기반 실행 환경 |
| 기준 브랜치 | 테스트 수행 시점의 작업 브랜치 |

## 5. 실행 명령

### Frontend 단위 테스트

```bash
cd frontend
yarn test:run
```

### Frontend E2E 테스트

```bash
cd frontend
yarn test:e2e
```

`test:e2e`는 내부적으로 production build 후 Playwright 테스트를 실행한다.

### Backend 테스트

```bash
cd backend/app
python manage.py test perfumes
```

Docker 환경에서는 다음 명령을 기준으로 한다.

```bash
docker compose run --rm backend sh -c "cd /backend/app && python manage.py test perfumes --noinput"
```

## 6. Frontend 테스트 항목

| ID | 구분 | 테스트 파일 | 검증 시나리오 | 통과 기준 |
|---|---|---|---|---|
| FE-UT-001 | UT | `frontend/src/App.test.tsx` | 보안 컨텍스트에서 `crypto.randomUUID`가 없어도 동의 플로우가 계속된다 | 동의 값과 세션 ID가 localStorage에 저장되고 동의 버튼이 사라진다 |
| FE-UT-004 | UT | `frontend/src/components/common/ImageUploader.test.tsx` | 이미지 업로더가 사용자 파일 선택/드롭 이벤트를 처리한다 | 유효 파일 처리, 미리보기, 콜백 호출이 기대값과 일치한다 |
| FE-UT-005 | UT | `frontend/src/components/curated/ProductModal.test.tsx` | 추천 상품 모달이 상품 상세 정보를 표시한다 | 상품명, 노트, 이미지 등 주요 정보가 렌더링된다 |
| FE-UT-006 | UT | `frontend/src/components/report/ProductCarousel.test.tsx` | 추천 상품 캐러셀이 추천 목록을 표시한다 | 추천 카드와 상호작용 결과가 기대값과 일치한다 |
| FE-UT-007 | UT | `frontend/src/components/guide/ScentNoteCarousel.test.tsx` | 향 노트 선택 UI가 사용자 선택을 반영한다 | 선택 상태와 콜백 호출이 기대값과 일치한다 |
| FE-E2E-001 | E2E | `frontend/e2e/image-upload.spec.ts` | 단일 파일 선택 시 업로드와 분석 요청이 각각 1회 발생한다 | console upload 로그 1회, `/api/analyze/` 요청 1회 |

## 6-1. Frontend 선택/후순위 테스트 항목

아래 항목은 필수 통과 기준에서는 제외하되, 회귀 방지와 품질 안정성을 위해 후순위로 관리한다.

| ID | 구분 | 테스트 대상 | 검증 시나리오 | 통과 기준 | 우선순위 |
|---|---|---|---|---|---|
| FE-OPT-001 | UT | `frontend/src/services/uploadService.test.ts` | 이미지 업로드 서비스가 비동기 처리 후 원격 URL 형식 값을 반환한다 | 반환 URL이 `olfit-assets/user-uploads/aura-*.jpg` 형식과 일치 | P2 |
| FE-OPT-002 | UT | `frontend/src/hooks/useInsightReport.test.ts` | 추천 상품 가격 정렬 로직이 원화 가격 기준으로 동작한다 | 정렬 결과가 기대 순서와 일치 | P2 |
| FE-OPT-003 | UT | `frontend/src/metadata/favicon.test.ts` | favicon 메타데이터가 유지된다 | HTML 메타데이터와 favicon 파일이 기대값과 일치 | P3 |
| FE-OPT-004 | E2E | `frontend/e2e/image-upload.spec.ts` | 빠른 double drop 시 현재 중복 방지 동작을 검증한다 | 현재 기준 upload 로그 1회, `/api/analyze/` 요청 1회와 일치 | P4 |
| FE-OPT-005 | UT | `useStore` | 저장된 동의 값과 session id가 있으면 재방문 시 동의 상태를 복원한다 | `hasConsented`가 `true`로 초기화된다 | P2 |
| FE-OPT-006 | UT | `ErrorBoundary` | 섹션 렌더링 중 예외가 발생해도 앱 전체가 중단되지 않는다 | fallback message 표시, 나머지 UI 유지 | P2 |
| FE-OPT-007 | E2E | `frontend/e2e/image-upload.spec.ts` | 잘못된 파일 업로드 시 분석 요청이 발생하지 않는다 | validation message 표시, `/api/analyze/` 미호출 | P2 |
| FE-OPT-008 | E2E | `frontend/e2e/image-upload.spec.ts` | 분석 결과의 추천 상품을 클릭하면 상세 모달이 열린다 | 상품명, 브랜드, 노트, 이미지 표시 | P2 |

## 7. Backend 테스트 항목

| ID | 구분 | 테스트 클래스/파일 | 검증 시나리오 | 통과 기준 |
|---|---|---|---|---|
| BE-API-001 | 통합 | `AnalyzeViewTest` | 세션 ID와 이미지, 선택 노트를 전달하면 분석 API가 추천 결과를 반환한다 | HTTP 200, `recommendations`, `analysisMetadata.radarScores` 포함 |
| BE-API-002 | 통합 | `AnalyzeViewTest` | 세션 ID 없이 분석 API를 호출한다 | HTTP 400, `error` 포함 |
| BE-UT-001 | UT | `PerfumeImageExtractorTest` | raw JSON의 이미지 URL을 브랜드별 이미지 디렉터리에 저장한다 | 생성 건수 1, 이미지 파일 생성, DB row mapping 일치 |
| BE-UT-002 | UT | `PerfumeImageExtractorTest` | 이미 저장된 이미지는 다시 다운로드하지 않는다 | created 0, skipped 1, downloader 미호출 |
| BE-UT-003 | UT | `PerfumeImageExtractorTest` | 이미지 다운로드 실패 URL도 DB 동기화 대상으로 기록한다 | failed 1, processed path 빈 값으로 mapping 생성 |
| BE-UT-004 | UT | `PerfumeImageExtractorTest` | Fragrantica designer catalog에서 상품 이미지 URL을 추출한다 | perfume name 기준 image/page URL mapping 일치 |
| BE-UT-005 | UT | `PerfumeImageExtractorTest` | raw file의 image URL과 product URL을 backfill한다 | raw JSON의 `image_url`, `product_url`이 갱신된다 |
| BE-UT-006 | UT | `PerfumeImageExtractorTest` | product page JSON-LD에서 image URL을 파싱한다 | JSON-LD image 값이 반환된다 |
| BE-INT-001 | 통합 | `PerfumeDataModelTest` | `load_perfumes`가 raw 데이터를 정규화해 detail/raw table에 저장한다 | perfume/detail/raw_data 필드 분리와 aura profile 저장이 기대값과 일치 |
| BE-INT-002 | 통합 | `PerfumeDataModelTest` | 기존 향수 데이터가 raw file 기준으로 갱신된다 | perfume 기본 정보, detail, raw_data가 최신 값으로 갱신 |
| BE-INT-003 | 통합 | `PerfumeDataModelTest` | `extract_perfume_images` command가 이미지 파일을 DB에 동기화한다 | `PerfumeImage` 생성, base64 저장, detail data에 image asset 미포함 |
| BE-SVC-001 | UT | `RecommendationServiceTest` | 추천 결과에 향수 상세 정보와 이미지 payload가 포함된다 | perfume/detail/image URL/base64 필드가 기대값과 일치 |
| BE-SVC-002 | UT | `RecommendationServiceTest` | parsed notes가 없으면 flat notes를 top/middle/base로 나눈다 | top/middle/base note 문자열이 기대값과 일치 |

## 8. RAG 테스트 항목

검색 품질 평가의 상세 기준은 [RAG Test](./rag-test.md)를 따른다.

| ID | 구분 | 대상 | 검증 시나리오 | 통과 기준 |
|---|---|---|---|---|
| BE-RAG-001 | UT | `AuraService` | VLM 분석 결과와 선택 노트로 RAG query text를 생성한다 | query가 이미지 요약, 분위기, 통합 노트, 주요 계열을 포함한다 |
| BE-RAG-002 | 통합 | `load_perfumes` | raw perfume data를 로드하면서 RAG용 `embedding_doc`을 생성한다 | `PerfumeDetail.data.embedding_doc`에 브랜드, 상품명, 설명, accord, note, 계열이 포함된다 |
| BE-RAG-003 | UT | `index_to_pinecone._build_metadata` | vector DB 검색과 재정렬에 필요한 metadata를 구성한다 | perfume id, brand, aura 축, notes, price, description 필드가 포함된다 |
| BE-RAG-004 | 통합 | `index_to_pinecone` | 동일한 `embedding_doc`은 hash 기반 local cache를 재사용한다 | OpenAI embedding 재호출 없이 기존 vector가 upsert 대상이 된다 |
| BE-RAG-005 | 통합 | `RecommendationService` | 향후 vector 후보군을 기존 aura similarity와 preference boost로 재정렬한다 | semantic 후보군의 순위가 aura/profile/selected notes 기준으로 보정된다 |
| BE-RAG-006 | UT | `AuraService` | 20개 gold scenario 입력으로 RAG query를 생성한다 | visual summary와 selected notes가 query에 포함된다 |
| BE-RAG-007 | UT | `AuraService` | 3개 experiment scenario 입력으로 RAG query를 생성한다 | scenario별 query 생성 경로가 정상 통과한다 |

## 9. Frontend-Backend 통합 시나리오

| ID | 시나리오 | 절차 | 통과 기준 |
|---|---|---|---|
| INT-001 | 최초 접속 및 동의 | 앱 접속 후 개인정보/분석 동의 버튼을 클릭한다 | 동의 상태가 저장되고 이미지 업로드 단계로 이동한다 |
| INT-002 | 향 노트 선택 | 사용자가 선호 향 노트를 선택한다 | 선택한 노트가 UI 상태와 분석 요청 데이터에 반영된다 |
| INT-003 | 이미지 업로드 및 분석 요청 | 사용자가 이미지를 업로드한다 | backend `/api/analyze/`로 이미지와 selected notes가 전달된다 |
| INT-004 | 분석 결과 표시 | backend가 추천 결과와 radar score를 반환한다 | frontend가 분석 결과, 추천 상품, 향수 상세 정보를 화면에 표시한다 |
| INT-005 | 추천 상품 상세 확인 | 사용자가 추천 상품을 선택한다 | 상품 모달 또는 상세 영역에 이름, 브랜드, 노트, 이미지가 표시된다 |
| INT-006 | 오류 응답 처리 | 세션 ID 누락 또는 API 오류 상황을 재현한다 | 사용자에게 오류 상태가 표시되고 앱이 중단되지 않는다 |

## 10. 통과 기준

테스트는 다음 조건을 모두 만족하면 통과로 판단한다.

- 자동화된 Frontend 단위 테스트가 실패 없이 종료된다.
- 자동화된 Frontend E2E 테스트가 현재 정의된 기대값과 일치한다.
- Backend 테스트가 실패 없이 종료된다.
- 통합 시나리오에서 사용자 흐름이 중단되지 않는다.
- API 요청/응답 필드가 frontend adapter와 backend contract 사이에서 불일치하지 않는다.
- RAG 검색 입력값인 `query_text`, `embedding_doc`, vector metadata가 문서화된 구조와 일치한다.
- 테스트 실패가 발생한 경우 원인이 기능 결함인지, 테스트 기대값 노후화인지 분류되어 기록된다.

## 11. 결함 처리 기준

| 우선순위 | 기준 | 예시 |
|---|---|---|
| P1 | 핵심 사용자 흐름이 진행되지 않음 | 이미지 업로드 불가, 분석 API 500, 결과 화면 미표시 |
| P2 | 주요 데이터가 누락되거나 잘못 표시됨 | 추천 상품명/노트/이미지 누락, radar score 누락 |
| P3 | 특정 예외 상황에서만 실패함 | 일부 브라우저 API 미지원, 세션 누락 처리 오류 |
| P4 | 문서화된 현재 동작 또는 개선 예정 항목 | rapid double drop 중복 방지처럼 현재 동작을 회귀 방지 목적으로 고정하는 항목 |

## 12. 산출물

- 자동화 테스트 실행 결과
- 실패 테스트 목록과 원인 분석
- 통합 시나리오 체크 결과
- 결함 목록 및 우선순위
- 회귀 테스트가 필요한 변경 사항 목록

## 13. 참고 테스트 파일

- `backend/app/perfumes/tests/test_analyze_api.py`
- `backend/app/perfumes/tests/test_image_extractor.py`
- `backend/app/perfumes/tests/test_load_perfumes.py`
- `backend/app/perfumes/tests/test_recommendation_service.py`
- `backend/app/perfumes/tests/test_rag_preparation.py`
- `backend/app/perfumes/services/aura_service.py`
- `backend/app/perfumes/management/commands/load_perfumes.py`
- `backend/app/perfumes/management/commands/index_to_pinecone.py`
- `frontend/src/App.test.tsx`
- `frontend/e2e/image-upload.spec.ts`
