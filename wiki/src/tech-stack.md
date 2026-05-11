# Tech Stack

이 문서는 현재 저장소에 실제 적용된 기술 스택을 기준으로 정리한다. 예정된 확장 기술은 별도 섹션에 구분한다.

## Runtime and Language

| Area | Stack | Usage |
| --- | --- | --- |
| Backend runtime | Python 3.12 | Django API 서버 실행 |
| Frontend language | TypeScript 5.9 | React 컴포넌트와 클라이언트 로직 작성 |
| Frontend runtime | Node.js / Yarn | Vite 개발 서버와 프론트엔드 의존성 관리 |

## Backend

| Stack | Version / Package | Usage |
| --- | --- | --- |
| Django | `django>=6.0.5` | 백엔드 웹 프레임워크 |
| Django REST Framework | `djangorestframework>=3.17.1` | REST API 구현 |
| django-environ | `django-environ>=0.13.0` | 환경 변수 기반 설정 로드 |
| django-cors-headers | `django-cors-headers>=4.9.0` | 프론트엔드와 API 간 CORS 처리 |
| drf-spectacular | `drf-spectacular>=0.28.0` | OpenAPI 문서화 기반 |
| mysqlclient | `mysqlclient>=2.2.8` | Django와 MySQL 연결 |
| pytest / pytest-django | `pytest>=8.0.0`, `pytest-django>=4.9.0` | 백엔드 테스트 |

## AI and Recommendation

| Stack | Version / Package | Usage |
| --- | --- | --- |
| OpenAI Python SDK | `openai>=1.12.0` | NVIDIA NIM 호환 API 호출 기반 |
| NumPy | `numpy>=1.26.0` | 아우라 벡터 연산 |
| scikit-learn | `scikit-learn>=1.4.0` | 코사인 유사도 기반 추천 점수 계산 |
| Pillow | `pillow>=10.2.0` | 이미지 처리 확장 기반 |
| requests | `requests>=2.32.3` | 외부 HTTP 요청 |

현재 추천 로직은 MySQL에서 후보 향수를 조회한 뒤, Python 서비스 레이어에서 아우라 벡터와 취향 노트를 기반으로 재정렬한다.

## Frontend

| Stack | Version / Package | Usage |
| --- | --- | --- |
| React | `react^19.2.0`, `react-dom^19.2.0` | UI 컴포넌트 구성 |
| Vite | `vite^7.2.4` | 개발 서버와 번들링 |
| React Router | `react-router^7.6.1` | 클라이언트 라우팅 |
| Zustand | `zustand^5.0.13` | 전역 상태 관리 |
| Axios | `axios^1.16.0` | API 통신 |
| Recharts | `recharts^2.15.4` | 레이더 차트 등 데이터 시각화 |
| html2canvas | `html2canvas^1.4.1` | 분석 리포트 이미지 캡처 |
| Embla Carousel | `embla-carousel-react^8.6.0` | 캐러셀 UI |

## UI and Styling

| Stack | Version / Package | Usage |
| --- | --- | --- |
| Tailwind CSS | `tailwindcss^3.4.19` | 유틸리티 기반 스타일링 |
| Radix UI | `@radix-ui/react-*` | 접근성 기반 headless UI 컴포넌트 |
| shadcn-style component setup | `components.json`, Radix, Tailwind | 프로젝트 소유 컴포넌트 패턴 |
| Lucide React | `lucide-react^0.562.0` | 아이콘 |
| class-variance-authority | `class-variance-authority^0.7.1` | 컴포넌트 variant 관리 |
| clsx / tailwind-merge | `clsx^2.1.1`, `tailwind-merge^3.4.0` | 조건부 클래스 병합 |
| tailwindcss-animate / tw-animate-css | `tailwindcss-animate^1.0.7`, `tw-animate-css^1.4.0` | 애니메이션 유틸리티 |

## Database

| Stack | Version / Config | Usage |
| --- | --- | --- |
| MySQL | `mysql:8.4.9` | 메인 RDB |
| InnoDB | MySQL 기본 스토리지 엔진 | 트랜잭션과 관계형 데이터 저장 |
| JSON column | Django `models.JSONField` | 향수 상세 문서, 노트, 가격, 아우라 프로필 등 반정형 데이터 저장 |
| MySQL X Protocol | `mysqlx=ON`, port `33060` | 추후 MySQL Document Store 접근 기반 |
| utf8mb4 | `utf8mb4_0900_ai_ci` | 한글 향수 데이터 저장 |

현재 운영 모델은 RDB 중심이다. `Brand`, `Perfume`의 식별과 필터링 필드는 정규 컬럼으로 관리하고, 향수 상세 정보는 JSON 컬럼에 보관한다.

## Infrastructure

| Stack | Usage |
| --- | --- |
| Docker | 프론트엔드, 백엔드, 데이터베이스 컨테이너 이미지 빌드 |
| Docker Compose | Vite, Django 백엔드, MySQL 로컬 오케스트레이션 |
| Named volume `mysql_data` | MySQL 데이터 영속화 |
| Named volume `frontend_node_modules` | 프론트엔드 컨테이너 의존성 보존 |
| Healthcheck | MySQL 준비 상태 확인 후 백엔드 기동 |
| JSON file logging | 컨테이너 로그 크기와 보관 개수 제한 |

## Documentation and CI

| Stack | Usage |
| --- | --- |
| mdBook | `wiki` 디렉터리의 프로젝트 문서 사이트 |
| GitHub Actions | mdBook 배포와 코드 리뷰 자동화 워크플로 |
| Conventional Commits | scope 기반 변경 이력 관리 |

## Planned Extensions

| Stack | Status | Purpose |
| --- | --- | --- |
| MySQL Document Store | Deferred | `PerfumeDocument` 같은 JSON 문서 저장 계층 분리 후보 |
| Pinecone or Vector DB | Deferred | 향수 `embedding_doc` 기반 벡터 검색 |
| OpenAI embeddings | Deferred | RAG 검색용 임베딩 생성 |

추후 확장 방향은 Backend 섹션의 MySQL Document Store Roadmap과 Vector RAG 문서를 기준으로 진행한다.
