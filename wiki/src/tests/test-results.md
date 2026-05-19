# Olfit 테스트 결과

## 테스트 결과 총괄

2026-05-19 기준 자동화 테스트는 총 40개가 통과했다.

| 범위 | 도구 | 테스트 수 | 결과 |
|---|---|---:|---|
| Backend | Django TestCase, DRF APIClient, Docker Compose | 20 | PASS |
| Frontend UT | Vitest, Testing Library, jsdom | 16 | PASS |
| Frontend E2E | Playwright Chromium | 4 | PASS |
| 합계 | - | 40 | PASS |

## 실행 환경 요약

| 영역 | 실행 환경 | 실행 명령 |
|---|---|---|
| Backend | Docker Compose `backend` 서비스, 테스트 DB `test_olfit_db` | `docker compose run --rm backend sh -c "cd /backend/app && python manage.py test perfumes --noinput"` |
| Frontend UT | Local Node/Yarn, Vitest, jsdom | `cd frontend && yarn test:run` |
| Frontend E2E | Local Node/Yarn, Playwright Chromium, production build | `cd frontend && yarn test:e2e` |

## 2026-05-16 테스트 현황

| 구분 | 명령 | 결과 | 비고 |
|---|---|---|---|
| Frontend UT | `cd frontend && yarn test:run` | 미실행 | 계획서 이관 및 wiki 정리 단계 |
| Frontend E2E | `cd frontend && yarn test:e2e` | 미실행 | 계획서 이관 및 wiki 정리 단계 |
| Backend Test | `cd backend/app && python manage.py test perfumes` | 미실행 | 계획서 이관 및 wiki 정리 단계 |
| RAG 전용 테스트 | 해당 없음 | 미구성 | 현재 코드에는 RAG 전용 자동화 테스트가 별도 분리되어 있지 않음 |
| RAG 검색 품질 평가 | 해당 없음 | 미실행 | LLM judge와 gold set 기반 Hit@5 평가 기준 문서화 필요 |

## RAG 테스트 점검 결과

현재 RAG 관련 구현 지점은 다음과 같다.

| 영역 | 대상 파일 | 현재 상태 |
|---|---|---|
| RAG query 생성 | `backend/app/perfumes/services/aura_service.py` | `AuraService`가 `query_text`를 생성 |
| RAG embedding document 생성 | `backend/app/perfumes/management/commands/load_perfumes.py` | `embedding_doc`을 `PerfumeDetail.data`에 저장 |
| Vector indexing | `backend/app/perfumes/management/commands/index_to_pinecone.py` | Pinecone 업서트와 metadata 생성 로직 존재 |
| 추천 결과 | `backend/app/perfumes/services/recommendation_service.py` | 현재 테스트는 추천 응답 구조와 note 분리 중심 |

## RAG 테스트 보강 현황

| ID | 테스트 대상 | 검증 내용 | 우선순위 |
|---|---|---|---|
| BE-RAG-001 | `AuraService` | 이미지 분석 결과와 선택 노트로 대칭형 RAG query가 생성되는지 검증 | 완료 |
| BE-RAG-002 | `load_perfumes` | raw perfume data 로드 시 `embedding_doc`이 detail data에 저장되는지 검증 | 완료 |
| BE-RAG-003 | `index_to_pinecone` | Pinecone metadata에 aura 축, notes, 가격, 상품 식별자가 포함되는지 검증 | 완료 |
| BE-RAG-004 | `index_to_pinecone` | `embedding_hash`가 동일할 때 local cache vector를 재사용하는지 검증 | 완료 |
| BE-RAG-005 | `RecommendationService` | vector 후보군을 aura similarity와 preference boost로 재정렬하는지 검증 | 완료 |

## 결과 기록 양식

새 테스트 실행 후 아래 형식으로 누적 기록한다.

| 일자 | 범위 | 명령 | 결과 | 실패 원인 | 후속 조치 |
|---|---|---|---|---|---|
| YYYY-MM-DD | Frontend UT | `cd frontend && yarn test:run` | PASS/FAIL | - | - |

## 2026-05-18 테스트 실행 결과

| 일자 | 범위 | 명령 | 결과 | 실패 원인 | 후속 조치 |
|---|---|---|---|---|---|
| 2026-05-18 | Backend Test | `docker compose run --rm backend sh -c "cd /backend/app && python manage.py test perfumes --noinput"` | PASS | - | `Ran 18 tests ... OK` 확인 |
| 2026-05-18 | Frontend UT | `cd frontend && yarn test:run` | PASS | - | `8 test files, 16 tests passed` 확인 |
| 2026-05-18 | Frontend E2E | `cd frontend && yarn test:e2e` | PASS | - | Playwright Chromium 기준 4개 테스트 통과 |
| 2026-05-19 | Backend Test | `docker compose run --rm backend sh -c "cd /backend/app && python manage.py test perfumes --noinput"` | PASS | - | `Ran 20 tests ... OK` 확인 |

