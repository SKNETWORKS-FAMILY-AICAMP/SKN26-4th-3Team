"""
@file recommendation_service.py
@module Perfumes/Services/RecommendationService
@description
데이터베이스에 적재된 향수 데이터를 기반으로 유사도 기반 추천을 수행합니다.
5축 아우라 유사도와 명시적 취향 매칭 가중치를 결합한 하이브리드 재랭킹 엔진입니다.

@author Olfít AI Team
@version 4.0.0
"""

import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
from perfumes.models import Perfume
from ..utils import load_preference_expansion, load_master_map

class RecommendationService:
    """
    [Hybrid Re-ranking Engine]
    MySQL의 메타데이터와 벡터 유사도를 결합하여 최적의 Top 5 향수를 선별합니다.
    """
    
    def __init__(self):
        self.master_map = load_master_map()
        self.axes = ["플로럴", "우디", "오리엔탈", "프레시", "구르망"]
        
        # [Pricing] 오늘 기준 환율 설정 (정렬용)
        self.exchange_rates = {
            "USD": 1380, "EUR": 1490, "GBP": 1730, "KRW": 1
        }

    def recommend(self, user_aura_dict, query_text, selected_notes):
        """
        사용자 아우라 벡터와 취향을 기반으로 맞춤형 향수를 추천합니다.
        
        @param user_aura_dict: 사용자의 5축 아우라 점수 딕셔너리
        @param query_text: RAG 검색용 쿼리 문장 (향후 벡터 검색 확장 포인트)
        @param selected_notes: 사용자가 선택한 성분 리스트
        @return: 정렬된 Top 5 향수 결과 리스트
        """
        main_family = max(user_aura_dict, key=user_aura_dict.get)
        
        # [Step 1] 1차 필터링: 메인 계열 기반 후보군 추출 (DB 최적화)
        # TODO: 향후 이 단계를 Pinecone 벡터 검색(Semantic Search)으로 교체 예정
        candidates = Perfume.objects.filter(family=main_family).select_related('brand')[:100]
        
        if candidates.count() < 20:
            candidates = Perfume.objects.all().select_related('brand')[:100]

        # 사용자 아우라 벡터화
        user_aura_vector = np.array([user_aura_dict.get(a, 0.2) for a in self.axes])
        
        # 취향 성분 확장 매핑 로드 (ex: '우드' 선택 시 '샌달우드', '시더우드' 등 매칭)
        expansion_map = load_preference_expansion()
        target_notes = []
        for n in selected_notes:
            target_notes.extend(expansion_map.get(n, [n]))
        target_notes = set(target_notes)
        
        ranked_results = []
        for p in candidates:
            # DB JSON 필드에서 상세 정보 및 사전 계산된 아우라 로드
            p_data = p.data
            p_aura = p_data.get('aura_profile')
            
            if not p_aura:
                p_aura = self._calculate_aura_on_the_fly(p_data.get('notes', []))
            
            p_vector = np.array([p_aura.get(a, 0.2) for a in self.axes])
            
            # [Step 2] 유사도 및 가중치 계산
            # A. 아우라 코사인 유사도 (70%)
            aura_sim = cosine_similarity([user_aura_vector], [p_vector])[0][0]
            
            # B. 취향 성분 포함 여부 가산점 (30%)
            p_notes = set(p_data.get('representative_notes') or p_data.get('notes', []))
            matches = p_notes & target_notes
            pref_boost = len(matches) * 0.1
            
            # 최종 스코어 합산
            final_score = (aura_sim * 0.7) + (min(pref_boost, 0.3))
            similarity_percent = int(min(final_score * 100, 98))
            
            # 원화 환산 가격 계산 (정렬용)
            price_krw = self._convert_to_krw(p_data.get("price"))
            
            ranked_results.append({
                "id": p.id,
                "name": p.korean_name,
                "brand": p.brand.name,
                "price": p_data.get("price", {}).get("raw", "정보없음"),
                "price_krw": price_krw,
                "size": p_data.get("volume", "N/A"),
                "image": p_data.get("image_url", ""),
                "tags": p_data.get("accords", [])[:3],
                "notes": ", ".join((p_data.get("representative_notes") or p_data.get("notes", []))[:5]),
                "family": p.family,
                "category": "Personal",
                "similarity": similarity_percent,
                "matchReason": self._generate_reason(matches, main_family),
                "details": {
                    "story": p_data.get("description", ""),
                    "topNotes": ", ".join(p_data.get("notes_parsed", {}).get("top", [])),
                    "middleNotes": ", ".join(p_data.get("notes_parsed", {}).get("middle", [])),
                    "baseNotes": ", ".join(p_data.get("notes_parsed", {}).get("base", [])),
                    "bestFor": ", ".join(p_data.get("keywords", [])[:3])
                }
            })
            
        # 유사도 내림차순 정렬 후 상위 5개 반환
        return sorted(ranked_results, key=lambda x: x['similarity'], reverse=True)[:5]

    def _convert_to_krw(self, price_data):
        """다양한 통화의 가격을 원화로 환산합니다."""
        if not price_data or not isinstance(price_data, dict): return 0
        amount = price_data.get("amount", 0)
        currency = price_data.get("currency", "KRW").upper()
        rate = self.exchange_rates.get(currency, 1350)
        return int(amount * rate)

    def _calculate_aura_on_the_fly(self, notes):
        """DB에 점수가 없을 경우 성분 리스트로부터 실시간 아우라를 산출합니다."""
        scores = {axis: 0.0 for axis in self.axes}
        for n in notes:
            ko_note = self.master_map["note_translations"].get(n, n)
            sub_accord = self.master_map["note_to_accord"].get(ko_note, "아로마틱")
            category = self.master_map["accord_to_category"].get(sub_accord, "기타")
            if category in scores: scores[category] += 1.0
        
        max_s = max(scores.values()) if scores.values() else 0
        if max_s == 0: return {a: 0.2 for a in self.axes}
        return {k: round(v / max_s, 2) for k, v in scores.items()}

    def _generate_reason(self, matches, main_family):
        """사용자에게 보여줄 매칭 사유 문구를 생성합니다."""
        if matches:
            match_str = ", ".join(list(matches)[:2])
            return f"선택하신 #{match_str} 성분이 포함되어 있으며, 당신의 #{main_family} 아우라와 완벽하게 조화됩니다."
        return f"당신의 분위기를 결정짓는 #{main_family} 계열의 베스트 추천 향수입니다."

# EOF: recommendation_service.py
