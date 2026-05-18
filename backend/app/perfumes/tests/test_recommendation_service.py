"""
@file test_recommendation_service.py
@role
RecommendationService의 추천 응답 payload를 검증하는 테스트 파일입니다.
향수 상세 정보, 이미지/base64 응답, notes_parsed 누락 시 flat notes fallback을 확인합니다.
"""

from django.test import TestCase

from perfumes.models import Brand, Perfume, PerfumeDetail, PerfumeImage
from perfumes.services.recommendation_service import RecommendationService

class RecommendationServiceTest(TestCase):
    def test_recommendations_include_perfume_detail_and_image_payload(self):
        brand = Brand.objects.create(name="BVLGARI")
        perfume = Perfume.objects.create(
            brand=brand,
            korean_name="옴니아 크리스탈린",
            english_name="omnia crystalline",
            product_type="perfume",
            family="프레시",
            release_year=2005,
        )
        detail = PerfumeDetail.objects.create(
            perfume=perfume,
            data={
                "price": {"raw": "$150", "amount": 150, "currency": "USD"},
                "description": "옴니아 크리스탈린 설명",
                "notes": ["대나무", "서양배", "연꽃"],
                "representative_notes": ["대나무", "서양배"],
                "notes_parsed": {
                    "top": ["대나무"],
                    "middle": ["서양배"],
                    "base": ["연꽃"],
                },
                "accords": ["우디", "플로럴"],
                "keywords": ["상쾌한", "우아한"],
                "aura_profile": {
                    "플로럴": 0.1,
                    "우디": 0.1,
                    "오리엔탈": 0.1,
                    "프레시": 0.6,
                    "구르망": 0.1,
                },
                "volume": "65ml",
                "meta": {"original_country": "이탈리아"},
            },
        )
        PerfumeImage.objects.create(
            perfume_detail=detail,
            original_url="https://img.example.com/omnia.jpg",
            processed_path="/backend/app/static/perfumes/images/bvlgari/omnia.jpg",
            base64_data="base64-image",
        )

        service = RecommendationService()
        result = service.recommend(
            {"플로럴": 0.1, "우디": 0.1, "오리엔탈": 0.1, "프레시": 0.6, "구르망": 0.1},
            "",
            ["대나무"],
        )

        self.assertEqual(len(result), 1)
        recommendation = result[0]
        self.assertEqual(recommendation["perfume"]["koreanName"], "옴니아 크리스탈린")
        self.assertEqual(recommendation["perfume"]["price"]["raw"], "$150")
        self.assertEqual(recommendation["perfume"]["description"], "옴니아 크리스탈린 설명")
        self.assertEqual(recommendation["perfume"]["notes"], ["대나무", "서양배"])
        self.assertEqual(recommendation["perfume"]["accords"], ["우디", "플로럴"])
        self.assertEqual(recommendation["perfume"]["keywords"]["ko"], ["상쾌한", "우아한"])
        self.assertEqual(recommendation["details"]["topNotes"], "대나무")
        self.assertEqual(recommendation["details"]["middleNotes"], "서양배")
        self.assertEqual(recommendation["details"]["baseNotes"], "연꽃")
        self.assertEqual(
            recommendation["imageDetail"]["url"],
            "/static/perfumes/images/bvlgari/omnia.jpg",
        )
        self.assertEqual(recommendation["imageDetail"]["base64"], "base64-image")
        self.assertEqual(recommendation["image"], "/static/perfumes/images/bvlgari/omnia.jpg")
        self.assertEqual(
            recommendation["imageUrl"],
            "http://localhost:8000/static/perfumes/images/bvlgari/omnia.jpg",
        )
        self.assertEqual(recommendation["imageBase64"], "base64-image")

    def test_recommendations_split_flat_notes_when_parsed_notes_are_missing(self):
        brand = Brand.objects.create(name="LE LABO")
        perfume = Perfume.objects.create(
            brand=brand,
            korean_name="네롤리 36",
            english_name="neroli 36",
            product_type="perfume",
            family="프레시",
        )
        PerfumeDetail.objects.create(
            perfume=perfume,
            data={
                "description": "네롤리 36 설명",
                "notes": ["네롤리", "베르가못", "오렌지 블라썸", "시더우드", "나르가모타"],
                "representative_notes": ["네롤리", "베르가못", "오렌지 블라썸", "시더우드", "나르가모타"],
                "aura_profile": {
                    "플로럴": 0.1,
                    "우디": 0.1,
                    "오리엔탈": 0.1,
                    "프레시": 0.6,
                    "구르망": 0.1,
                },
            },
        )

        service = RecommendationService()
        result = service.recommend(
            {"플로럴": 0.1, "우디": 0.1, "오리엔탈": 0.1, "프레시": 0.6, "구르망": 0.1},
            "",
            ["네롤리"],
        )

        recommendation = result[0]
        self.assertEqual(recommendation["details"]["topNotes"], "네롤리, 베르가못, 오렌지 블라썸")
        self.assertEqual(recommendation["details"]["middleNotes"], "나르가모타")
        self.assertEqual(recommendation["details"]["baseNotes"], "시더우드")


# ----------------------------------------------------------------
# Update History
# 2026-05-18: tests.py에서 RecommendationServiceTest를 분리하고 파일 역할 header/footer 추가. (worker: nobrain711)
# ----------------------------------------------------------------

# EOF: test_recommendation_service.py