## 2026-05-18 Frontend 테스트 실행 결과

E2E 테스트 코드를 현재 UI와 중복 방지 동작 기준으로 갱신한 뒤, `corepack` 없이 `yarn` 명령으로 재실행해 아래 결과를 확인했다. `yarn playwright install chromium`으로 Playwright Chromium 설치도 확인했다.

| 구분 | 명령 | 결과 | 요약 |
|---|---|---|---|
| Frontend UT | `cd frontend && yarn test:run` | PASS | Vitest 기준 8개 테스트 파일, 16개 테스트 통과 |
| Frontend E2E | `cd frontend && yarn test:e2e` | PASS | Playwright Chromium 기준 4개 테스트 통과 |

### Frontend E2E 검증 상세

| 테스트 | 결과 | 검증 내용 |
|---|---|---|
| `single file selection uploads once and requests analysis once` | PASS | 단일 이미지 업로드 후 `분석 시작` 클릭 시 upload log 1회, `/api/analyze/` 요청 1회 |
| `rapid double drop keeps the current duplicate prevention behavior` | PASS | 빠른 double drop 상황에서 현재 중복 방지 lock 기준 upload log 1회, `/api/analyze/` 요청 1회 |
| `invalid file upload does not request analysis` | PASS | 잘못된 파일 업로드 시 validation message 표시, `/api/analyze/` 미호출 |
| `recommendation card opens product detail modal` | PASS | 추천 상품 카드 클릭 시 상세 모달에 상품명, 브랜드, 노트, 이미지 표시 |

### Frontend UT 검증 상세

2026-05-18에 `cd frontend && yarn test:run`을 재실행해 Vitest 기준 8개 테스트 파일, 16개 테스트가 모두 통과함을 확인했다.

| 테스트 파일 | 테스트 케이스 | 결과 | 검증 내용 |
|---|---|---|---|
| `frontend/src/App.test.tsx` | `continues consent when randomUUID is unavailable in insecure browser contexts` | PASS | 보안 컨텍스트가 아니어서 `crypto.randomUUID`를 사용할 수 없어도 동의 플로우가 유지되고 동의 상태와 session id가 저장됨 |
| `frontend/src/services/uploadService.test.ts` | `returns a simulated remote upload URL after the async delay` | PASS | 이미지 업로드 서비스가 비동기 처리 후 `olfit-assets/user-uploads/aura-*.jpg` 형식의 시뮬레이션 원격 URL을 반환함 |
| `frontend/src/hooks/useInsightReport.test.ts` | `sorts recommendations by backend-provided KRW price instead of display price text` | PASS | 추천 상품 정렬이 화면 표시용 가격 문자열이 아니라 backend 제공 원화 가격 기준으로 동작함 |
| `frontend/src/hooks/useInsightReport.test.ts` | `places missing or invalid KRW prices after priced recommendations` | PASS | 원화 가격이 없거나 잘못된 추천 상품은 정상 가격 상품 뒤로 정렬됨 |
| `frontend/src/metadata/favicon.test.ts` | `registers the Olfit favicon used by browser tabs` | PASS | HTML metadata에 Olfit favicon 경로와 타입이 유지됨 |
| `frontend/src/components/common/ImageUploader.test.tsx` | `describes image preparation without claiming an S3 upload` | PASS | 이미지 업로더 안내 문구가 실제 S3 업로드가 아니라 이미지 준비/분석 흐름으로 표현됨 |
| `frontend/src/components/curated/ProductModal.test.tsx` | `renders fragrance concentration on its own semantic title line` | PASS | 상품 모달에서 향수 농도 표현이 상품명과 분리된 의미 있는 제목 줄로 렌더링됨 |
| `frontend/src/components/curated/ProductModal.test.tsx` | `renders The Story with Korean word-preserving line wrapping` | PASS | `The Story` 영역의 한국어 문장이 단어 단위 줄바꿈을 유지함 |
| `frontend/src/components/report/ProductCarousel.test.tsx` | `resets to the first slide when product order changes` | PASS | 추천 상품 순서가 바뀌면 캐러셀이 첫 번째 슬라이드로 초기화됨 |
| `frontend/src/components/report/ProductCarousel.test.tsx` | `keeps the Best Pick badge attached to the original AI pick` | PASS | 정렬이나 이동 후에도 Best Pick 배지가 최초 AI 추천 상품에 유지됨 |
| `frontend/src/components/report/ProductCarousel.test.tsx` | `enables carousel loop navigation` | PASS | 캐러셀 이전/다음 이동이 끝에서 다시 처음 또는 마지막으로 순환됨 |
| `frontend/src/components/report/ProductCarousel.test.tsx` | `renders product cards with stable full-height sizing` | PASS | 상품 카드가 안정적인 전체 높이 레이아웃으로 렌더링됨 |
| `frontend/src/components/report/ProductCarousel.test.tsx` | `does not render per-product feedback buttons` | PASS | 개별 상품 카드에 feedback 버튼이 렌더링되지 않음 |
| `frontend/src/components/report/ProductCarousel.test.tsx` | `keeps Korean fragrance concentration words from splitting in product names` | PASS | 한국어 향수 농도 단어가 상품명에서 부자연스럽게 분리되지 않음 |
| `frontend/src/components/report/ProductCarousel.test.tsx` | `renders fragrance concentration on its own semantic line` | PASS | 캐러셀 카드의 향수 농도 표현이 별도 의미 줄로 렌더링됨 |
| `frontend/src/components/guide/ScentNoteCarousel.test.tsx` | `returns to the selected note when revisiting a pyramid layer` | PASS | 향 노트 피라미드 레이어를 다시 방문해도 이전 선택 노트가 유지됨 |

