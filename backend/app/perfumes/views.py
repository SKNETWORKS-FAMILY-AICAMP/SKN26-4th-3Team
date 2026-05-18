"""
@file views.py
@module Perfumes/Views
@description
Olfít Connect의 핵심 비즈니스 로직을 API 엔드포인트로 노출합니다.
사용자의 요청을 받아 VLM 분석, 아우라 스코어링, 하이브리드 추천 프로세스를 오케스트레이션합니다.

@author Olfít AI Team
@version 4.9.0
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from scent_engine import VLEngine
from .services.aura_service import AuraService
from .services.recommendation_service import RecommendationService
from .serializers import (
    AnalyzeRequestSerializer,
    AnalyzeResponseSerializer,
    ErrorResponseSerializer,
)


class AnalyzeView(APIView):
    """
    [Main Analysis Endpoint]
    POST /api/analyze/
    사용자가 업로드한 이미지와 선택한 향 노트를 기반으로 통합 향수 추천 리포트를 생성합니다.
    """

    @extend_schema(
        operation_id="analyzePersonalScent",
        summary="이미지와 선호 노트 기반 향수 추천 분석",
        description=(
            "1. VLM을 통한 이미지 시각 감성 분석\n"
            "2. 5축 아우라 점수 산출 및 L2 정규화\n"
            "3. RAG + Aura Re-ranking 기반 하이브리드 추천\n"
            "4. 개인화된 추천 사유 및 리포트 데이터 반환"
        ),
        request=AnalyzeRequestSerializer,
        parameters=[
            OpenApiParameter(
                name="X-Session-ID",
                type=str,
                location=OpenApiParameter.HEADER,
                required=True,
                description="개인정보 동의 이후 발급된 익명 세션 ID입니다.",
            ),
        ],
        responses={
            200: AnalyzeResponseSerializer,
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="세션 ID 누락 또는 잘못된 요청입니다.",
            ),
        },
    )
    def post(self, request):
        """
        분석 요청을 처리하고 추천 결과를 반환합니다.
        """
        # [Security] 익명 세션 ID 확인 (Handshake 검증)
        session_id = request.headers.get("X-Session-ID")
        print(f"\n🚨 [Analyze API] Session: {session_id}")

        if not session_id:
            return Response(
                {
                    "error": "세션 ID가 누락되었습니다. 개인정보 동의 후 다시 시도해주세요."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 요청 데이터 추출 (Base64 이미지 및 선택된 노트 목록)
        image_base64 = request.data.get("image")
        selected_notes = request.data.get("selectedNotes", [])

        # --------------------------------------------------------
        # 1. 서비스 엔진 초기화
        # --------------------------------------------------------
        vl_engine = VLEngine()  # Vision-Language Engine (NVIDIA NIM)
        aura_service = AuraService()  # Scoring & Query Generation Service
        recommend_service = RecommendationService()  # Hybrid Recommendation Engine

        # --------------------------------------------------------
        # 2. [VLM Stage] 실시간 시각 감성 분석
        # 이미지에서 색상, 사물, 무드 등 핵심 키워드를 추출합니다.
        # --------------------------------------------------------
        print(f"[STEP 1] 🚀 Starting Live VLM Analysis...")
        vl_result = vl_engine.analyze_image(image_base64)
        print(f"[STEP 2] 📝 VLM Summary: {vl_result.get('visual_summary')}")

        # --------------------------------------------------------
        # 3. [Scoring Stage] 5축 아우라 계산 및 대칭 쿼리 생성
        # 시각 분석 결과와 사용자 취향을 융합하여 수치적 아우라와 RAG 쿼리를 생성합니다.
        # --------------------------------------------------------
        print("[STEP 3] 📊 Calculating Aura Scores & Generating Query...")
        # (v4.9 수정): readable_query 통합으로 4개 요소만 언패킹
        radar_scores, fragrance_mapping, query_text, aura_vectors = (
            aura_service.calculate_combined_aura(vl_result, selected_notes)
        )

        # --------------------------------------------------------
        # 4. [Recommendation Stage] 하이브리드 재랭킹 추천 (Top 5)
        # RAG 검색 결과에 아우라 유사도와 노트 가산점을 더해 최적의 향수를 선정합니다.
        # --------------------------------------------------------
        print("[STEP 4] 🎯 Fetching Hybrid Recommendations...")
        recommendations = recommend_service.recommend(
            aura_vectors, query_text, selected_notes
        )

        rec_names = [r["name"] for r in recommendations]
        print(f"[STEP 5] ✅ Final Recommendations: {', '.join(rec_names)}")
        print(f"--- Analysis for Session {session_id} Complete ---\n")

        # --------------------------------------------------------
        # 5. [UI Mapping] 프론트엔드 명칭 치환 및 데이터 가공
        # 도메인 명칭(오리엔탈)을 UI 명칭(앰버)으로 변환합니다.
        # --------------------------------------------------------
        ui_radar_scores = {
            "플로랄": radar_scores.get("플로럴", 0),
            "우디": radar_scores.get("우디", 0),
            "앰버": radar_scores.get("오리엔탈", 0),
            "프레시": radar_scores.get("프레시", 0),
            "구르망": radar_scores.get("구르망", 0),
        }

        # 개인 무드 태그 생성 및 치환
        personal_mood = f"#{' #'.join(fragrance_mapping.get('descriptors', [])[:3])}"
        personal_mood = personal_mood.replace("오리엔탈", "앰버").replace("플로럴", "플로랄")

        # 최종 쿼리 문구 치환 (UI 표시용)
        final_readable_query = query_text.replace("오리엔탈", "앰버").replace("플로럴", "플로랄")

        # --------------------------------------------------------
        # 6. [Response] 최종 리포트 데이터 응답
        # --------------------------------------------------------
        response_data = {
            "type": "personal",
            "personalMood": personal_mood,
            "perfumeKeywords": [
                f"#{kw}" for kw in fragrance_mapping.get("components_ko", [])[:3]
            ],
            "fashionStyle": vl_result.get("visual_summary", ""),
            "analysisMetadata": {
                "base64Image": image_base64,
                "selectedNotes": selected_notes,
                "radarScores": ui_radar_scores,
                "readableQuery": final_readable_query, # RAG 쿼리와 통합된 문구 사용
            },
            "recommendations": recommendations,
        }

        return Response(response_data)

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-15: refactor(analyzeview): optimize API orchestration and documentation. (author: @Gloveman)
# 2026-05-11: docs(wiki): move frontend notes into mdbook. (author: @nobrain711)
# 2026-05-11: feat(backend): migrate django fragrance apiAdds the Django REST backend, scent engine services, perfume data loa.... (author: @nobrain711)
# 2026-05-14: docs(api): document analyze endpoint in swagger. (author: @nobrain711)
# 2026-05-14: refactor(apiview): S4P-58 apply separated aura score logic to apiview. (author: @Gloveman)
# ----------------------------------------------------------------

# EOF: views.py
