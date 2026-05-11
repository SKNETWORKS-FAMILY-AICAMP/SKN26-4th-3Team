# Olfít Connect: Backend & Recommendation Engine

Olfít Connect의 핵심 지능을 담당하는 백엔드 서버입니다. NVIDIA NIM VLM을 통한 이미지 분석과 800여 개의 실제 향수 데이터를 기반으로 한 지능형 추천 시스템이 구현되어 있습니다.

## 1. Project Structure (Detailed)

백엔드 폴더 구조와 각 구성 요소의 역할은 다음과 같습니다.

```text
backend/
├── Dockerfile              # 백엔드 컨테이너 빌드 정의 (Python 3.12-slim)
├── requirements.txt        # 백엔드 의존성 패키지 (Django, DRF, OpenAI, NumPy 등)
├── README.md               # 본 문서
└── app/                    # Django 프로젝트 소스 루트
    ├── manage.py           # Django 관리 스크립트
    ├── app/                # 프로젝트 설정 폴더
    │   ├── settings.py     # DB, CORS, AI API 등 전역 설정
    │   └── urls.py         # 최상위 API 라우팅
    ├── perfumes/           # 향수 추천 핵심 앱
    │   ├── models.py       # Brand, Perfume 테이블 정의 (RDB-JSON Hybrid)
    │   ├── views.py        # API 엔드포인트 로직 (AnalyzeView)
    │   ├── urls.py         # perfumes 앱 전용 라우팅
    │   ├── utils.py        # 매핑 데이터 로더 및 유틸리티
    │   ├── tests.py        # TDD 기반 API 통합 테스트 코드
    │   ├── services/       # 비즈니스 로직 레이어
    │   │   ├── aura_service.py      # 5축 스코어링 및 쿼리 생성
    │   │   └── recommendation_service.py # 하이브리드 재랭킹 엔진
    │   ├── management/     # 관리 명령 (Batch Jobs)
    │   │   └── commands/
    │   │       ├── load_perfumes.py     # JSON -> MySQL 적재 (ETL)
    │   │       └── index_to_pinecone.py # 벡터 DB 인덱싱 (확장 포인트)
    │   └── data/           # 앱 내부 정적 데이터
    │       └── mappings/   # 마스터 맵, 성분 번역, 무드 기술서 등 JSON
    ├── lib/                # 외부 독립 라이브러리
    │   └── scent_engine/   # [Core Intelligence]
    │       ├── vision.py   # NVIDIA NIM VLM 연동 엔진
    │       ├── mapper.py   # 시각 키워드 -> 향기 어코드 매핑 로직
    │       ├── rules.py    # 매핑 규칙 정의 데이터
    │       └── utils.py    # JSON 추출 및 VLM 결과 정규화
    └── data/               # 데이터 소스
        └── raw/            # 800여 개의 원본 향수 JSON 파일셋
```

---

## 2. Data Architecture

Olfít Connect는 관계형 메타데이터(MySQL)와 유연한 상세 정보(JSON)를 결합한 **하이브리드 저장 구조**를 채택합니다.

### RDB Schema (`perfumes_perfume` 테이블)

| Column | Type | Description |
| :--- | :--- | :--- |
| **id** | Integer | 고유 식별자 (Primary Key) |
| **brand_id** | ForeignKey | 브랜드 테이블 참조 (Brand 명칭 등) |
| **korean_name** | CharField | 상품의 공식 한글 명칭 |
| **english_name** | CharField | 상품의 공식 영문 명칭 (Unique Key) |
| **product_type** | CharField | 세부 분류 (cologne, eau_de_parfum 등) |
| **family** | CharField | 5대 핵심 계열 (플로럴, 우디, 프레시 등) |
| **data** | JSONField | **[하이브리드 데이터]** 상세 스펙 및 AI 분석 데이터 |

### JSON Data Detail (`data` 필드 예시)

`data` 컬럼에는 변동성이 크거나 검색 연산이 필요 없는 상세 정보들이 구조화되어 저장됩니다. 특히 **`description`** 필드는 프론트엔드에서 **`details.story`**로 매핑되어 사용됩니다.

```json
{
  "description": "자유롭고 대담한 여성을 위한 시프레 플로럴 향수...", // DB 저장 원본 (details.story로 매핑)
  "price": {
    "raw": "$185",
    "amount": 185,
    "currency": "USD"
  },
  "volume": "100ml",
  "image_url": "https://img.fraganty.ai/perfume/611.jpg",
  "notes": ["오렌지", "베르가못", "장미", "자스민", "패출리"],
  "accords": ["시트러스", "우디", "패출리", "로즈"],
  "keywords": ["우아한", "세련된", "여성스러운"],
  "aura_profile": {
    "플로럴": 0.35,
    "우디": 0.20,
    "오리엔탈": 0.15,
    "프레시": 0.30,
    "구르망": 0.00
  },
  "embedding_doc": "CHANEL 코코 마드모아젤... 시트러스, 우디 분위기의... 플로럴 계열 향수."
}
```


---

## 3. Core Services

- **VLEngine**: 이미지에서 시각적 감성 키워드를 추출 (NVIDIA NIM).
- **AuraService**: 비전 키워드 + 사용자 취향을 5축 벡터로 융합 (60:40 비율).
- **RecommendationService**: DB 후보군 필터링 및 70/30 하이브리드 재랭킹.

---

## 4. Getting Started & Testing

```powershell
# 프로젝트 루트에서 실행
docker compose up -d --build

# 테스트 실행
docker compose exec backend python app/manage.py test perfumes
```

---
@footer
Olfít Connect Project - Backend Technical Documentation
