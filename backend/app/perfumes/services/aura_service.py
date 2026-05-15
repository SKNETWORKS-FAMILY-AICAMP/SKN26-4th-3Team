"""
aura_service.py
---------------
사용자의 시각적 결과(VLM)와 명시적 취향(Selected Notes)을 결합하여
통합적인 '향기 아우라'를 계산하고, RAG 검색을 위한 한글 쿼리를 생성한다.

역할:
1. 비전 분석 결과(VLM)와 사용자 선호도(Selected Notes)를 다차원 벡터 공간에서 융합.
2. 5축(플로럴, 우디, 오리엔탈, 프레시, 구르망) 아우라 스코어 산출.
3. UI 시각화를 위한 레이더 차트용 점수(Radar Scores) 스케일링.
4. RAG 검색 및 UI 표시를 위한 대칭형 한글 쿼리 생성.

중요:
- 시각 정보(60%)와 사용자 취향(40%)의 가중치를 적용하여 벡터 융합.
- 계열별 현실적 최대 기대 점수(Ref Max)를 사용하여 UI 레이더 차트의 선명도 확보.
- RAG 쿼리는 태그 기반 구조화 데이터와 자연스러운 문장을 모두 포함.
"""

import numpy as np
from ..utils import load_master_map, load_user_preference_map
from scent_engine import map_image_to_fragrance_keywords


class AuraService:
    """
    [Aura Scoring & Query Generation Service]
    비전 분석 결과와 사용자 선호도를 다차원 벡터 공간에서 융합합니다.
    """

    def __init__(self):
        self.master_map = load_master_map()
        self.pref_map = load_user_preference_map()
        self.axes = ["플로럴", "우디", "오리엔탈", "프레시", "구르망"]
        self.family_mapping = {
            "FLORAL": "플로럴",
            "WOODY": "우디",
            "AMBERY": "오리엔탈",
            "FRESH": "프레시",
            "GOURMAND": "구르망",
        }
        # 계열별 현실적 최대 기대 점수 (Ref Max)
        # 플로럴(10.0), 우디(7.0), 오리엔탈(7.0), 프레시(10.0), 구르망(4.0)
        self.ref_max = np.array([10.0, 7.0, 7.0, 10.0, 4.0])

    def calculate_combined_aura(self, vl_result, selected_notes):
        """
        비전 결과와 사용자 노트를 결합하여 통합 아우라 리포트를 생성합니다.

        @param vl_result: VLEngine.analyze_image()의 결과 딕셔너리
        @param selected_notes: 사용자가 프론트엔드에서 선택한 향기 성분 리스트
        @return: (radar_scores, fragrance_mapping, query_text, readable_query, search_vector_dict)
        """
        # [Step 1] 매퍼 로직 실행: 시각 키워드를 향수 키워드로 변환
        fragrance_mapping = map_image_to_fragrance_keywords(vl_result)

        # [Step 2] 시각 벡터 산출 (60% 비중)
        visual_vector = self._holistic_score_aggregation(fragrance_mapping)

        # [Step 3] 취향 벡터 산출 (40% 비중)
        pref_vector = self._get_preference_vector(selected_notes)

        # [Step 4] 벡터 융합 및 정규화
        combined_raw = (visual_vector * 0.6) + (pref_vector * 0.4)

        # [Step 5] 시각화용 및 추천 연산용 벡터 분리
        # UI 레이더 차트용 (현실적 최대치 기반 스케일링)
        radar_scores = self._scale_to_visualize(combined_raw)

        # 추천 서비스 연산용 (L2 정규화)
        norm = np.linalg.norm(combined_raw)
        search_vector = combined_raw / norm if norm > 0 else combined_raw
        search_vector_dict = {
            axis: float(round(val, 4)) for axis, val in zip(self.axes, search_vector)
        }

        # [Step 6] 대칭형 쿼리 생성 (RAG 및 UI용)
        query_text, readable_query = self._generate_symmetric_korean_query(
            vl_result, fragrance_mapping, search_vector_dict, selected_notes
        )

        return (
            radar_scores,
            fragrance_mapping,
            query_text,
            readable_query,
            search_vector_dict,
        )

    def _scale_to_visualize(self, vector):
        """
        UI Radar Chart를 위한 현실적 최대치(Ref Max) 기반 스케일링.
        개성을 선명하게 보여주면서도 절대적 강도를 보존합니다.
        """
        if np.max(vector) == 0:
            return {axis: 0.1 for axis in self.axes}

        # 각 축의 현실적 최대치 대비 비율 계산
        scaled = vector / self.ref_max

        # 시각적 피드백을 위해 가장 큰 축이 최소 0.8 이상이 되도록 부스팅 (선택 사항)
        # max_ratio = np.max(scaled)
        # if 0 < max_ratio < 0.8:
        #     scaled = scaled * (0.8 / max_ratio)

        return {
            axis: float(round(np.clip(val, 0.1, 1.0), 2))
            for axis, val in zip(self.axes, scaled)
        }

    def _holistic_score_aggregation(self, mapping):
        """비전 매핑 결과를 5축 점수로 집계합니다."""
        scores = {axis: 0.0 for axis in self.axes}
        raw_scores = mapping.get("scores", {})

        # 계열별 가중치 합산
        for item in raw_scores.get("families", []):
            std_fam = self.family_mapping.get(item["name"])
            if std_fam in scores:
                scores[std_fam] += item["score"]

        # 어코드 및 성분 기반 미세 보정
        for item in raw_scores.get("subs", []):
            # 영문 어코드명을 한글로 변환 (예: 'Floral' -> '플로럴')
            ko_accord = self.master_map["accord_translations"].get(item["name"], item["name"])
            cat = self.master_map["accord_to_category"].get(ko_accord)
            if cat in scores:
                scores[cat] += item["score"] * 0.7

        for item in raw_scores.get("components_ko", []):
            # 이미 한글로 변환된 성분명이므로 직접 어코드 매핑 확인
            sub_accord = self.master_map["note_to_accord"].get(item["name"], "아로마틱")
            cat = self.master_map["accord_to_category"].get(sub_accord)
            if cat in scores:
                scores[cat] += item["score"] * 0.5

        return np.array([scores[a] for a in self.axes])

    def _get_preference_vector(self, selected_notes):
        """사용자가 직접 선택한 노트를 5축 벡터로 변환합니다."""
        scores = {axis: 0.0 for axis in self.axes}
        for note in selected_notes:
            # 선호도 매핑에서 직접 계열(axis) 정보를 가져옴
            mapping = self.pref_map.get(note)
            if mapping and mapping["axis"] in scores:
                scores[mapping["axis"]] += 3.0  # 명시적 선택에는 높은 가중치 부여
        return np.array([scores[a] for a in self.axes])

    def _generate_symmetric_korean_query(
        self, vl_result, fragrance_mapping, aura_score, selected_notes
    ):
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


# EOF: aura_service.py
