# Backend

백엔드 설계, 데이터 저장 전략, RAG 확장 방향을 정리한다.

- [MySQL Document Store Roadmap](./backend/mysql-document-store-roadmap.md)
- [Recommendation API Contract](./backend/recommendation-api-contract.md)
- [Vector RAG](./backend/vector-rag.md)

## Current Recommendation Flow

현재 추천 API는 `perfumes/views.py`의 `AnalyzeView`가 오케스트레이션한다.

1. 프론트엔드가 이미지 Base64와 `selectedNotes`를 전송한다.
2. `VLEngine`이 이미지에서 시각 키워드를 추출한다.
3. `AuraService`가 이미지 키워드와 사용자가 고른 노트를 결합해 5축 아우라 점수를 만든다.
4. `RecommendationService`가 MySQL의 향수 후보를 조회하고, 아우라 유사도와 취향 노트 매칭을 조합해 Top 5를 반환한다.

추천 응답은 프론트엔드 모달이 바로 렌더링할 수 있도록 상품 기본 정보뿐 아니라 상세 설명, 가격, 이미지, 향 노트 피라미드까지 포함한다. 이 계약은 `Recommendation API Contract` 문서에서 관리한다.