## 2026-05-19 Backend 테스트 상세

이번 실행에서 backend 테스트는 Docker Compose 환경 기준으로 통과했다.

| 항목 | 내용 |
|---|---|
| 실행 환경 | Docker Compose `backend` 서비스 |
| 테스트 DB | `test_olfit_db` |
| 실행 테스트 수 | 20 |
| 최종 결과 | OK |
| 주요 검증 범위 | Analyze API, 이미지 추출/동기화, raw perfume 로드, 추천 응답, RAG query/document/metadata 준비 |
| 테스트 파일 구조 | `backend/app/perfumes/tests.py` 단일 파일에서 `backend/app/perfumes/tests/` 패키지로 분리 |

## Backend 테스트 파일 구조 상세

분리 후 Django test runner는 `backend/app/perfumes/tests/` 패키지의 `test_*.py` 파일을 자동 탐색한다. 기존 `backend/app/perfumes/tests.py` 파일은 import 충돌을 피하기 위해 제거했다.

| 테스트 파일 | 테스트 클래스 | 테스트 수 | 담당 범위 |
|---|---|---:|---|
| `backend/app/perfumes/tests/test_analyze_api.py` | `AnalyzeViewTest` | 2 | analyze API 요청/응답과 session id validation |
| `backend/app/perfumes/tests/test_image_extractor.py` | `PerfumeImageExtractorTest` | 6 | raw JSON 이미지 추출, 기존 이미지 skip, 실패 URL 기록, Fragrantica image backfill/parser |
| `backend/app/perfumes/tests/test_load_perfumes.py` | `PerfumeDataModelTest` | 3 | raw perfume 로드, detail/raw data 정규화, 이미지 추출 command의 DB 동기화 |
| `backend/app/perfumes/tests/test_recommendation_service.py` | `RecommendationServiceTest` | 2 | 추천 응답 payload, 이미지/base64, flat notes fallback |
| `backend/app/perfumes/tests/test_rag_preparation.py` | `RagPreparationTest` | 7 | RAG query, embedding document, Pinecone metadata, local cache, 재정렬, gold/experiment scenario query 생성 |

개별 테스트 메서드 기준 상세는 다음과 같다.

