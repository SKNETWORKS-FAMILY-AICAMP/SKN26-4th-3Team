from rest_framework import serializers
from .models import Brand, Perfume

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country_code']

class PerfumeSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    data = serializers.SerializerMethodField()
    
    class Meta:
        model = Perfume
        fields = [
            'id', 'brand', 'brand_name', 'korean_name', 'english_name', 
            'product_type', 'family', 'release_year', 'data', 'created_at'
        ]

    def get_data(self, obj):
        detail = getattr(obj, 'detail', None)
        return getattr(detail, 'data', {}) or {}
