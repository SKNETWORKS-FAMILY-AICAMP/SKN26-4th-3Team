"""
@file serializers.py
@role
Serializes perfume domain models for API and documentation surfaces.
"""

from rest_framework import serializers
from .models import Brand, Perfume

class BrandSerializer(serializers.ModelSerializer):
    """브랜드 모델의 기본 식별 정보를 직렬화한다."""

    class Meta:
        """BrandSerializer가 노출할 모델과 필드를 정의한다."""

        model = Brand
        fields = ['id', 'name', 'country_code']

class PerfumeSerializer(serializers.ModelSerializer):
    """향수 모델과 연결된 상세 JSON, 이미지 정보를 API 응답 형태로 직렬화한다."""

    brand_name = serializers.CharField(source='brand.name', read_only=True)
    data = serializers.SerializerMethodField()
    image_asset = serializers.SerializerMethodField()
    
    class Meta:
        """PerfumeSerializer가 노출할 모델과 필드를 정의한다."""

        model = Perfume
        fields = [
            'id', 'brand', 'brand_name', 'korean_name', 'english_name', 
            'product_type', 'family', 'release_year', 'data', 'image_asset', 'created_at'
        ]

    def get_data(self, obj):
        """PerfumeDetail JSON이 없을 때도 빈 딕셔너리로 안전하게 반환한다."""
        detail = getattr(obj, 'detail', None)
        return getattr(detail, 'data', {}) or {}

    def get_image_asset(self, obj):
        """첫 번째 연결 이미지를 프론트엔드가 기대하는 asset payload로 변환한다."""
        detail = getattr(obj, 'detail', None)
        if detail is None:
            return {}

        image = detail.images.first()
        if image is None:
            return {}

        return {
            'original_url': image.original_url,
            'backend_path': image.processed_path,
            'base64': image.base64_data,
        }


class AnalyzeRequestSerializer(serializers.Serializer):
    """분석 API 요청 body schema를 정의한다."""

    image = serializers.CharField(
        help_text="사용자가 업로드한 이미지의 Base64 문자열입니다.",
    )
    selectedNotes = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
        help_text="사용자가 선택한 향 노트 목록입니다.",
    )


class ErrorResponseSerializer(serializers.Serializer):
    """API 오류 응답 schema를 정의한다."""

    error = serializers.CharField(help_text="클라이언트에 표시할 오류 메시지입니다.")


class PriceSerializer(serializers.Serializer):
    """추천 상품 가격 정보를 직렬화한다."""

    raw = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.FloatField(required=False)
    currency = serializers.CharField(required=False, allow_blank=True)


class NotesPyramidSerializer(serializers.Serializer):
    """향수 노트를 top, middle, base 피라미드 구조로 직렬화한다."""

    top = serializers.ListField(child=serializers.CharField(), required=False)
    middle = serializers.ListField(child=serializers.CharField(), required=False)
    base = serializers.ListField(child=serializers.CharField(), required=False)


class RecommendationPerfumeSerializer(serializers.Serializer):
    """추천 카드 내부의 향수 상세 정보를 직렬화한다."""

    id = serializers.IntegerField()
    brand = serializers.CharField()
    koreanName = serializers.CharField()
    englishName = serializers.CharField()
    productType = serializers.CharField()
    family = serializers.CharField()
    releaseYear = serializers.IntegerField(required=False, allow_null=True)
    price = PriceSerializer(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    ingredientsRaw = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.ListField(child=serializers.CharField(), required=False)
    representativeNotes = serializers.ListField(child=serializers.CharField(), required=False)
    notesPyramid = NotesPyramidSerializer(required=False)
    accords = serializers.ListField(child=serializers.CharField(), required=False)
    keywords = serializers.DictField(required=False)
    auraProfile = serializers.DictField(child=serializers.FloatField(), required=False)
    volume = serializers.CharField(required=False, allow_blank=True)
    meta = serializers.DictField(required=False)


class RecommendationImageDetailSerializer(serializers.Serializer):
    """추천 상품 이미지의 원본, 백엔드 경로, base64 정보를 직렬화한다."""

    url = serializers.CharField(required=False, allow_blank=True)
    originalUrl = serializers.CharField(required=False, allow_blank=True)
    backendPath = serializers.CharField(required=False, allow_blank=True)
    base64 = serializers.CharField(required=False, allow_blank=True)


class RecommendationDetailsSerializer(serializers.Serializer):
    """추천 상세 모달에서 사용하는 스토리와 노트 설명을 직렬화한다."""

    story = serializers.CharField(required=False, allow_blank=True)
    topNotes = serializers.CharField(required=False, allow_blank=True)
    middleNotes = serializers.CharField(required=False, allow_blank=True)
    baseNotes = serializers.CharField(required=False, allow_blank=True)
    bestFor = serializers.CharField(required=False, allow_blank=True)


class RecommendationSerializer(serializers.Serializer):
    """개별 추천 결과 카드의 전체 API 응답 schema를 정의한다."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    brand = serializers.CharField()
    price = serializers.CharField()
    price_krw = serializers.IntegerField(required=False)
    size = serializers.CharField()
    image = serializers.CharField(required=False, allow_blank=True)
    imageUrl = serializers.CharField(required=False, allow_blank=True)
    imageBase64 = serializers.CharField(required=False, allow_blank=True)
    perfume = RecommendationPerfumeSerializer()
    imageDetail = RecommendationImageDetailSerializer(required=False)
    imageAsset = serializers.DictField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    family = serializers.CharField()
    category = serializers.CharField()
    similarity = serializers.IntegerField()
    matchReason = serializers.CharField()
    details = RecommendationDetailsSerializer()


class AnalysisMetadataSerializer(serializers.Serializer):
    """분석 결과를 재현하거나 표시하는 데 필요한 메타데이터를 직렬화한다."""

    base64Image = serializers.CharField()
    selectedNotes = serializers.ListField(child=serializers.CharField())
    radarScores = serializers.DictField(child=serializers.FloatField())
    readableQuery = serializers.CharField()


class AnalyzeResponseSerializer(serializers.Serializer):
    """분석 API의 최종 응답 schema를 정의한다."""

    type = serializers.CharField()
    personalMood = serializers.CharField()
    perfumeKeywords = serializers.ListField(child=serializers.CharField())
    fashionStyle = serializers.CharField()
    analysisMetadata = AnalysisMetadataSerializer()
    recommendations = RecommendationSerializer(many=True)

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-14: fix(backend): include perfume image payloads. (author: @nobrain711)
# 2026-05-11: docs(wiki): move frontend notes into mdbook. (author: @nobrain711)
# 2026-05-11: feat(backend): migrate django fragrance apiAdds the Django REST backend, scent engine services, perfume data loa.... (author: @nobrain711)
# 2026-05-14: docs(api): document analyze endpoint in swagger. (author: @nobrain711)
# 2026-05-13: feat(perfumes): persist perfume image assets. (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: serializers.py