| 테스트 파일 | 테스트 메서드 | 검증 내용 |
|---|---|---|
| `test_analyze_api.py` | `test_analyze_success` | session id와 이미지, 선택 노트를 전달하면 analyze API가 200 응답과 추천/metadata를 반환 |
| `test_analyze_api.py` | `test_analyze_missing_session_id` | session id 없이 analyze API 호출 시 400 error 응답 반환 |
| `test_image_extractor.py` | `test_extracts_images_from_raw_json_into_brand_directories` | raw JSON의 image URL을 브랜드 디렉터리 파일로 저장하고 DB sync row를 생성 |
| `test_image_extractor.py` | `test_skips_existing_images_without_downloading_again` | 이미 저장된 이미지가 있으면 downloader를 다시 호출하지 않고 skip 처리 |
| `test_image_extractor.py` | `test_records_failed_image_url_for_database_sync` | 다운로드 실패 URL도 빈 processed path로 DB sync 대상에 기록 |
| `test_image_extractor.py` | `test_backfills_fragrantica_image_urls_from_designer_catalog` | Fragrantica designer catalog HTML에서 상품 image/page URL 추출 |
| `test_image_extractor.py` | `test_backfills_raw_file_image_url_and_product_url` | raw file의 image URL과 product URL을 catalog 기준으로 backfill |
| `test_image_extractor.py` | `test_parses_product_page_json_ld_image` | product page JSON-LD script에서 image URL 파싱 |
| `test_load_perfumes.py` | `test_load_perfumes_populates_normalized_detail_and_raw_data` | raw perfume data를 Perfume/Detail/RawData로 분리 저장하고 detail data를 정규화 |
| `test_load_perfumes.py` | `test_load_perfumes_updates_existing_perfume_raw_data` | 기존 perfume row가 raw file 기준으로 최신 detail/raw data로 갱신 |
| `test_load_perfumes.py` | `test_extract_perfume_images_syncs_downloaded_images_to_database` | `extract_perfume_images` command가 다운로드된 이미지 정보를 `PerfumeImage`에 저장 |
| `test_recommendation_service.py` | `test_recommendations_include_perfume_detail_and_image_payload` | 추천 응답에 perfume detail, notes pyramid, static image URL, base64 payload 포함 |
| `test_recommendation_service.py` | `test_recommendations_split_flat_notes_when_parsed_notes_are_missing` | `notes_parsed`가 없어도 flat notes를 top/middle/base로 나눠 응답 |
| `test_rag_preparation.py` | `test_aura_service_generates_symmetric_query_for_rag` | VLM 결과와 선택 노트로 대칭형 RAG query와 search vector 생성 |
| `test_rag_preparation.py` | `test_load_perfumes_persists_embedding_doc_for_rag` | `load_perfumes`가 RAG용 `embedding_doc`을 `PerfumeDetail.data`에 저장 |
| `test_rag_preparation.py` | `test_index_to_pinecone_metadata_contains_reranking_fields` | Pinecone metadata에 재정렬용 aura 축, 가격, 노트, 상품 식별자 포함 |
| `test_rag_preparation.py` | `test_index_to_pinecone_reuses_local_cache_when_embedding_hash_matches` | `embedding_hash`가 동일하면 OpenAI 호출 없이 local cache vector를 Pinecone upsert에 재사용 |
| `test_rag_preparation.py` | `test_recommendation_service_reranks_semantic_matches_with_aura_and_notes` | semantic 후보군을 aura similarity와 selected note bonus로 재정렬 |
| `test_rag_preparation.py` | `test_gold_scenarios_generate_rag_queries` | 20개 gold scenario의 visual summary와 selected notes가 RAG query에 반영 |
| `test_rag_preparation.py` | `test_experiment_scenarios_generate_rag_queries` | 3개 experiment scenario가 RAG query 생성 경로를 정상 통과 |

추가된 RAG 준비 테스트는 다음과 같다.

| ID | 테스트 대상 | 테스트 메서드 | 검증 내용 |
|---|---|---|---|
| BE-RAG-001 | `AuraService` | `test_aura_service_generates_symmetric_query_for_rag` | VLM 분석 결과와 선택 노트로 대칭형 RAG query와 search vector가 생성되는지 검증 |
| BE-RAG-002 | `load_perfumes` | `test_load_perfumes_persists_embedding_doc_for_rag` | raw perfume data 로드 시 `PerfumeDetail.data.embedding_doc`이 저장되는지 검증 |
| BE-RAG-003 | `index_to_pinecone` | `test_index_to_pinecone_metadata_contains_reranking_fields` | Pinecone metadata에 perfume id, 브랜드, aura 축, 가격, 노트, 설명이 포함되는지 검증 |
| BE-RAG-004 | `index_to_pinecone` | `test_index_to_pinecone_reuses_local_cache_when_embedding_hash_matches` | `embedding_hash`가 동일할 때 OpenAI embedding 재호출 없이 cached vector를 upsert하는지 검증 |
| BE-RAG-005 | `RecommendationService` | `test_recommendation_service_reranks_semantic_matches_with_aura_and_notes` | semantic 점수가 더 낮아도 aura와 selected note가 일치하는 후보를 상위로 재정렬하는지 검증 |
| BE-RAG-006 | `AuraService` | `test_gold_scenarios_generate_rag_queries` | 20개 gold scenario 입력으로 RAG query가 생성되고 각 selected note가 query에 포함되는지 검증 |
| BE-RAG-007 | `AuraService` | `test_experiment_scenarios_generate_rag_queries` | `dual_aura_clash`, `citrus_fresh_boost`, `oriental_night` 실험 scenario 입력으로 RAG query가 생성되는지 검증 |

로컬 Python에서 `python manage.py test perfumes`를 직접 실행할 경우 다음 이슈가 있었다.

| 구분 | 내용 |
|---|---|
| 인코딩 | Windows cp949 콘솔에서 settings 초기화 로그의 이모지 출력으로 `UnicodeEncodeError` 발생 |
| 의존성 | `PYTHONIOENCODING=utf-8` 지정 후에는 로컬 Python 환경에 `corsheaders` 모듈이 없어 `ModuleNotFoundError` 발생 |
| 권장 실행 경로 | 프로젝트 의존성이 갖춰진 Docker Compose backend 서비스에서 테스트 실행 |
