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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 동일 브랜드 내 중복 상품 방지
        unique_together = ('brand', 'english_name')

    def __str__(self):
        return f"[{self.brand.name}] {self.english_name}"


class PerfumeDetail(models.Model):
    """
    향수 추천과 표시 로직에서 사용하는 상세 JSON 데이터를 관리하는 테이블
    """
    perfume = models.OneToOneField(Perfume, on_delete=models.CASCADE, related_name='detail', help_text="향수 참조")
    data = models.JSONField(default=dict, help_text="서비스용 향수 상세 JSON 문서")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Detail for {self.perfume}"


class PerfumeRawData(models.Model):
    """
    수집 원본 JSON과 출처 URL을 보존하는 테이블
    """
    perfume = models.OneToOneField(Perfume, on_delete=models.CASCADE, related_name='raw_data', help_text="향수 참조")
    raw_json = models.JSONField(default=dict, help_text="변형 전 원본 향수 JSON 문서")
    source_url = models.CharField(max_length=500, blank=True, null=True, help_text="원본 페이지 URL")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Raw data for {self.perfume}"


class PerfumeImage(models.Model):
    """
    향수 상세 데이터에 연결된 원본 이미지 URL과 로컬 처리 경로를 관리하는 테이블
    """
    perfume_detail = models.ForeignKey(PerfumeDetail, on_delete=models.CASCADE, related_name='images', help_text="향수 상세 참조")
    original_url = models.CharField(max_length=500, help_text="원본 이미지 URL")
    processed_path = models.CharField(max_length=500, blank=True, help_text="다운로드 또는 처리된 이미지 경로")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('perfume_detail', 'original_url')

    def __str__(self):
        return self.original_url
