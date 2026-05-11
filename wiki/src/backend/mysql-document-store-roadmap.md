# MySQL Document Store Roadmap

## Status

Deferred. 현재 단계에서는 Django ORM 기반의 RDB 모델을 유지하고, 추후 데이터 규모와 검색 요구가 커질 때 MySQL Document Store 성격의 JSON 문서 저장 계층을 도입한다.

## Context

현재 백엔드는 MySQL의 관계형 테이블을 중심으로 향수 데이터를 관리한다. `Perfume` 모델은 브랜드, 상품명, 계열, 출시년도처럼 검색과 무결성이 중요한 값은 정규 컬럼으로 두고, 가격, 노트, 설명, 이미지 URL, 아우라 프로필, 임베딩 문서 등 유동적인 상세 정보는 `data` JSON 컬럼에 저장한다.

이 구조는 현재 800여 개 향수 데이터와 추천 MVP에는 충분하다. 다만 JSON 내부 값이 검색, 정렬, 추천, RAG 파이프라인의 핵심 조건으로 확장되면 JSON 컬럼 하나에 원본 문서와 파생 데이터를 모두 넣는 방식은 관리가 어려워질 수 있다.

## Decision

당장은 별도 MongoDB 같은 물리 DB를 추가하지 않는다. MySQL 안에서 RDB 테이블과 JSON 문서 저장 방식을 함께 쓰는 방향을 유지한다.

추후 개발에서는 전체 모델을 MySQL Document Store 중심으로 전환하지 않고, 다음처럼 역할을 분리한다.

```text
RDB tables
- brands
- perfumes
- perfume_notes
- perfume_aura_scores
- perfume_prices

JSON document storage in MySQL
- perfume_documents
  - perfume_id
  - source
  - raw_data
  - normalized_data
  - embedding_doc
  - created_at
  - updated_at
```

## Recommended First Step

X DevAPI 컬렉션을 바로 도입하기보다 Django ORM에 잘 맞는 문서 테이블을 먼저 추가한다.

```python
class PerfumeDocument(models.Model):
    perfume = models.OneToOneField(
        Perfume,
        on_delete=models.CASCADE,
        related_name="document",
    )
    source = models.CharField(max_length=100)
    raw_data = models.JSONField(default=dict)
    normalized_data = models.JSONField(default=dict)
    embedding_doc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

이렇게 하면 MySQL의 JSON 문서 저장 장점을 유지하면서도 Django 마이그레이션, 테스트, ORM 조회 흐름을 크게 깨지 않는다.

## Migration Triggers

다음 조건 중 하나 이상이 현실화되면 문서 저장 계층 분리를 시작한다.

- JSON 내부 필드로 검색하거나 정렬하는 API가 늘어난다.
- 브랜드별 원본 JSON 구조가 계속 바뀌어 `Perfume.data`의 의미가 불명확해진다.
- `aura_profile`, `embedding_doc`, `notes`, `price.amount`가 추천과 검색의 핵심 조건이 된다.
- 원본 크롤링 데이터와 서비스 정규화 데이터를 동시에 보관해야 한다.
- RAG 재색인 이력이나 원본 문서 버전 관리가 필요해진다.

## Implementation Notes

- `Perfume`에는 서비스 식별과 필터링에 필요한 안정적인 컬럼만 남긴다.
- 원본 크롤링 응답은 `PerfumeDocument.raw_data`에 보관한다.
- 서비스에서 사용하는 정규화 문서는 `PerfumeDocument.normalized_data`에 보관한다.
- RAG 입력 문자열은 JSON 내부에만 숨기지 말고 `embedding_doc`처럼 명시 필드로 둔다.
- JSON 내부 필드를 DB에서 자주 조회해야 하면 generated column 또는 functional index를 검토한다.
- X DevAPI 기반 Collection 접근은 Django ORM 테이블 분리 후에도 문서 CRUD 요구가 충분히 커졌을 때 별도 repository/service 계층으로 도입한다.

## Consequences

이 방향은 MySQL 하나로 RDB와 문서형 데이터를 함께 관리하므로 운영 복잡도를 낮춘다. 백업, 권한, 트랜잭션, 배포 단위도 기존 MySQL 운영 체계를 따른다.

대신 JSON 문서 구조는 애플리케이션 레벨에서 검증해야 한다. 스키마리스 저장소처럼 쓰더라도 추천과 RAG에 필요한 필드는 테스트와 데이터 로더에서 명시적으로 검증해야 한다.

## Current Recommendation

현재는 `Perfume.data` JSON 컬럼을 유지한다. 다음 단계에서 바로 해야 할 일은 물리 DB 분리가 아니라, JSON 안에 섞인 원본 문서와 추천용 파생 데이터를 분리할 수 있도록 `PerfumeDocument` 같은 문서 테이블을 설계하는 것이다.
