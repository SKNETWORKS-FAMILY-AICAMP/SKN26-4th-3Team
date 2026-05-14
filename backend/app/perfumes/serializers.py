from rest_framework import serializers
from .models import Brand, Perfume

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country_code']

class PerfumeSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    data = serializers.SerializerMethodField()
    image_asset = serializers.SerializerMethodField()
    
    class Meta:
        model = Perfume
        fields = [
            'id', 'brand', 'brand_name', 'korean_name', 'english_name', 
            'product_type', 'family', 'release_year', 'data', 'image_asset', 'created_at'
        ]

    def get_data(self, obj):
        detail = getattr(obj, 'detail', None)
        return getattr(detail, 'data', {}) or {}

    def get_image_asset(self, obj):
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
    error = serializers.CharField(help_text="클라이언트에 표시할 오류 메시지입니다.")


class PriceSerializer(serializers.Serializer):
    raw = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.FloatField(required=False)
    currency = serializers.CharField(required=False, allow_blank=True)


class NotesPyramidSerializer(serializers.Serializer):
    top = serializers.ListField(child=serializers.CharField(), required=False)
    middle = serializers.ListField(child=serializers.CharField(), required=False)
    base = serializers.ListField(child=serializers.CharField(), required=False)


class RecommendationPerfumeSerializer(serializers.Serializer):
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
    url = serializers.CharField(required=False, allow_blank=True)
    originalUrl = serializers.CharField(required=False, allow_blank=True)
    backendPath = serializers.CharField(required=False, allow_blank=True)
    base64 = serializers.CharField(required=False, allow_blank=True)


class RecommendationDetailsSerializer(serializers.Serializer):
    story = serializers.CharField(required=False, allow_blank=True)
    topNotes = serializers.CharField(required=False, allow_blank=True)
    middleNotes = serializers.CharField(required=False, allow_blank=True)
    baseNotes = serializers.CharField(required=False, allow_blank=True)
    bestFor = serializers.CharField(required=False, allow_blank=True)


class RecommendationSerializer(serializers.Serializer):
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
    base64Image = serializers.CharField()
    selectedNotes = serializers.ListField(child=serializers.CharField())
    radarScores = serializers.DictField(child=serializers.FloatField())
    readableQuery = serializers.CharField()


class AnalyzeResponseSerializer(serializers.Serializer):
    type = serializers.CharField()
    personalMood = serializers.CharField()
    perfumeKeywords = serializers.ListField(child=serializers.CharField())
    fashionStyle = serializers.CharField()
    analysisMetadata = AnalysisMetadataSerializer()
    recommendations = RecommendationSerializer(many=True)
