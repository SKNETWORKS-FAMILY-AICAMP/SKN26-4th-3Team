"""
@file recommendation_service.py
@module Perfumes/Services/RecommendationService
@description
RAG 후보 검색 + 5축 아우라 코사인 유사도 재정렬 기반 향수 추천 서비스입니다.

기존 방식:
    family 기준 DB 후보 추출
    → Aura Similarity 70% + Preference Boost 30%
    → Top 5 추천

최종 수정 방식:
    AuraService가 생성한 query_text
    + 사용자가 직접 선택한 향 성분
    + 5축 아우라 프로필
    → OpenAI Embedding
    → Pinecone에서 embedding_doc 기준 Top-K 후보 검색
    → 후보군에 대해서만 5축 aura_profile 코사인 유사도 계산
    → aura similarity 기준 Top 5 추천

핵심:
- RAG는 의미적으로 가까운 후보군을 가져오는 역할입니다.
- 5축 아우라 코사인 유사도는 최종 재정렬 기준입니다.
- 기존 70:30 임의 가중치 점수식은 사용하지 않습니다.
"""

import os
from typing import Any

import numpy as np
from django.db.models import Case, IntegerField, When
from sklearn.metrics.pairwise import cosine_similarity

from perfumes.models import Perfume
from ..utils import load_preference_expansion, load_master_map


