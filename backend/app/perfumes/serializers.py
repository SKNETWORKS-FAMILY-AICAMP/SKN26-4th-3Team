from rest_framework import serializers
from .models import Brand, Perfume

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country_code']

class PerfumeSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    
    class Meta:
        model = Perfume
        fields = [
            'id', 'brand', 'brand_name', 'korean_name', 'english_name', 
            'product_type', 'family', 'release_year', 'data', 'created_at'
        ]
