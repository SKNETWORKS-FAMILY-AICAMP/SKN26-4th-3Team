# Olfít Connect: Vector RAG Implementation Guide

본 문서는 **Olfít Connect**의 다음 개발 단계인 **"벡터 임베딩 및 하이브리드 RAG 검색"**을 구현하는 팀원을 위한 기술 가이드입니다. 현재 구축된 5축 아우라 시스템을 기반으로 정밀한 시맨틱 검색을 결합하는 방법을 설명합니다.

---

## 1. 현재 시스템 상태 (Current State)

- **데이터베이스**: MySQL 8.4에 800+ 향수 데이터가 적재되어 있습니다.
- **아우라 스코어링**: 이미지 분석 및 취향 선택을 통해 5축(Floral, Woody 등) 벡터가 실시간으로 계산됩니다.
- **임베딩 준비**: `Perfume` 모델의 `data` 필드 내에 **`embedding_doc`** 문자열이 이미 생성되어 저장되어 있습니다.
  - *형식*: `[브랜드] [상품명] [설명]. [어코드] 분위기의 [성분] 향이 느껴지는 [계열] 향수.`

---

## 2. 다음 단계: 벡터 임베딩 파이프라인 (Roadmap)

### Step 1: 벡터 DB(Pinecone) 인프라 구축
1.  [Pinecone](https://www.pinecone.io/) 계정을 생성하고 API Key를 획득합니다.
2.  `.env` 파일에 `PINECONE_API_KEY`, `PINECONE_ENVIRONMENT`, `PINECONE_INDEX_NAME`을 추가합니다.
3.  1536차원(OpenAI `text-embedding-3-small` 기준) 또는 선택한 모델의 차원에 맞는 인덱스를 생성합니다.

### Step 2: 벌크 임베딩 및 인덱싱 (Management Command)
1.  `perfumes/management/commands/index_to_pinecone.py` (이미 골격이 구현됨)를 완성합니다.
2.  MySQL의 모든 `Perfume` 레코드를 순회하며 `embedding_doc`을 벡터로 변환합니다.
3.  변환된 벡터를 `id`, `metadata`(이름, 브랜드, 아우라 점수 등)와 함께 Pinecone에 업로드합니다.

### Step 3: 백엔드 검색 로직 고도화 (`RecommendationService`)
현재의 1차 필터링 방식을 벡터 검색으로 교체합니다.
1.  사용자의 분석 결과인 `query_text`를 실시간으로 임베딩합니다.
2.  Pinecone에서 상위 50~100개의 후보군을 유사도 기반으로 추출합니다.
3.  추출된 후보군을 대상으로 **기존의 Aura Similarity + Preference Boost**를 적용하여 최종 Top 5를 재정렬(Re-ranking)합니다.

---

## 3. 핵심 파일 및 확장 가이드 (Target Files)

다음 팀원은 아래의 구분표를 기준으로 작업을 진행해야 합니다.

### 🔴 불변 로직 (Immutable - 수정 금지)
시스템의 정체성과 수학적 정합성을 유지하는 로직입니다.
- **`lib/scent_engine/vision.py`**: VLM 호출 및 키워드 추출 로직. (Gemma 모델의 프롬프트와 분석 규격은 유지해야 함)
- **`perfumes/services/aura_service.py`**: 5축 스코어링 수식 및 취향 가중치(60:40) 로직. (아우라 벡터 생성 방식은 그대로 유지)
- **`perfumes/views.py`**: API 응답 스키마 및 세션 검증 로직. (프론트엔드와의 계약이므로 필드명을 바꾸면 안 됨)

### 🟢 변화 및 확장 로직 (Mutable - 수정 대상)
벡터 RAG 연동을 위해 반드시 수정/구현해야 하는 로직입니다.
- **`perfumes/services/recommendation_service.py`**: 
  - **`recommend()` 함수 상단**: 기존 `Perfume.objects.filter()`를 통한 1차 필터링을 삭제하고, **Pinecone 유사도 검색 로직**을 주입하세요.
  - **결과 병합**: Pinecone에서 가져온 후보군을 대상으로 기존의 `Aura Similarity` 재정렬 로직을 연결하세요.
- **`perfumes/management/commands/index_to_pinecone.py`**: 
  - 현재 비어있는 `handle()` 로직을 구현하여 DB 데이터를 Pinecone으로 벌크 업로드하세요.
- **`.env`**:
  - `PINECONE_API_KEY`, `OPENAI_API_KEY`(임베딩용) 등 신규 자격 증명을 추가하세요.

---

## 4. AI 개발 팁 (For AI Assistant)

이 프로젝트의 코드는 상세한 주석과 함께 **Header/Footer** 구조를 가지고 있습니다. AI에게 작업을 지시할 때 다음 프롬프트를 활용하세요:

> "현재 `AuraService`가 생성하는 `query_text`를 받아 OpenAI 임베딩 API를 호출하고, 그 결과로 Pinecone 인덱스를 조회하여 후보군을 반환하는 함수를 `RecommendationService`에 추가해줘. 기존 5축 유사도 재정렬 로직은 그대로 유지해야 해."

---

## 5. 문의 및 히스토리
- **v1.0**: 5축 아우라 스코어링 및 하이브리드 저장소 구축 완료.
- **v2.0 (Next)**: 벡터 RAG 기반 시맨틱 검색 연동 예정.

**Good Luck, Connect the Scents!**