class RecommendationService:
    """
    [Hybrid RAG + Aura Re-ranking Engine]

    1. query_text 기반 Pinecone RAG 검색으로 후보군을 가져옵니다.
    2. 후보군 안에서 사용자 5축 아우라와 향수 aura_profile의 코사인 유사도로 재정렬합니다.
    """

    def __init__(self):
        self.master_map = load_master_map()
        self.axes = ["플로럴", "우디", "오리엔탈", "프레시", "구르망"]

        self.exchange_rates = {
            "USD": 1380,
            "EUR": 1490,
            "GBP": 1730,
            "KRW": 1,
        }

        self.pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "olfit-perfumes")
        self.embedding_model = os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            "text-embedding-3-small",
        )

        # RAG로 가져올 후보 수. 기본 50개.
        self.rag_top_k = int(os.getenv("RAG_TOP_K", "50"))

    def recommend(self, user_aura_dict, query_text, selected_notes):
        """
        사용자 아우라와 RAG query_text를 기반으로 향수를 추천합니다.

        @param user_aura_dict: 사용자의 5축 아우라 점수 딕셔너리
        @param query_text: AuraService에서 생성한 RAG 검색용 쿼리
        @param selected_notes: 사용자가 선택한 성분 리스트
        @return: 정렬된 Top 5 향수 결과 리스트
        """

        main_family = self._get_main_family(user_aura_dict)

        # [Step 1] query_text에 사용자 취향과 5축 아우라 정보를 명시적으로 보강
        enhanced_query_text = self._build_enhanced_rag_query(
            query_text=query_text,
            user_aura_dict=user_aura_dict,
            selected_notes=selected_notes,
            main_family=main_family,
        )

        # [Step 2] RAG 후보 검색: Pinecone에서 의미적으로 가까운 향수 후보 Top-K 추출
        rag_matches = self._search_pinecone(
            query_text=enhanced_query_text,
            top_k=self.rag_top_k,
        )

        if rag_matches:
            candidates = self._load_perfumes_by_rag_matches(rag_matches)
        else:
            # Pinecone 장애/미설정 시 예외 fallback
            # 정상 방향은 RAG 후보 검색 + 5축 재정렬이다.
            candidates = self._fallback_candidates(main_family)

        # [Step 3] 사용자 아우라 벡터 생성
        user_aura_vector = self._build_user_aura_vector(user_aura_dict)

        # [Step 4] 사용자 선택 노트 확장
        # 최종 점수 가산용이 아니라 추천 이유 설명용으로 사용한다.
        target_notes = self._expand_selected_notes(selected_notes)

        # [Step 5] 후보군 안에서 5축 아우라 코사인 유사도 기반 재정렬
        ranked_results = []

        for item in candidates:
            perfume = item["perfume"]
            rag_score = item["rag_score"]

            p_data = perfume.data or {}

            p_aura = p_data.get("aura_profile")
            if not p_aura:
                p_aura = self._calculate_aura_on_the_fly(p_data.get("notes", []))

            perfume_aura_vector = self._build_perfume_aura_vector(p_aura)
            aura_sim = cosine_similarity(
                [user_aura_vector],
                [perfume_aura_vector],
            )[0][0]

            p_notes = set(
                p_data.get("representative_notes")
                or p_data.get("notes", [])
                or []
            )

            matches = p_notes & target_notes

            similarity_percent = self._score_to_percent(aura_sim)
            price_krw = self._convert_to_krw(p_data.get("price"))

            ranked_results.append(
                {
                    "id": perfume.id,
                    "name": perfume.korean_name,
                    "brand": perfume.brand.name,
                    "price": self._get_price_raw(p_data),
                    "price_krw": price_krw,
                    "size": p_data.get("volume", "N/A"),
                    "image": p_data.get("image_url", ""),
                    "tags": p_data.get("accords", [])[:3],
                    "notes": ", ".join(
                        (p_data.get("representative_notes") or p_data.get("notes", []))[:5]
                    ),
                    "family": perfume.family,
                    "category": "Personal",

                    # 최종 추천 점수: 5축 아우라 코사인 유사도 기반
                    "similarity": similarity_percent,
                    "auraScore": round(float(aura_sim), 4),

                    # RAG 후보 검색 점수: 디버깅/설명용으로 별도 보존
                    "ragScore": round(float(rag_score), 4),

                    "matchReason": self._generate_hybrid_reason(
                        matches=matches,
                        main_family=main_family,
                        selected_notes=selected_notes,
                        user_aura_dict=user_aura_dict,
                        perfume_data=p_data,
                        rag_score=rag_score,
                        aura_score=aura_sim,
                    ),
                    "details": {
                        "story": p_data.get("description", ""),
                        "topNotes": ", ".join(
                            p_data.get("notes_parsed", {}).get("top", [])
                        ),
                        "middleNotes": ", ".join(
                            p_data.get("notes_parsed", {}).get("middle", [])
                        ),
                        "baseNotes": ", ".join(
                            p_data.get("notes_parsed", {}).get("base", [])
                        ),
                        "bestFor": ", ".join(self._safe_keywords(p_data)[:3]),

                        # 디버깅 및 설명용
                        "embeddingDoc": p_data.get("embedding_doc", ""),
                        "queryText": query_text,
                        "enhancedQueryText": enhanced_query_text,
                    },
                }
            )

        # 최종 Top 5는 aura similarity 기준으로 재정렬
        return sorted(
            ranked_results,
            key=lambda x: x.get("auraScore", 0),
            reverse=True,
        )[:5]

    def _build_enhanced_rag_query(
        self,
        query_text: str,
        user_aura_dict: dict[str, float] | None,
        selected_notes,
        main_family: str,
    ) -> str:
        """
        AuraService가 만든 기본 query_text에 사용자 취향과 5축 아우라 정보를 추가합니다.

        목적:
        - RAG 검색 후보군을 더 정확히 가져오기 위함
        - 사용자가 직접 선택한 노트와 5축 아우라 방향성을 임베딩 검색문에 반영
        - 단, 최종 점수에 임의 비율로 가산하지는 않음
        """

        parts: list[str] = []

        if query_text and str(query_text).strip():
            parts.append(str(query_text).strip())

        cleaned_selected_notes = self._normalize_text_list(selected_notes)

        if cleaned_selected_notes:
            for note in cleaned_selected_notes:
                parts.append(f"user_preference_note:{note}")

            notes_text = ", ".join(cleaned_selected_notes)
            parts.append(f"사용자가 직접 선호한 향 성분은 {notes_text}입니다.")
            parts.append(f"{notes_text} 성분이 포함되거나 유사한 분위기의 향수를 우선적으로 찾습니다.")

        aura_items = self._sorted_aura_items(user_aura_dict)

        if aura_items:
            top_aura = aura_items[:3]

            for axis, score in top_aura:
                parts.append(f"user_aura_axis:{axis}")
                parts.append(f"user_aura_score:{axis}:{score:.2f}")

            top_aura_text = ", ".join(
                [f"{axis} {score:.2f}" for axis, score in top_aura]
            )
            parts.append(f"사용자의 주요 향기 아우라는 {top_aura_text}입니다.")

        if main_family:
            parts.append(f"main_aura_family:{main_family}")
            parts.append(f"가장 강한 향기 계열은 {main_family}입니다.")

        return " ".join(parts)

    def _search_pinecone(self, query_text: str, top_k: int = 50) -> list[dict[str, Any]]:
        """
        query_text를 임베딩한 뒤 Pinecone에서 유사 향수 후보를 검색합니다.

        반환 형식:
        [
            {
                "perfume_id": 1,
                "score": 0.8123,
                "metadata": {...}
            }
        ]
        """

        openai_api_key = os.getenv("OPENAI_API_KEY")
        pinecone_api_key = os.getenv("PINECONE_API_KEY")

        if not query_text or not query_text.strip():
            print("[RAG] query_text가 비어 있어 Pinecone 검색을 건너뜁니다.")
            return []

        if not openai_api_key or not pinecone_api_key:
            print("[RAG] OPENAI_API_KEY 또는 PINECONE_API_KEY가 없어 fallback을 사용합니다.")
            return []

        try:
            from openai import OpenAI
            from pinecone import Pinecone

            client = OpenAI(api_key=openai_api_key)
            pc = Pinecone(api_key=pinecone_api_key)
            index = pc.Index(self.pinecone_index_name)

            embedding_response = client.embeddings.create(
                model=self.embedding_model,
                input=query_text,
            )

            query_vector = embedding_response.data[0].embedding

            search_response = index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
            )

            matches = self._extract_matches(search_response)

            results: list[dict[str, Any]] = []

            for match in matches:
                perfume_id = self._extract_perfume_id(match)
                score = self._extract_score(match)
                metadata = self._extract_metadata(match)

                if perfume_id is None:
                    continue

                results.append(
                    {
                        "perfume_id": perfume_id,
                        "score": score,
                        "metadata": metadata,
                    }
                )

            return results

        except Exception as e:
            print(f"[RAG] Pinecone 검색 실패: {type(e).__name__}: {e}")
            return []

    def _load_perfumes_by_rag_matches(
        self,
        rag_matches: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Pinecone 검색 결과의 perfume_id 순서를 유지하면서
        MySQL Perfume 객체를 로드합니다.
        """

        ids = [item["perfume_id"] for item in rag_matches]
        score_by_id = {
            item["perfume_id"]: float(item.get("score", 0.0))
            for item in rag_matches
        }

        if not ids:
            return []

        preserved_order = Case(
            *[When(id=pk, then=pos) for pos, pk in enumerate(ids)],
            output_field=IntegerField(),
        )

        perfumes = (
            Perfume.objects.filter(id__in=ids)
            .select_related("brand")
            .order_by(preserved_order)
        )

        results = []

        for perfume in perfumes:
            results.append(
                {
                    "perfume": perfume,
                    "rag_score": score_by_id.get(perfume.id, 0.0),
                }
            )

        return results

    def _fallback_candidates(self, main_family: str) -> list[dict[str, Any]]:
        """
        Pinecone 미설정 또는 장애 시 사용하는 fallback입니다.
        """

        perfumes = list(
            Perfume.objects.filter(family=main_family)
            .select_related("brand")
            .order_by("id")[:50]
        )

        if len(perfumes) < 5:
            perfumes = list(
                Perfume.objects.all()
                .select_related("brand")
                .order_by("id")[:50]
            )

        return [
            {
                "perfume": perfume,
                "rag_score": 0.0,
            }
            for perfume in perfumes
        ]

    def _build_user_aura_vector(self, user_aura_dict: dict[str, float]) -> np.ndarray:
        """
        사용자 5축 아우라 dict를 numpy vector로 변환합니다.
        """

        if not user_aura_dict:
            return np.array([0.2 for _ in self.axes])

        values = []

        for axis in self.axes:
            try:
                values.append(float(user_aura_dict.get(axis, 0.2)))
            except (TypeError, ValueError):
                values.append(0.2)

        return np.array(values)

    def _build_perfume_aura_vector(self, perfume_aura_dict: dict[str, float]) -> np.ndarray:
        """
        향수 aura_profile dict를 numpy vector로 변환합니다.
        """

        if not perfume_aura_dict:
            return np.array([0.2 for _ in self.axes])

        values = []

        for axis in self.axes:
            try:
                values.append(float(perfume_aura_dict.get(axis, 0.2)))
            except (TypeError, ValueError):
                values.append(0.2)

        return np.array(values)

    def _expand_selected_notes(self, selected_notes) -> set[str]:
        """
        사용자가 선택한 성분을 확장합니다.

        예:
        우드 → 샌달우드, 시더우드 등
        """

        expansion_map = load_preference_expansion()

        target_notes = []

        for note in selected_notes or []:
            target_notes.extend(expansion_map.get(note, [note]))

        return set(target_notes)

    def _calculate_aura_on_the_fly(self, notes):
        """
        DB에 aura_profile이 없을 경우 성분 리스트로부터 실시간 아우라를 산출합니다.
        기존 RecommendationService 로직을 유지한 fallback입니다.
        """

        scores = {axis: 0.0 for axis in self.axes}

        for note in notes or []:
            ko_note = self.master_map["note_translations"].get(note, note)
            sub_accord = self.master_map["note_to_accord"].get(ko_note, "아로마틱")
            category = self.master_map["accord_to_category"].get(sub_accord, "기타")

            if category in scores:
                scores[category] += 1.0

        max_s = max(scores.values()) if scores.values() else 0

        if max_s == 0:
            return {axis: 0.2 for axis in self.axes}

        return {key: round(value / max_s, 2) for key, value in scores.items()}

    def _generate_hybrid_reason(
        self,
        matches: set[str],
        main_family: str,
        selected_notes,
        user_aura_dict: dict[str, float] | None,
        perfume_data: dict[str, Any],
        rag_score: float,
        aura_score: float,
    ) -> str:
        """
        RAG 후보 검색 + 5축 아우라 재정렬 기반 추천 사유를 생성합니다.
        """

        accords = perfume_data.get("accords", []) or []
        keywords = self._safe_keywords(perfume_data)
        notes = perfume_data.get("representative_notes") or perfume_data.get("notes", []) or []

        selected_notes_list = self._normalize_text_list(selected_notes)
        aura_items = self._sorted_aura_items(user_aura_dict)

        reason_parts = []

        if main_family:
            reason_parts.append(f"이미지와 취향에서 도출된 #{main_family} 아우라와 잘 맞습니다")

        if aura_items:
            top_axis = aura_items[0][0]
            reason_parts.append(f"5축 아우라 중 #{top_axis} 성향을 기준으로 재정렬되었습니다")

        if selected_notes_list:
            selected_text = ", ".join(selected_notes_list[:2])
            reason_parts.append(f"사용자가 직접 선택한 #{selected_text} 취향을 RAG 검색 쿼리에 반영했습니다")

        if matches:
            match_str = ", ".join(list(matches)[:2])
            reason_parts.append(f"실제 향수 노트에서도 #{match_str} 성분과 연결됩니다")

        if notes:
            note_str = ", ".join(notes[:2])
            reason_parts.append(f"{note_str} 노트가 이미지의 향 이미지와 유사합니다")

        if accords:
            accord_str = ", ".join(accords[:2])
            reason_parts.append(f"{accord_str} 계열의 분위기를 가지고 있습니다")

        if keywords:
            keyword_str = ", ".join(keywords[:2])
            reason_parts.append(f"{keyword_str} 인상으로 추천되었습니다")

        reason_parts.append(
            f"RAG 후보 점수 {float(rag_score):.2f}, 5축 유사도 {float(aura_score):.2f}를 기준으로 선별되었습니다"
        )

        return " · ".join(reason_parts) + "."

    def _convert_to_krw(self, price_data):
        """다양한 통화의 가격을 원화로 환산합니다."""
        if not price_data or not isinstance(price_data, dict):
            return 0

        amount = price_data.get("amount", 0)
        currency = str(price_data.get("currency", "KRW")).upper()
        rate = self.exchange_rates.get(currency, 1350)

        try:
            return int(float(amount) * rate)
        except (TypeError, ValueError):
            return 0

    def _get_price_raw(self, perfume_data: dict[str, Any]) -> str:
        """가격 원문을 안전하게 반환합니다."""
        price = perfume_data.get("price", {})

        if isinstance(price, dict):
            return price.get("raw", "정보없음") or "정보없음"

        if isinstance(price, str) and price.strip():
            return price.strip()

        return "정보없음"

    def _safe_keywords(self, perfume_data: dict[str, Any]) -> list[str]:
        """
        keywords가 list 또는 dict 형태로 들어오는 경우를 모두 처리합니다.
        """

        keywords = perfume_data.get("keywords", [])

        if isinstance(keywords, list):
            return [str(k) for k in keywords if str(k).strip()]

        if isinstance(keywords, dict):
            result = []

            for key in ["ko", "en"]:
                values = keywords.get(key, [])
                if isinstance(values, list):
                    result.extend([str(v) for v in values if str(v).strip()])

            return result

        return []

    def _normalize_text_list(self, values) -> list[str]:
        """
        문자열/리스트/None 입력을 중복 없는 list[str]로 정리합니다.
        """

        if not values:
            return []

        if isinstance(values, str):
            raw_values = [values]
        elif isinstance(values, list):
            raw_values = values
        elif isinstance(values, tuple) or isinstance(values, set):
            raw_values = list(values)
        else:
            raw_values = [values]

        result = []
        seen = set()

        for value in raw_values:
            cleaned = str(value).strip()

            if not cleaned:
                continue

            if cleaned in seen:
                continue

            seen.add(cleaned)
            result.append(cleaned)

        return result

    def _sorted_aura_items(
        self,
        user_aura_dict: dict[str, float] | None,
    ) -> list[tuple[str, float]]:
        """
        5축 아우라 점수를 높은 순서로 정렬합니다.
        """

        if not user_aura_dict or not isinstance(user_aura_dict, dict):
            return []

        items: list[tuple[str, float]] = []

        for axis in self.axes:
            value = user_aura_dict.get(axis)

            try:
                score = float(value)
            except (TypeError, ValueError):
                score = 0.0

            items.append((axis, score))

        return sorted(items, key=lambda x: x[1], reverse=True)

    def _get_main_family(self, user_aura_dict: dict[str, float]) -> str:
        """
        사용자 5축 아우라 중 가장 높은 계열을 반환합니다.
        """

        aura_items = self._sorted_aura_items(user_aura_dict)

        if not aura_items:
            return "프레시"

        return aura_items[0][0]

    def _score_to_percent(self, score: float) -> int:
        """
        cosine similarity score를 UI용 퍼센트로 변환합니다.
        """

        try:
            value = float(score)
        except (TypeError, ValueError):
            value = 0.0

        value = max(0.0, min(value, 0.98))

        return int(value * 100)

    def _extract_matches(self, search_response) -> list[Any]:
        """
        Pinecone SDK 응답이 객체/딕셔너리 형태 어느 쪽이어도 처리합니다.
        """

        if isinstance(search_response, dict):
            return search_response.get("matches", []) or []

        return getattr(search_response, "matches", []) or []

    def _extract_perfume_id(self, match) -> int | None:
        """
        Pinecone match에서 perfume_id를 추출합니다.
        metadata.perfume_id가 있으면 우선 사용하고,
        없으면 vector id를 사용합니다.
        """

        metadata = self._extract_metadata(match)

        perfume_id = metadata.get("perfume_id")

        if perfume_id is None:
            if isinstance(match, dict):
                perfume_id = match.get("id")
            else:
                perfume_id = getattr(match, "id", None)

        if perfume_id is None:
            return None

        try:
            return int(perfume_id)
        except (TypeError, ValueError):
            return None

    def _extract_score(self, match) -> float:
        """
        Pinecone match에서 similarity score를 추출합니다.
        """

        if isinstance(match, dict):
            return float(match.get("score", 0.0) or 0.0)

        return float(getattr(match, "score", 0.0) or 0.0)

    def _extract_metadata(self, match) -> dict[str, Any]:
        """
        Pinecone match에서 metadata를 추출합니다.
        """

        if isinstance(match, dict):
            metadata = match.get("metadata", {}) or {}
        else:
            metadata = getattr(match, "metadata", {}) or {}

        if isinstance(metadata, dict):
            return metadata

        return {}


# EOF: recommendation_service.py