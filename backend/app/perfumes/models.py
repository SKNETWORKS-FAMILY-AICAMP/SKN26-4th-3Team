from django.db import models

class Brand(models.Model):
    """
    향수 브랜드 정보를 관리하는 테이블
    """
    name = models.CharField(max_length=100, unique=True, help_text="브랜드 공식 명칭")
    country_code = models.CharField(max_length=10, blank=True, null=True, help_text="국가 코드 (KR, FR, UK 등)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Perfume(models.Model):
    """
    향수 상품의 핵심 메타데이터와 상세 정보를 관리하는 테이블
    """
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='perfumes', help_text="브랜드 참조")
    korean_name = models.CharField(max_length=255, help_text="한글 상품명")
    english_name = models.CharField(max_length=255, help_text="영문 상품명")
    
    # 원본 데이터의 'product_subtype'을 DB의 'product_type'으로 매핑
    product_type = models.CharField(max_length=50, help_text="perfume, cologne 등 기본 분류")
    
    # 5대 계열: 플로럴, 우디, 오리엔탈, 프레시, 구르망
    family = models.CharField(max_length=50, help_text="5대 핵심 계열")
    
    release_year = models.IntegerField(null=True, blank=True, help_text="출시년도")
    
    # NoSQL 스타일의 상세 정보 통합 필드 (Price, Volume, Notes, Accords, Keywords, Image 등)
    # MySQL의 JSON 타입을 활용
    data = models.JSONField(default=dict, help_text="상세 정보 (NoSQL 스타일)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 동일 브랜드 내 중복 상품 방지
        unique_together = ('brand', 'english_name')

    def __str__(self):
        return f"[{self.brand.name}] {self.english_name}"
