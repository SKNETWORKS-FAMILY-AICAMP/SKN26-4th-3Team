"""
@file views.py
@module Perfumes/Views
@description
Olfít Connect의 핵심 비즈니스 로직을 API 엔드포인트로 노출합니다.
사용자의 요청을 받아 VLM 분석, 아우라 스코어링, 추천 프로세스를 오케스트레이션합니다.

@author Olfít AI Team
@version 4.0.0
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
    이미지와 취향 노트를 받아 최종 향수 추천 리포트를 생성합니다.
    """

    @extend_schema(
        operation_id="analyzePersonalScent",
        summary="이미지와 선호 노트 기반 향수 추천 분석",
        description=(
            "사용자가 업로드한 이미지와 선택한 향 노트를 분석해 아우라 점수, "
            "향수 키워드, Top 5 추천 향수와 상세 표시 정보를 반환합니다."
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
        examples=[
            OpenApiExample(
                "Analyze request",
                value={
                    "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB...",
                    "selectedNotes": ["베르가못", "샌달우드"],
                },
                request_only=True,
            ),
            OpenApiExample(
                "Analyze response",
                value={
                    "type": "personal",
                    "personalMood": "#세련된 #차분한 #모던한",
                    "perfumeKeywords": ["#베르가못", "#시더우드"],
                    "fashionStyle": "검은색 슈트를 입은 세련된 남성",
                    "analysisMetadata": {
                        "base64Image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB...",
                        "selectedNotes": ["베르가못", "샌달우드"],
                        "radarScores": {
                            "플로럴": 0.1,
                            "우디": 0.5,
                            "오리엔탈": 0.1,
                            "프레시": 0.2,
                            "구르망": 0.1,
                        },
                        "readableQuery": "세련된 분위기의 베르가못, 시더우드 향이 느껴지는 우디 계열 향수.",
                    },
                    "recommendations": [
                        {
                            "id": 1,
                            "name": "옴니아 크리스탈린",
                            "brand": "BVLGARI",
                            "price": "$150",
                            "price_krw": 207000,
                            "size": "65ml",
                            "image": "/static/perfumes/images/bvlgari/omnia.jpg",
                            "perfume": {
                                "id": 1,
                                "brand": "BVLGARI",
                                "koreanName": "옴니아 크리스탈린",
                                "englishName": "omnia crystalline",
                                "productType": "perfume",
                                "family": "프레시",
                                "releaseYear": 2005,
                                "price": {
                                    "raw": "$150",
                                    "amount": 150,
                                    "currency": "USD",
                                },
                                "description": "옴니아 크리스탈린 설명",
                                "ingredientsRaw": "",
                                "notes": ["대나무", "서양배", "연꽃"],
                                "representativeNotes": ["대나무", "서양배"],
                                "notesPyramid": {
                                    "top": ["대나무"],
                                    "middle": ["서양배"],
                                    "base": ["연꽃"],
                                },
                                "accords": ["우디", "플로럴"],
                                "keywords": {"ko": ["상쾌한", "우아한"]},
                                "auraProfile": {"프레시": 0.6},
                                "volume": "65ml",
                                "meta": {},
                            },
                            "imageDetail": {
                                "url": "/static/perfumes/images/bvlgari/omnia.jpg",
                                "originalUrl": "https://img.example.com/omnia.jpg",
                                "backendPath": "/backend/app/static/perfumes/images/bvlgari/omnia.jpg",
                                "base64": "base64-image",
                            },
                            "imageAsset": {},
                            "tags": ["우디", "플로럴"],
                            "notes": "대나무, 서양배",
                            "family": "프레시",
                            "category": "Personal",
                            "similarity": 90,
                            "matchReason": "선택하신 #대나무 성분이 포함되어 있으며, 당신의 #프레시 아우라와 완벽하게 조화됩니다.",
                            "details": {
                                "story": "옴니아 크리스탈린 설명",
                                "topNotes": "대나무",
                                "middleNotes": "서양배",
                                "baseNotes": "연꽃",
                                "bestFor": "상쾌한, 우아한",
                            },
                        }
                    ],
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        # [Security] 익명 세션 ID 확인 (Handshake 검증)
        session_id = request.headers.get("X-Session-ID")
        print(f"\n🚨 [CRITICAL DEBUG] ANALYZE API CALLED IN Unified Repo!")
        print(f"   > Session ID: {session_id}")

        if not session_id:
            print("❌ [DEBUG] Rejected: Missing Session ID")
            return Response(
                {
                    "error": "세션 ID가 누락되었습니다. 개인정보 동의 후 다시 시도해주세요."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 요청 데이터 추출
        image_base64 = request.data.get("image")
        selected_notes = request.data.get("selectedNotes", [])

        # 1. 서비스 엔진 초기화
        vl_engine = VLEngine()  # Vision-Language Engine
        aura_service = AuraService()  # Scoring & Query Service
        recommend_service = RecommendationService()  # DB-based Ranking Service

        # 2. [VLM Stage] 실시간 시각 감성 분석 실행
        # NVIDIA NIM API 호출 및 이미지 키워드 추출
        print(f"[STEP 1] 🚀 Starting Live VLM Analysis using {vl_engine.model}...")
        vl_result = vl_engine.analyze_image(image_base64)
        print(f"[STEP 2] 📝 VLM Result Summary: {vl_result.get('visual_summary')}")

        # 3. [Scoring Stage] 5축 아우라 계산 및 대칭 쿼리 생성
        # 이미지 키워드 + 사용자 선택 노트를 통합하여 5차원 벡터 산출
        print("[STEP 3] 📊 Calculating Aura Scores & Generating Query...")
        radar_scores, fragrance_mapping, query_text, readable_query, aura_vectors = (
            aura_service.calculate_combined_aura(vl_result, selected_notes)
        )
        print(f"       > Primary Family: {max(aura_vectors, key=aura_vectors.get)}")

        # 4. [Recommendation Stage] 하이브리드 재랭킹 추천 (Top 5)
        # 5축 유사도(70%) + 성분 가산점(30%)을 적용하여 DB에서 제품 추출
        print("[STEP 4] 🎯 Fetching Recommendations from DB...")
        recommendations = recommend_service.recommend(
            aura_vectors, query_text, selected_notes
        )

        rec_names = [r["name"] for r in recommendations]
        print(f"[STEP 5] ✅ Final Recommendations: {', '.join(rec_names)}")
        print(f"--- Analysis for Session {session_id} Complete ---\n")

        # 5. [Mapping] 프론트엔드 UI 규격에 맞게 명칭 치환 (오리엔탈 -> 앰버, 플로럴 -> 플로랄)
        ui_radar_scores = {
            "플로랄": radar_scores.get("플로럴", 0),
            "우디": radar_scores.get("우디", 0),
            "앰버": radar_scores.get("오리엔탈", 0),
            "프레시": radar_scores.get("프레시", 0),
            "구르망": radar_scores.get("구르망", 0),
        }

        # UI용 무드 키워드 및 쿼리 문구 치환
        personal_mood = f"#{' #'.join(fragrance_mapping.get('descriptors', [])[:3])}"
        personal_mood = personal_mood.replace("오리엔탈", "앰버").replace(
            "플로럴", "플로랄"
        )

        final_readable_query = readable_query.replace("오리엔탈", "앰버").replace(
            "플로럴", "플로랄"
        )

        # 6. [Response] 프론트엔드 규격에 맞춘 최종 결과 응답
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
                "readableQuery": final_readable_query,
            },
            "recommendations": recommendations,
        }

        return Response(response_data)

# EOF: views.py
