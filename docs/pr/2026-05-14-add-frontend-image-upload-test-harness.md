# PR 제목

# [S4P-13] Test: 프론트 테스트 환경 및 누적 작업 반영

---

# PR 본문

## 🔗 Jira 연동
Refs S4P-13
Refs S4P-22
Refs S4P-23
Refs S4P-24
Refs S4P-25
Refs S4P-30
Refs S4P-31
Refs S4P-56
Refs S4P-61
Refs S3P-149
Refs S3P-150
Refs S3P-151

---

## 📌 요약
이번 PR은 `upstream/dev` 이후 `origin/main`에 누적된 Olfit 마이그레이션, Docker/DB 구성, 추천 API 개선, Swagger 문서화, 프론트 이미지 업로드 테스트 환경 구축 작업을 반영합니다.
- Django REST backend와 Vite React frontend를 monorepo 구조로 정리했습니다.
- MySQL, backend, frontend Docker 실행 구성을 보강했습니다.
- 추천 응답에 perfume/detail/image 데이터를 포함하고, 향 피라미드 note 분리 처리를 반영했습니다.
- DRF Swagger API Docs에 분석 엔드포인트 스키마를 추가했습니다.
- 이미지 업로드 중복 이벤트 검증 결과를 wiki로 분리하고, Vitest/Playwright 테스트 환경을 추가했습니다.

---

## ✅ 작업 내용
| Jira 이슈 | 작업 내용 |
|---|---|
| S3P-149 | Olfit monorepo 마이그레이션, backend/frontend/wiki 문서 구조 정리 |
| S3P-150 | Docker Compose, MySQL, backend startup/migration 흐름 정리 |
| S3P-151 | wiki backend SUMMARY 링크 및 mdBook 구조 보정 |
| S4P-56 | perfume image URL backfill, image asset 저장, detail/raw data 정규화 |
| S4P-31 | 추천 응답의 scent pyramid top/middle/base note 분리 및 frontend normalization 보강 |
| S4P-61 | DRF Swagger API Docs에 analyze endpoint request/response schema 추가 |
| S4P-22 | ImageUploader 중복 이벤트 진단 결과 wiki 반영 |
| S4P-23 | 이미지 업로드 테스트 결과 문서 분리 |
| S4P-24 | 이미지 업로드 troubleshooting 문서 정리 |
| S4P-25 | frontend wiki SUMMARY 및 테스트 가이드 최신화 |
| S4P-30 | 이미지 업로드 진단 결과와 후속 대응 범위 기록 |
| S4P-13 | Vitest, Testing Library, jsdom, Playwright 기반 프론트 테스트 환경 추가 |

---

## 🔧 주요 변경 사항
- **BE:** Django REST API, perfume detail/image 모델 및 migration, recommendation response mapping, Swagger schema 보강
- **FE:** Vite React fragrance experience, 추천 응답 adapter, ImageUploader 흐름, Vitest/Playwright 테스트 추가
- **LLM / RAG:** Vector RAG 및 기술 스택 wiki 문서 정리, 추천 API contract 문서화
- **Infra:** Docker Compose project/service 구성, MySQL init/startup script, `.env.example`, `.gitattributes`, test artifact ignore 처리

---

## 🧪 테스트 결과
- [x] 로컬 실행 확인
- [x] 엔드포인트 응답 확인
- [x] 유닛 테스트

| Metric | Result | Note |
|:---|:---:|:---|
| backend recommendation tests | PASS | `backend/app/perfumes/tests.py` 기준 API/서비스 테스트 추가 |
| frontend unit test | PASS | `corepack yarn test:run` 통과 |
| frontend E2E test | PASS | `corepack yarn test:e2e` 통과 |
| Swagger schema | PASS | analyze endpoint request/response serializer 및 example 반영 |

---

## ⚠️ 리뷰 요청 사항
리뷰어가 특히 확인해줬으면 하는 부분을 적습니다.
- `upstream/dev` 이후 누적 커밋이 포함된 PR이라 변경 범위가 큽니다. 이슈별 작업 내용이 의도한 범위와 맞는지 확인 부탁드립니다.
- 추천 API 응답 구조 변경이 frontend adapter와 기존 UI에 호환되는지 확인 부탁드립니다.
- ImageUploader의 double drop 중복 처리 현상은 테스트와 wiki에 기록했으며, 별도 fix 이슈로 분리할지 확인 부탁드립니다.

---

## ✔️ 최종 체크리스트
- [x] Jira 이슈 키가 참조용으로 정확히 입력됐다 (`Refs S4P-13` 등)
- [x] 커밋 메시지 형식을 지켰다 (`type(scope): 내용`)
- [x] 코드 컨벤션을 준수했다
- [x] 불필요한 로그 및 임시 파일을 제거했다
- [x] 로컬에서 정상 동작을 확인했다
