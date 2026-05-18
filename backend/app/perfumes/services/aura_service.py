"""
@file aura_service.py
@role
사용자의 시각적 분석 결과(VLM)와 명시적 취향(Selected Notes)을 융합하여 '향기 아우라(Aura)'를 산출하는 서비스입니다.
시각/취향 벡터 융합, 5축 레이더 차트 점수 계산, 그리고 RAG 검색을 위한 정교한 자연어 쿼리 생성을 담당합니다.
"""

# ----------------------------------------------------------------
# Update History
# 2026-05-16: 기존의 구조화된 rag_query 대신, 자연스러운 문장의 query만을 구성하여 반환하도록 수정 (worker: Gloveman)
# ----------------------------------------------------------------

import numpy as np
from ..utils import load_master_map, load_user_preference_map
from scent_engine import map_image_to_fragrance_keywords


class AuraService:
    """
    [User Aura Analysis & Mapping Engine]
    사용자의 스타일 이미지를 수치화된 향기 프로필로 변환하는 핵심 엔진입니다.
    """

    def __init__(self):
        """서비스 초기화 및 공통 매핑 데이터 로드"""
        self.master_map = load_master_map()
        self.pref_map = load_user_preference_map()
        self.axes = ["플로럴", "우디", "오리엔탈", "프레시", "구르망"]

        # 내부 영문 상수와 시스템 한글 명칭 매핑
        self.family_mapping = {
            "FLORAL": "플로럴",
            "WOODY": "우디",
            "AMBERY": "오리엔탈",
            "FRESH": "프레시",
            "GOURMAND": "구르망",
        }

        # 계열별 현실적 최대 기대 점수 (Ref Max Scaling용)
        # 플로럴(10.0), 우디(7.0), 오리엔탈(7.0), 프레시(10.0), 구르망(4.0)
        # 각 계열의 성분 노출 빈도와 난이도를 고려한 수치입니다.
        self.ref_max = np.array([10.0, 7.0, 7.0, 10.0, 4.0])

    def calculate_combined_aura(self, vl_result, selected_notes):
        """
        VLM 분석 결과와 사용자 선택 노트를 결합하여 최종 아우라 프로필을 생성합니다.

        Args:
            vl_result (dict): VLEngine에서 생성된 시각 분석 JSON 데이터
            selected_notes (list): 사용자가 UI에서 선택한 한글 노트 명칭 리스트

        Returns:
            tuple: (radar_scores, fragrance_mapping, query_text, search_vector_dict)
        """
        # [Step 1] Vision-to-Scent Mapping
        # 시각적 키워드(예: 'blue', 'ocean')를 향수 도메인 속성으로 변환합니다.
        fragrance_mapping = map_image_to_fragrance_keywords(vl_result)

        # [Step 2] Visual Score Aggregation (60% weight)
        # 이미지 분석을 통해 도출된 원천 점수들을 5개 축으로 집계합니다.
        visual_vector = self._holistic_score_aggregation(fragrance_mapping)

        # [Step 3] Preference Score Aggregation (40% weight)
        # 사용자가 직접 선택한 향기 성분들에 대해 강력한 가중치를 부여한 벡터를 생성합니다.
        pref_vector = self._get_preference_vector(selected_notes)

        # [Step 4] Vector Fusion
        # 시각적 감성(객관적 스타일)과 성분 취향(주관적 선호)을 통합합니다.
        combined_raw = (visual_vector * 0.6) + (pref_vector * 0.4)

        # [Step 5] Separation for UI and Search

        # 5-1. UI 레이더 차트용 점수 (Ref Max Scaling)
        # 사용자에게 직관적인 그래프를 보여주기 위해 계열별 난이도를 반영하여 스케일링합니다.
        radar_scores = self._scale_to_visualize(combined_raw)

        # 5-2. 추천 엔진용 벡터 (L2 Normalization)
        # 코사인 유사도 연산의 신뢰도를 위해 벡터 크기를 1로 맞춥니다.
        norm = np.linalg.norm(combined_raw)
        search_vector = combined_raw / norm if norm > 0 else combined_raw
        search_vector_dict = {
            axis: float(round(val, 4)) for axis, val in zip(self.axes, search_vector)
        }

        # [Step 6] Symmetric Query Generation
        # 향수 인덱싱 문서와 대칭을 이루는 고품질 자연어 쿼리를 생성합니다.
        query_text = self._generate_symmetric_korean_query(
            vl_result, fragrance_mapping, search_vector_dict, selected_notes
        )

        return (
            radar_scores,
            fragrance_mapping,
            query_text,
            search_vector_dict,
        )

    def _scale_to_visualize(self, vector):
        """
        사용자 경험(UX)을 고려하여 아우라 수치를 0.1~1.0 사이로 스케일링합니다.

        Args:
            vector (np.array): 결합된 원천 점수 벡터

        Returns:
            dict: 레이더 차트 표시용 5축 점수
        """
        if np.max(vector) == 0:
            return {axis: 0.1 for axis in self.axes}

        # 축별 현실적 최대치(ref_max) 대비 비율로 변환
        scaled = vector / self.ref_max

        # 하한값 0.1, 상한값 1.0으로 클램핑하여 시각적 안정성 확보
        return {
            axis: float(round(np.clip(val, 0.1, 1.0), 2))
            for axis, val in zip(self.axes, scaled)
        }

    def _holistic_score_aggregation(self, mapping):
        """
        매핑된 향수 속성(Family, Sub, Component)들을 가중 합산하여 5축 점수를 산출합니다.

        Weighting Policy:
        - Primary Families: 100% 반영
        - Secondary Sub-accords: 70% 반영 (뉘앙스 보정)
        - Tertiary Components: 50% 반영 (미세 보정)
        """
        scores = {axis: 0.0 for axis in self.axes}
        raw_scores = mapping.get("scores", {})

        # 1. 메인 계열 점수 합산
        for item in raw_scores.get("families", []):
            std_fam = self.family_mapping.get(item["name"])
            if std_fam in scores:
                scores[std_fam] += item["score"]

        # 2. 서브 어코드 점수 합산 (가중치 0.7)
        for item in raw_scores.get("subs", []):
            # 영문 어코드명을 한글로 변환 (예: 'Floral' -> '플로럴')
            ko_accord = self.master_map["accord_translations"].get(
                item["name"], item["name"]
            )
            cat = self.master_map["accord_to_category"].get(ko_accord)
            if cat in scores:
                scores[cat] += item["score"] * 0.7

        # 3. 세부 성분 점수 합산 (가중치 0.5)
        for item in raw_scores.get("components_ko", []):
            # 이미 한글로 변환된 성분명이므로 직접 어코드 매핑 확인
            # 노트 -> 어코드 -> 카테고리 순으로 재귀적 매핑 탐색
            sub_accord = self.master_map["note_to_accord"].get(item["name"], "아로마틱")
            cat = self.master_map["accord_to_category"].get(sub_accord)
            if cat in scores:
                scores[cat] += item["score"] * 0.5

        return np.array([scores[a] for a in self.axes])

    def _get_preference_vector(self, selected_notes):
        """
        사용자가 선택한 노트(취향)를 강력한 수치 데이터로 변환합니다.

        Args:
            selected_notes (list): 사용자가 직접 고른 향기 성분 리스트

        Returns:
            np.array: 취향 지향점이 반영된 5축 벡터
        """
        scores = {axis: 0.0 for axis in self.axes}
        for note in selected_notes:
            # 선호도 매핑 테이블에서 해당 성분의 메인 축(axis) 정보를 직접 조회
            mapping = self.pref_map.get(note)
            if mapping and mapping["axis"] in scores:
                # 명시적 선택 성분에는 +3.0의 높은 가중치를 주어 추천 결과에 큰 영향을 미치게 함
                scores[mapping["axis"]] += 3.0

        return np.array([scores[a] for a in self.axes])

    def _generate_symmetric_korean_query(
        self, vl_result, fragrance_mapping, aura_score, selected_notes
    ):
        """
        RAG 성능을 위해 인덱싱 문서(Document)와 문장 구조가 대칭을 이루는 쿼리를 생성합니다.

        Structure: [이미지 요약]. [무드] 분위기의 [통합 노트] 향이 느껴지는 [메인 계열] 계열 향수.
        """
        summary = vl_result.get("visual_summary", "분위기 있는 이미지")

        # 이미지 무드 영문 태그를 한글 번역본으로 치환
        en_moods = vl_result.get("mood", [])
        ko_moods = [self.master_map["accord_translations"].get(m, m) for m in en_moods]

        # 분석된 성분과 선택한 성분을 합치고 중복 제거
        analyzed_notes = fragrance_mapping.get("components_ko", [])
        combined_notes = list(dict.fromkeys(analyzed_notes + selected_notes))

        # 현재 점수 중 가장 지배적인 계열(Main Family) 추출
        main_family = max(aura_score, key=aura_score.get)

        # [Symmetric RAG Strategy]
        # 인덱싱 문서의 "std_accords 분위기의 std_notes 향이 느껴지는 family 계열 향수" 문장 구조와
        # 동일한 구조로 임베딩 모델의 매칭 확률을 극대화합니다.
        readable = f"{summary}. {', '.join(ko_moods)} 분위기의 {', '.join(combined_notes)} 향이 느껴지는 {main_family} 계열 향수."

        return readable


# EOF: aura_service.py
