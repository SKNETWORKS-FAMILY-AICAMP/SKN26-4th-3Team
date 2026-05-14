# Recommendation API Contract

## Status

Accepted. 최근 추천 관련 작업은 다음 커밋 기준으로 문서화한다.

- `1f2aae5 feat(perfumes): persist perfume image assets`
- `32ea455 feat(api): include perfume details in recommendations`
- `b9dd43c fix(frontend): map detailed recommendation payloads`
- `1950d08 fix(recommendations): split scent pyramid notes`

## Context

추천 화면은 백엔드 추천 결과를 카드와 상세 모달에 그대로 사용한다. 따라서 API는 단순한 상품명 목록이 아니라 다음 정보를 안정적으로 내려줘야 한다.

- 브랜드, 한글명, 영문명, 가격, 용량, 계열
- 추천 점수와 추천 사유
- 제품 이미지 URL 또는 Base64 이미지
- 제품 설명과 사용 상황 키워드
- Top, Middle, Base 향 노트 피라미드

이 정보는 `Perfume`, `PerfumeDetail`, `PerfumeImage`에 나뉘어 저장된다. 원본 크롤링 JSON은 `PerfumeRawData`에 보존하고, 서비스 표시와 추천에 필요한 정규화 값은 `PerfumeDetail.data`에 둔다.

## Response Shape

`RecommendationService.recommend()`는 `recommendations` 배열의 각 항목을 다음 형태로 반환한다.

```json
{
  "id": 1,
  "name": "옴니아 크리스탈린",
  "brand": "BVLGARI",
  "price": "$150",
  "price_krw": 207000,
  "size": "65ml",
  "image": "/static/perfumes/images/bvlgari/omnia.jpg",
  "perfume": {
    "id": 1,
    "brand": "BVLGARI",
    "koreanName": "옴니아 크리스탈린",
    "englishName": "omnia crystalline",
    "productType": "perfume",
    "family": "프레시",
    "price": { "raw": "$150", "amount": 150, "currency": "USD" },
    "description": "옴니아 크리스탈린 설명",
    "notes": ["대나무", "서양배", "연꽃"],
    "representativeNotes": ["대나무", "서양배"],
    "notesPyramid": {
      "top": ["대나무"],
      "middle": ["서양배"],
      "base": ["연꽃"]
    }
  },
  "imageDetail": {
    "url": "/static/perfumes/images/bvlgari/omnia.jpg",
    "originalUrl": "https://img.example.com/omnia.jpg",
    "backendPath": "/backend/app/static/perfumes/images/bvlgari/omnia.jpg",
    "base64": "base64-image"
  },
  "tags": ["우디", "플로럴"],
  "notes": "대나무, 서양배",
  "family": "프레시",
  "category": "Personal",
  "similarity": 90,
  "matchReason": "선택하신 #대나무 성분이 포함되어 있으며, 당신의 #프레시 아우라와 완벽하게 조화됩니다.",
  "details": {
    "story": "옴니아 크리스탈린 설명",
    "topNotes": "대나무",
    "middleNotes": "서양배",
    "baseNotes": "연꽃",
    "bestFor": "상쾌한, 우아한"
  }
}
```

`details`는 프론트엔드 `Product` 타입의 상세 모달 표시 계약에 맞춘 필드다. `perfume`은 백엔드 원천 상세 payload에 가깝고, 이후 상세 페이지나 디버깅에서 더 많은 정보를 참조할 때 사용한다.

## Image Payload

이미지는 `PerfumeImage` 모델에 별도로 저장한다.

- `original_url`: 원본 이미지 URL
- `processed_path`: 백엔드가 저장한 로컬 이미지 경로
- `base64_data`: 다운로드된 이미지 Base64

추천 응답은 `imageDetail.url`에 브라우저가 접근 가능한 `/static/...` 경로를 우선 담는다. Base64가 있으면 프론트엔드는 `data:image/jpeg;base64,...` 형태로 정규화해서 표시할 수 있다.

## Scent Pyramid Rules

향 노트 피라미드는 다음 우선순위로 만든다.

1. `PerfumeDetail.data.notes_parsed.top/middle/base`가 있으면 그대로 사용한다.
2. 원본 데이터의 `notes`가 `{top, middle, base}` 딕셔너리면 `load_perfumes`가 한글 표준화 후 `notes_parsed`로 보존한다.
3. `notes_parsed`가 없으면 `representative_notes`, `standardized_notes`, `notes` 순서로 flat notes를 가져와 Top/Middle/Base로 나눈다.

Flat notes fallback은 MID/BASE가 빈 문자열로 내려가 모달에 빈 행이 생기는 문제를 막기 위한 방어 로직이다. 이 fallback은 원본 데이터가 피라미드 구조를 제공하지 않는 경우의 표시 품질을 위한 것이며, 실제 조향 순서를 보장하는 데이터는 아니다.

## Frontend Mapping

프론트엔드 `normalizeBackendRecommendation()`은 백엔드 추천 항목을 기존 `Product` 타입으로 변환한다.

- `details.topNotes`, `details.middleNotes`, `details.baseNotes`를 우선 사용한다.
- 상세 노트가 비어 있을 때만 대표 노트 문자열을 Top fallback으로 사용한다.
- `imageDetail.base64`, `imageAsset.base64`, `/static/...` URL 순서로 이미지 표시 값을 만든다.

이 매핑은 백엔드 API 계약을 보존하면서도 로컬 fallback 상품 데이터와 같은 `Product` UI 컴포넌트를 재사용하기 위한 adapter 역할을 한다.

## Verification

추천 응답 계약은 백엔드 서비스 테스트로 고정한다.

```bash
docker compose run --rm backend sh -c "cd /backend/app && python manage.py test perfumes.tests.RecommendationServiceTest --keepdb"
```

프론트엔드 타입/번들 검증은 다음 명령을 사용한다.

```bash
cd frontend
npm run build
```
