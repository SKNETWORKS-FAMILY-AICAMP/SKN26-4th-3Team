# 🔄 Olfít 시퀀스 다이어그램 (Sequence Diagram)

향수 추천 요청 시 컴포넌트 간 상호작용 및 API 호출 순서를 기술한다.

## 1. 하이브리드 추천 시나리오 (Main Flow)

사용자가 사진을 업로드하고 "분석하기"를 클릭했을 때 발생하는 전체 시퀀스입니다.

![sequence_diagram](../../assets/backend/architecture/sequence_diagram.png)

### 시퀀스 설명
1.  **Frontend → Backend**: 이미지(Base64)와 선택된 노트 리스트를 담아 `/api/analyze/` 호출.
2.  **Backend → NVIDIA NIM**: `VLEngine`이 이미지를 전달하여 시각적 특징(JSON) 분석 요청.
3.  **NVIDIA NIM → Backend**: 스타일, 색상, 사물 등이 담긴 JSON 응답.
4.  **Backend (AuraService)**: 
    - `scent_engine`을 통해 시각 데이터 매핑.
    - 사용자 취향과 결합하여 5축 아우라 점수 산출.
    - 대칭형 RAG 검색 쿼리 생성.
5.  **Backend → OpenAI**: 검색 쿼리를 1536차원 벡터로 변환(Embedding).
6.  **Backend → Pinecone**: 임베딩 벡터로 시맨틱 검색 수행.
7.  **Pinecone → Backend**: 유사도 높은 향수 후보군(Top 30) 메타데이터 반환.
8.  **Backend (RecommendationService)**:
    - 후보군 향수들의 아우라 벡터와 사용자 아우라 벡터 간 코사인 유사도 계산.
    - RAG 점수와 가중 합산하여 최종 Top 5 재정렬.
9.  **Backend → MySQL**: 선정된 Top 5 향수의 **상세 이미지(Base64 등)**를 DB에서 일괄 조회합니다. (텍스트 정보는 Pinecone 메타데이터를 활용하여 DB 부하를 최소화합니다.)
10. **Backend → Frontend**: 최종 추천 결과(Top 5) 및 아우라 분석 리포트 반환.

---

## 2. 예외 및 Fallback 시나리오

### 2.1 Pinecone/OpenAI 장애 시
- **동작**: 시스템은 Pinecone 장애를 감지하면 즉시 **MySQL Fallback** 모드로 전환합니다.
- **로직**: 사용자의 메인 아우라 계열(Main Family)과 일치하는 향수들을 DB에서 1차 필터링한 후, 아우라 유사도만으로 추천을 수행합니다.

### 2.2 VLM 분석 실패 시
- **동작**: NVIDIA API 타임아웃 혹은 JSON 파싱 오류 시 `DUMMY_RESULT`를 반환합니다.
- **목적**: 서비스가 완전히 중단되지 않도록 기본 스타일 분석 결과를 제공하여 사용자 경험을 유지합니다.

---

## 3. 핵심 설계 포인트
- **동기식 처리**: 정확한 분석 결과를 위해 전체 프로세스는 동기적으로 처리되나, 각 API 호출에는 타임아웃을 설정하여 무한 대기를 방지합니다.
- **Stateless**: 백엔드는 별도의 세션 상태를 유지하지 않으며, 모든 필요 정보는 요청 시 전달되거나 추천 결과에 포함되어 반환됩니다.
