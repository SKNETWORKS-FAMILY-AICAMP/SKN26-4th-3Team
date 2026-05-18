"""
@file recommendation_service.py
@role
RAG 검색과 5축 아우라 유사도 재정렬을 결합하여 최적의 향수를 선정하는 하이브리드 추천 엔진 서비스입니다.
Pinecone 벡터 검색, L2 기반 재랭킹, 가중치 합산 스코어링을 통해 고도로 개인화된 추천 결과를 생성합니다.
"""

# ----------------------------------------------------------------
# Update History
# 2026-05-16: 추천 로직에 벡터 검색 및 하이브리드 리랭킹을 추가 (worker: Gloveman)
# ----------------------------------------------------------------

import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Case, IntegerField, When
from perfumes.models import Perfume, PerfumeImage
from ..utils import load_user_preference_map, load_master_map, split_notes_heuristic


class RecommendationService:
    """
    [Hybrid Recommendation Engine]
    시각적 감성과 수치적 아우라를 통합 분석하여 개인화된 향수 추천을 제공하는 핵심 서비스 클래스입니다.
    """

    def __init__(self):
        self.master_map = load_master_map()
        self.axes = ["플로럴", "우디", "오리엔탈", "프레시", "구르망"]

        # Pinecone 및 RAG 설정 (환경 변수 기반)
        self.pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "olfit-perfumes")
        self.embedding_model = os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )
        self.rag_top_k = int(os.getenv("RAG_TOP_K", "30"))

    def recommend(self, user_aura_dict, query_text, selected_notes):
        """
        사용자의 아우라 프로필과 분석된 쿼리를 기반으로 최종 추천 리스트를 생성합니다.

        Args:
            user_aura_dict (dict): 사용자의 5축 아우라 점수 (L2 정규화 상태)
            query_text (str): VLM을 통해 분석된 이미지 요약 텍스트
            selected_notes (list): 사용자가 직접 선택한 선호 향기 성분 목록

        Returns:
            list: 가공된 추천 제품 정보 목록 (Top 5)
        """
        # [Step 1] 자연어 쿼리 보강 (Search Query Enrichment)
        enhanced_query = self._build_enhanced_rag_query(
            query_text, user_aura_dict, selected_notes
        )
        print(f"\n🔍 [RAG Query] {enhanced_query}")

        # [Step 2] RAG 후보군 추출 (Pinecone Semantic Search)
        rag_matches = self._search_pinecone(enhanced_query, top_k=self.rag_top_k)

        # Pinecone 검색 실패 시 DB 기반 Fallback 가동
        if not rag_matches:
            main_family = max(user_aura_dict, key=user_aura_dict.get)
            return self._fallback_recommend(main_family, user_aura_dict, selected_notes)

        # [Step 3] 하이브리드 재정렬 (Hybrid Re-ranking)
        user_vector = self._get_aura_vector(user_aura_dict)
        print(f"📊 [User Aura Vector] {user_vector}")

        target_notes_set = self._get_target_notes_set(selected_notes)

        pre_ranked_results = []
        for match in rag_matches:
            m = match.metadata
            if not m:
                continue

            # 개별 향수의 아우라 벡터 및 RAG 점수 추출
            p_vector = self._get_aura_vector(m)
            rag_score = float(match.score)
            raw_notes = m.get("representative_notes", [])

            # 통합 점수 산출 (Aura + RAG + Bonus)
            hybrid_data = self._compute_hybrid_score(
                user_vector, p_vector, rag_score, raw_notes, target_notes_set
            )

            pre_ranked_results.append(
                {
                    "id": int(m["perfume_id"]),
                    "name": m["korean_name"],
                    "metadata": m,
                    **hybrid_data,
                }
            )

        # 최종 하이브리드 점수 기준 내림차순 정렬
        top_5_raw = sorted(
            pre_ranked_results, key=lambda x: x["hybrid_score"], reverse=True
        )[:5]

        # [DEBUG] 상세 점수 내역 출력
        print("\n🏆 [Top 5 Hybrid Recommendations]")
        for i, res in enumerate(top_5_raw):
            print(
                f"  {i+1}. {res['name']} | Score: {res['hybrid_score']:.4f} (Aura:{res['aura_sim']:.4f}*0.5 + RAG:{res['rag_score']:.4f}*0.5 + Bonus:{res['note_bonus']:.2f})"
            )

        # [DEBUG] 1위 제품과의 대칭성 확인
        if top_5_raw:
            self._print_symmetry_check(enhanced_query, top_5_raw[0]["id"])

        # [Step 4] 선정된 제품의 이미지 상세 정보(Base64 등) 일괄 조회
        top_5_ids = [x["id"] for x in top_5_raw]
        images = self._get_images(top_5_ids)

        # [Step 5] 최종 응답 규격 포맷팅
        return self._build_final_response(
            top_5_raw, images, selected_notes, user_aura_dict
        )

    # ----------------------------------------------------------------
    # [Internal Scoring Helpers] - Logic unification
    # ----------------------------------------------------------------

    def _get_aura_vector(self, data_dict):
        """
        다양한 소스(DB 딕셔너리, Pinecone 메타데이터)로부터 정규화된 5축 벡터를 생성합니다.

        Args:
            data_dict (dict): 아우라 정보를 담은 딕셔너리

        Returns:
            np.array: L2 정규화된 5차원 NumPy 배열
        """
        # DB(한글 키)와 메타데이터(aura_ 접두사 영문 키) 모두 대응
        vector = np.array(
            [
                float(
                    data_dict.get(
                        "플로럴",
                        data_dict.get("플로랄", data_dict.get("aura_floral", 0.0)),
                    )
                ),
                float(data_dict.get("우디", data_dict.get("aura_woody", 0.0))),
                float(
                    data_dict.get(
                        "오리엔탈",
                        data_dict.get("앰버", data_dict.get("aura_amber", 0.0)),
                    )
                ),
                float(data_dict.get("프레시", data_dict.get("aura_fresh", 0.0))),
                float(data_dict.get("구르망", data_dict.get("aura_gourmand", 0.0))),
            ]
        )

        # 벡터 크기 확인 (L2 Norm)
        norm = np.linalg.norm(vector)
        # 0 벡터인 경우 균등 분포로 Fallback하여 연산 오류 방지
        return vector if norm > 0 else np.array([0.4472] * 5)

    def _get_target_notes_set(self, selected_notes):
        """
        사용자가 선택한 노트를 포함하여, 가산점 매칭 범위를 확장한 전체 노트 세트를 반환합니다.
        """
        pref_map = load_user_preference_map()
        target_notes = []
        for n in selected_notes:
            mapping = pref_map.get(n)
            target_notes.extend(mapping.get("expansion", [n]) if mapping else [n])
        return set(target_notes)

    def _compute_hybrid_score(
        self, user_vector, p_vector, rag_score, raw_notes, target_notes_set
    ):
        """
        코사인 유사도와 RAG 점수, 노트 보너스를 가중 합산하여 최종 점수를 도출합니다.

        Formula: (Aura Sim * 0.5) + (RAG Score * 0.5) + (Note Match Bonus)
        """
        # 1. Aura Similarity (수치적 일치도)
        aura_sim = cosine_similarity([user_vector], [p_vector])[0][0]

        # 2. Note Match Bonus (명시적 취향 가산점)
        # 선택한 성분이 제품에 포함되어 있을 경우 개당 0.03점, 최대 0.1점 부여
        matches_count = len(set(raw_notes) & target_notes_set)
        note_bonus = min(matches_count * 0.03, 0.1)

        # 3. Hybrid Score (가중 합산) - 5:5 밸런스 적용
        hybrid_score = (aura_sim * 0.5) + (rag_score * 0.5) + note_bonus

        return {
            "aura_sim": aura_sim,
            "rag_score": rag_score,
            "note_bonus": note_bonus,
            "hybrid_score": hybrid_score,
        }

    def _get_images(self, perfume_ids):
        """추천된 향수들의 이미지 객체를 DB에서 일괄 조회합니다."""
        return {
            img.perfume_detail.perfume_id: img
            for img in PerfumeImage.objects.filter(
                perfume_detail__perfume_id__in=perfume_ids
            ).select_related("perfume_detail")
        }

    def _print_symmetry_check(self, query, top_1_id):
        """1위 제품과 쿼리의 자연어 구조적 대칭성을 출력합니다 (디버깅용)."""
        try:
            from perfumes.models import PerfumeDetail

            detail = PerfumeDetail.objects.get(perfume_id=top_1_id)
            top_1_doc = detail.data.get("embedding_doc", "N/A")
            print(f"\n⚖️  [Symmetry Check - Top 1]")
            print(f"  > Query: {query}")
            print(f"  > Document: {top_1_doc}")
        except Exception:
            pass

    def _fallback_recommend(self, main_family, user_aura_dict, selected_notes):
        """
        Pinecone이나 OpenAI 장애 시 MySQL DB를 직접 조회하여 추천을 수행합니다.
        Main Family 필터링 후 실시간 아우라 매칭 연산을 수행합니다.
        """
        # 1차 필터링: 동일 계열 향수 추출
        candidates = Perfume.objects.filter(family=main_family).select_related(
            "brand", "detail"
        )[:50]
        if not candidates:
            candidates = Perfume.objects.select_related("brand", "detail")[:50]

        user_vector = self._get_aura_vector(user_aura_dict)
        target_notes_set = self._get_target_notes_set(selected_notes)

        fallback_results = []
        for p in candidates:
            p_data = p.detail.data or {}
            p_vector = self._get_aura_vector(p_data.get("aura_profile", {}))

            # RAG 점수 대신 중립 점수(0.5)를 사용하여 하이브리드 점수 산출
            hybrid_data = self._compute_hybrid_score(
                user_vector,
                p_vector,
                0.5,
                p_data.get("representative_notes", []),
                target_notes_set,
            )

            # _build_final_response 규격에 맞춘 가상 메타데이터 구성
            fallback_results.append(
                {
                    "id": p.id,
                    "metadata": {
                        "perfume_id": p.id,
                        "brand": p.brand.name,
                        "korean_name": p.korean_name,
                        "english_name": p.english_name,
                        "family": p.family,
                        "product_type": p.product_type,
                        "release_year": p.release_year or 0,
                        "price_raw": (
                            p_data.get("price", {}).get("raw", "정보없음")
                            if isinstance(p_data.get("price"), dict)
                            else str(p_data.get("price"))
                        ),
                        "price_krw": p_data.get("price_krw", 0),
                        "price_amount": (
                            p_data.get("price", {}).get("amount", 0)
                            if isinstance(p_data.get("price"), dict)
                            else 0
                        ),
                        "price_currency": (
                            p_data.get("price", {}).get("currency", "KRW")
                            if isinstance(p_data.get("price"), dict)
                            else "KRW"
                        ),
                        "volume": p_data.get("volume", "N/A"),
                        "image_url": p_data.get("image_url", ""),
                        "accords": p_data.get("accords", []),
                        "representative_notes": p_data.get("representative_notes", []),
                        "description": p_data.get("description", ""),
                        "top_notes": p_data.get("notes_parsed", {}).get("top", []),
                        "middle_notes": p_data.get("notes_parsed", {}).get(
                            "middle", []
                        ),
                        "base_notes": p_data.get("notes_parsed", {}).get("base", []),
                        "keywords": p_data.get("keywords", []),
                        **p_data.get("aura_profile", {}),
                    },
                    **hybrid_data,
                }
            )

        top_5_raw = sorted(
            fallback_results, key=lambda x: x["hybrid_score"], reverse=True
        )[:5]
        images = self._get_images([x["id"] for x in top_5_raw])
        return self._build_final_response(
            top_5_raw, images, selected_notes, user_aura_dict
        )

    # ----------------------------------------------------------------
    # [Response Formatting]
    # ----------------------------------------------------------------

    def _build_final_response(self, top_5_raw, images, selected_notes, user_aura_dict):
        """
        추천된 제품 리스트를 프론트엔드 AnalyzeResponseSerializer 규격에 맞게 가공합니다.
        이 과정에서 한글 번역 및 점수 퍼센트 변환이 이루어집니다.
        """
        note_trans = self.master_map.get("note_translations", {})
        target_notes_set = self._get_target_notes_set(selected_notes)

        final_results = []
        for item in top_5_raw:
            m = item["metadata"]
            p_id = item["id"]
            image_obj = images.get(p_id)

            def translate_list(notes):
                return [note_trans.get(n, n) for n in notes]

            # 피라미드 번역 적용
            translated_pyramid = {
                "top": translate_list(m.get("top_notes", [])),
                "middle": translate_list(m.get("middle_notes", [])),
                "base": translate_list(m.get("base_notes", [])),
            }

            # 전체 노트 리스트 및 매칭 성분 확인
            raw_notes = m.get("representative_notes", [])
            p_notes_list = translate_list(raw_notes)
            matches = set(raw_notes) & target_notes_set

            # UI 레이더용 유사도 (0~98% 범위로 안전하게 변환)
            hybrid_sim = int(min(item["hybrid_score"] * 100, 98))

            final_results.append(
                {
                    "id": p_id,
                    "name": m["korean_name"],
                    "brand": m["brand"],
                    "price": m["price_raw"],
                    "price_krw": int(m["price_krw"]),
                    "size": m["volume"],
                    "image": m["image_url"],
                    "perfume": {
                        "id": p_id,
                        "brand": m["brand"],
                        "koreanName": m["korean_name"],
                        "englishName": m["english_name"],
                        "productType": m["product_type"],
                        "family": m["family"],
                        "releaseYear": int(m.get("release_year", 0)),
                        "price": {
                            "raw": m["price_raw"],
                            "amount": float(m.get("price_amount", 0)),
                            "currency": m["price_currency"],
                        },
                        "description": m["description"],
                        "notes": p_notes_list,
                        "representativeNotes": p_notes_list,
                        "notesPyramid": translated_pyramid,
                        "accords": m.get("accords", []),
                        "keywords": {"ko": m.get("keywords", [])},
                        "auraProfile": {
                            "플로랄": m.get("aura_floral", m.get("플로랄", 0.4472)),
                            "우디": m.get("aura_woody", m.get("우디", 0.4472)),
                            "앰버": m.get("aura_amber", m.get("오리엔탈", 0.4472)),
                            "프레시": m.get("aura_fresh", m.get("프레시", 0.4472)),
                            "구르망": m.get("aura_gourmand", m.get("구르망", 0.4472)),
                        },
                        "volume": m["volume"],
                    },
                    "imageDetail": {
                        "url": m["image_url"],
                        "originalUrl": (
                            image_obj.original_url if image_obj else m["image_url"]
                        ),
                        "backendPath": image_obj.processed_path if image_obj else "",
                        "base64": image_obj.base64_data if image_obj else "",
                    },
                    "tags": m.get("accords", [])[:3],
                    "notes": ", ".join(p_notes_list[:5]),
                    "family": m["family"],
                    "category": "Personal",
                    "similarity": hybrid_sim,
                    "matchReason": self._generate_hybrid_reason(
                        matches,
                        m["family"],
                        hybrid_sim,
                        item["rag_score"],
                        selected_notes,
                        user_aura_dict,
                    ),
                    "details": {
                        "story": m["description"],
                        "topNotes": ", ".join(translated_pyramid["top"]),
                        "middleNotes": ", ".join(translated_pyramid["middle"]),
                        "baseNotes": ", ".join(translated_pyramid["base"]),
                        "bestFor": ", ".join(m.get("keywords", [])[:3]),
                    },
                }
            )
        return final_results

    def _build_enhanced_rag_query(self, query_text, user_aura_dict, selected_notes):
        """
        임베딩 모델이 잘 이해할 수 있는 자연어 쿼리를 생성합니다.
        '대칭형 검색'을 위해 인덱싱 문서와 문장 성분을 공유합니다.
        """
        parts = []
        if query_text:
            parts.append(query_text.strip())

        # 선호 노트 명시
        if selected_notes:
            parts.append(f"이용자는 {', '.join(selected_notes)} 향을 선호하며")

        # 아우라 무드 명시 (대칭성 확보의 핵심)
        top_axes = sorted(user_aura_dict.items(), key=lambda x: x[1], reverse=True)[:2]
        if top_axes:
            parts.append(
                f"{'와 '.join([a[0] for a in top_axes])} 분위기가 느껴지는 향수를 찾고 있습니다."
            )
        return " ".join(parts)

    def _search_pinecone(self, query_text, top_k=50):
        """
        OpenAI 임베딩 모델을 호출하여 쿼리를 벡터화한 뒤 Pinecone에서 상위 후보를 검색합니다.
        """
        openai_key, pinecone_key = os.getenv("OPENAI_API_KEY"), os.getenv(
            "PINECONE_API_KEY"
        )
        if not openai_key or not pinecone_key or not query_text:
            return []

        try:
            from openai import OpenAI
            from pinecone import Pinecone

            client, pc = OpenAI(api_key=openai_key), Pinecone(api_key=pinecone_key)
            index = pc.Index(self.pinecone_index_name)

            # OpenAI 3-small 임베딩 생성 (1536차원)
            query_vector = (
                client.embeddings.create(input=[query_text], model=self.embedding_model)
                .data[0]
                .embedding
            )

            # 벡터 검색 수행
            return index.query(
                vector=query_vector, top_k=top_k, include_metadata=True
            ).matches
        except Exception as e:
            print(f"[RAG Error] {e}")
            return []

    def _generate_hybrid_reason(
        self, matches, family, hybrid_sim, rag_score, selected_notes, user_aura_dict
    ):
        """
        사용자의 아우라와 취향을 종합적으로 분석하여 전문성 있는 추천 사유를 동적으로 생성합니다.
        'Dual Aura' 상황에 대응하는 조화로운 스토리텔링을 제공합니다.
        """
        sorted_user_axes = sorted(
            user_aura_dict.items(), key=lambda x: x[1], reverse=True
        )
        top_user_axis, second_user_axis = sorted_user_axes[0][0], (
            sorted_user_axes[1][0] if len(sorted_user_axes) > 1 else None
        )
        # 상위 2개 축의 점수 차이가 0.05 이내면 듀얼 아우라로 간주
        is_dual = second_user_axis and (
            sorted_user_axes[0][1] - sorted_user_axes[1][1] < 0.05
        )

        reasons = []

        # 1. 아우라/무드 매칭 섹션
        if is_dual:
            reasons.append(
                f"당신은 #[{top_user_axis}]의 매력과 #[{second_user_axis}]의 감성을 동시에 지니셨네요. 이 두 분위기를 조화롭게 잇는 {family} 향기를 제안합니다."
            )
        elif family == top_user_axis:
            reasons.append(
                f"분석 결과 당신의 #[{family}] 아우라와 완벽하게 공명하는 향기입니다."
            )
        else:
            reasons.append(
                f"당신의 #[{top_user_axis}] 아우라에 {family}의 세련된 뉘앙스를 더해줄 최적의 선택입니다."
            )

        # 2. 성분/취향 매칭 섹션
        if matches:
            reasons.append(
                f"특히 선호하시는 #[{', '.join(list(matches)[:2])}] 성분이 이 제품의 핵심 정체성을 완성하고 있습니다."
            )
        elif selected_notes:
            reasons.append(
                f"선택하신 #[{', '.join(selected_notes[:2])}] 향기의 감성을 가장 현대적으로 재해석하여 담아냈습니다."
            )

        # 3. 스타일/이미지 완성도 섹션
        if rag_score > 0.85:
            reasons.append(
                f"이미지에서 느껴지는 독보적인 무드를 {hybrid_sim}%의 높은 일치율로 완벽히 스타일링해 드립니다."
            )
        else:
            reasons.append(
                f"전체적인 스타일 조화도가 {hybrid_sim}%로 매우 높아, 당신의 고유한 분위기를 돋보이게 합니다."
            )

        return " ".join(reasons)


# EOF: recommendation_service.py
