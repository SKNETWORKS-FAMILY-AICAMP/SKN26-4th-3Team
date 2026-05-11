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
from scent_engine import VLEngine
from .services.aura_service import AuraService
from .services.recommendation_service import RecommendationService

class AnalyzeView(APIView):
    """
    [Main Analysis Endpoint]
    POST /api/analyze/
    이미지와 취향 노트를 받아 최종 향수 추천 리포트를 생성합니다.
    """
    
    def post(self, request):
        # [Security] 익명 세션 ID 확인 (Handshake 검증)
        session_id = request.headers.get('X-Session-ID')
        print(f"\n🚨 [CRITICAL DEBUG] ANALYZE API CALLED IN Unified Repo!")
        print(f"   > Session ID: {session_id}")
        
        if not session_id:
            print("❌ [DEBUG] Rejected: Missing Session ID")
            return Response(
                {"error": "세션 ID가 누락되었습니다. 개인정보 동의 후 다시 시도해주세요."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 요청 데이터 추출
        image_base64 = request.data.get('image')
        selected_notes = request.data.get('selectedNotes', [])

        # 1. 서비스 엔진 초기화
        vl_engine = VLEngine() # Vision-Language Engine
        aura_service = AuraService() # Scoring & Query Service
        recommend_service = RecommendationService() # DB-based Ranking Service

        # 2. [VLM Stage] 실시간 시각 감성 분석 실행
        # NVIDIA NIM API 호출 및 이미지 키워드 추출
        print(f"[STEP 1] 🚀 Starting Live VLM Analysis using {vl_engine.model}...")
        vl_result = vl_engine.analyze_image(image_base64)
        print(f"[STEP 2] 📝 VLM Result Summary: {vl_result.get('visual_summary')}")

        # 3. [Scoring Stage] 5축 아우라 계산 및 대칭 쿼리 생성
        # 이미지 키워드 + 사용자 선택 노트를 통합하여 5차원 벡터 산출
        print("[STEP 3] 📊 Calculating Aura Scores & Generating Query...")
        radar_scores, fragrance_mapping, query_text, readable_query = aura_service.calculate_combined_aura(vl_result, selected_notes)
        print(f"       > Primary Family: {max(radar_scores, key=radar_scores.get)}")

        # 4. [Recommendation Stage] 하이브리드 재랭킹 추천 (Top 5)
        # 5축 유사도(70%) + 성분 가산점(30%)을 적용하여 DB에서 제품 추출
        print("[STEP 4] 🎯 Fetching Recommendations from DB...")
        recommendations = recommend_service.recommend(radar_scores, query_text, selected_notes)
        
        rec_names = [r['name'] for r in recommendations]
        print(f"[STEP 5] ✅ Final Recommendations: {', '.join(rec_names)}")
        print(f"--- Analysis for Session {session_id} Complete ---\n")

        # 5. [Response] 프론트엔드 규격에 맞춘 최종 결과 응답
        response_data = {
            "type": "personal",
            "personalMood": f"#{' #'.join(fragrance_mapping.get('descriptors', [])[:3])}",
            "perfumeKeywords": [f"#{kw}" for kw in fragrance_mapping.get('components_ko', [])[:3]],
            "fashionStyle": vl_result.get("visual_summary", ""),
            "analysisMetadata": {
                "base64Image": image_base64,
                "selectedNotes": selected_notes,
                "radarScores": radar_scores,
                "readableQuery": readable_query
            },
            "recommendations": recommendations
        }

        return Response(response_data)

# EOF: views.py
