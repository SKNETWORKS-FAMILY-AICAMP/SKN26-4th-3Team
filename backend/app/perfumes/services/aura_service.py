"""
@file aura_service.py
@module Perfumes/Services/AuraService
@description
사용자의 시각적 결과(VLM)와 명시적 취향(Selected Notes)을 결합하여
통합적인 '향기 아우라'를 계산하고, RAG 검색을 위한 한글 쿼리를 생성합니다.

@author Olfít AI Team
@version 4.0.0
"""

import numpy as np
from ..utils import load_master_map
from scent_engine import map_image_to_fragrance_keywords

class AuraService:
    """
    [Aura Scoring & Query Generation Service]
    비전 분석 결과와 사용자 선호도를 다차원 벡터 공간에서 융합합니다.
    """
    
    def __init__(self):
        self.master_map = load_master_map()
        self.axes = ["플로럴", "우디", "오리엔탈", "프레시", "구르망"]
        self.family_mapping = {
            "FLORAL": "플로럴", "WOODY": "우디", "AMBERY": "오리엔탈", 
            "FRESH": "프레시", "GOURMAND": "구르망"
        }

    def calculate_combined_aura(self, vl_result, selected_notes):
        """
        비전 결과와 사용자 노트를 결합하여 통합 아우라 리포트를 생성합니다.
        
        @param vl_result: VLEngine.analyze_image()의 결과 딕셔너리
        @param selected_notes: 사용자가 프론트엔드에서 선택한 향기 성분 리스트
        @return: (radar_scores, fragrance_mapping, query_text, readable_query)
        """
        # [Step 1] 매퍼 로직 실행: 시각 키워드를 향수 키워드로 변환
        fragrance_mapping = map_image_to_fragrance_keywords(vl_result)
        
        # [Step 2] 시각 벡터 산출 (60% 비중)
        visual_vector = self._holistic_score_aggregation(fragrance_mapping)
        
        # [Step 3] 취향 벡터 산출 (40% 비중)
        pref_vector = self._get_preference_vector(selected_notes)
        
        # [Step 4] 벡터 융합 및 정규화
        combined = (visual_vector * 0.6) + (pref_vector * 0.4)
        radar_scores = self._normalize_to_dict(combined)
        
        # [Step 5] 대칭형 쿼리 생성 (RAG 및 UI용)
        query_text, readable_query = self._generate_symmetric_korean_query(vl_result, fragrance_mapping, radar_scores, selected_notes)
        
        return radar_scores, fragrance_mapping, query_text, readable_query

    def _holistic_score_aggregation(self, mapping):
        """비전 매핑 결과를 5축 점수로 집계합니다."""
        scores = {axis: 0.0 for axis in self.axes}
        raw_scores = mapping.get("scores", {})

        # 계열별 가중치 합산
        for item in raw_scores.get("families", []):
            std_fam = self.family_mapping.get(item["name"])
            if std_fam in scores: scores[std_fam] += item["score"]

        # 어코드 및 성분 기반 미세 보정
        for item in raw_scores.get("subs", []):
            cat = self.master_map["accord_to_category"].get(item["name"])
            if cat in scores: scores[cat] += item["score"] * 0.7

        for item in raw_scores.get("components_ko", []):
            sub_accord = self.master_map["note_to_accord"].get(item["name"], "아로마틱")
            cat = self.master_map["accord_to_category"].get(sub_accord)
            if cat in scores: scores[cat] += item["score"] * 0.5

        return np.array([scores[a] for a in self.axes])

    def _get_preference_vector(self, selected_notes):
        """사용자가 직접 선택한 노트를 5축 벡터로 변환합니다."""
        scores = {axis: 0.0 for axis in self.axes}
        for note in selected_notes:
            sub_accord = self.master_map['note_to_accord'].get(note, "아로마틱")
            category = self.master_map['accord_to_category'].get(sub_accord, "프레시")
            if category in scores:
                scores[category] += 2.0 # 명시적 선택에는 높은 가중치 부여
        return np.array([scores[a] for a in self.axes])

    def _generate_symmetric_korean_query(self, vl_result, fragrance_mapping, aura_score, selected_notes):
        """RAG 검색을 위한 100% 한글 대칭형 쿼리를 생성합니다."""
        summary = vl_result.get("visual_summary", "분위기 있는 이미지")
        en_moods = vl_result.get("mood", [])
        ko_moods = [self.master_map["accord_translations"].get(m, m) for m in en_moods]
        
        analyzed_notes = fragrance_mapping.get("components_ko", [])
        combined_notes = list(dict.fromkeys(analyzed_notes + selected_notes))
        
        main_family = max(aura_score, key=aura_score.get)
        
        # [UI 표시용] 자연스러운 한글 문장
        readable = f"{summary}. {', '.join(ko_moods)} 분위기의 {', '.join(combined_notes)} 향이 느껴지는 {main_family} 계열 향수."
        
        # [RAG 검색용] 태그 기반 구조화 쿼리
        rag_query = f"visual_summary:{summary} "
        rag_query += " ".join([f"visual_mood:{m}" for m in ko_moods]) + " "
        rag_query += " ".join([f"fragrance_note_ko:{n}" for n in combined_notes]) + " "
        rag_query += f"fragrance_family:{main_family}"
        
        return rag_query, readable

    def _normalize_to_dict(self, vector):
        """내부 계산(1.0 합계)과 UI 시각화(스케일 업)를 위한 이중 정규화"""
        total_s = np.sum(vector)
        if total_s == 0: return {a: 0.2 for a in self.axes}
        
        normalized = vector / total_s
        # UI 레이더 차트용 스케일 업 (최대 1.0)
        visual_scaled = np.clip(normalized * 2.8, 0.1, 1.0)
        
        return {axis: float(round(val, 2)) for axis, val in zip(self.axes, visual_scaled)}

# EOF: aura_service.py
