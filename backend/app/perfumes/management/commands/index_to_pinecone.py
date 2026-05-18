"""
@file index_to_pinecone.py
@description
MySQL에 저장된 향수 데이터를 Pinecone 벡터 데이터베이스로 인덱싱하는 Django 관리 명령어입니다.
OpenAI 임베딩 모델을 사용하여 텍스트를 벡터화하며, 데이터 변경 시에만 임베딩을 갱신하는
'Hash 기반 스마트 캐싱' 기능을 포함하고 있습니다.

@author Olfít AI Team
@version 4.9.0
"""

import os
import time
import hashlib
from typing import Any
from django.core.management.base import BaseCommand
from perfumes.models import Perfume, PerfumeDetail


class Command(BaseCommand):
    """
    Pinecone 인덱싱 프로세스를 관리하는 커맨드 클래스입니다.
    """

    help = "Batch index perfumes into Pinecone Vector DB with Hash-based smart caching"

    def add_arguments(self, parser):
        """명령어 인자를 정의합니다."""
        parser.add_argument(
            "--batch-size",
            type=int,
            default=50,
            help="한 번에 Pinecone에 Upsert할 개수",
        )
        parser.add_argument(
            "--limit", type=int, default=0, help="테스트용 개수 제한 (0은 전체)"
        )
        parser.add_argument(
            "--recreate-index",
            action="store_true",
            help="기존 Pinecone 인덱스 삭제 후 재생성",
        )
        parser.add_argument(
            "--use-local-cache",
            action="store_true",
            help="문서 내용이 동일할 경우 DB에 저장된 벡터 재사용 (OpenAI 비용 절감)",
        )

    def handle(self, *args, **options):
        """
        인덱싱 프로세스의 메인 로직을 수행합니다.
        API 키 확인, 인덱스 상태 점검, 배치 임베딩 및 Upsert 순서로 진행됩니다.
        """
        # 1. 환경 변수 및 설정 로드
        openai_api_key = os.getenv("OPENAI_API_KEY")
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "olfit-perfumes")

        embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        dimension = 1536

        if not openai_api_key or not pinecone_api_key:
            self.stdout.write(
                self.style.ERROR(
                    "API Key가 설정되지 않았습니다. .env 파일을 확인하세요."
                )
            )
            return

        try:
            from openai import OpenAI
            from pinecone import Pinecone, ServerlessSpec
        except ImportError:
            self.stdout.write(
                self.style.ERROR("필수 라이브러리(openai, pinecone-client)가 없습니다.")
            )
            return

        client = OpenAI(api_key=openai_api_key)
        pc = Pinecone(api_key=pinecone_api_key)

        # --------------------------------------------------------
        # [2. Index Management]
        # 인덱스 존재 여부를 확인하고, 필요 시 삭제 및 재생성을 수행합니다.
        # --------------------------------------------------------
        existing_indexes = pc.list_indexes().names()
        if options["recreate_index"] and pinecone_index_name in existing_indexes:
            self.stdout.write(
                self.style.WARNING(f"기존 인덱스 삭제 중: {pinecone_index_name}")
            )
            pc.delete_index(pinecone_index_name)

            # 삭제 완료 대기 (최대 30초)
            for _ in range(30):
                if pinecone_index_name not in pc.list_indexes().names():
                    break
                time.sleep(1)
            existing_indexes = pc.list_indexes().names()

        if pinecone_index_name not in existing_indexes:
            self.stdout.write(f"새 인덱스 생성 중: {pinecone_index_name}...")
            pc.create_index(
                name=pinecone_index_name,
                dimension=dimension,
                metric="cosine",  # 코사인 유사도 기준 검색
                spec=ServerlessSpec(
                    cloud=os.getenv("PINECONE_CLOUD", "aws"),
                    region=os.getenv("PINECONE_REGION", "us-east-1"),
                ),
            )
            # 생성 준비 완료 대기
            for _ in range(30):
                if pinecone_index_name in pc.list_indexes().names():
                    break
                time.sleep(1)

        index = pc.Index(pinecone_index_name)

        # --------------------------------------------------------
        # [3. Data Preparation]
        # MySQL에서 인덱싱할 향수 데이터를 효율적으로 로드합니다.
        # --------------------------------------------------------
        queryset = (
            Perfume.objects.select_related("brand", "detail").all().order_by("id")
        )
        db_count = queryset.count()

        # 이미 인덱싱이 완료되었는지 확인 (중복 작업 방지)
        stats = index.describe_index_stats()
        total_vector_count = stats.get("total_vector_count", 0)

        if (
            not options["recreate_index"]
            and total_vector_count >= db_count
            and db_count > 0
        ):
            self.stdout.write(
                self.style.SUCCESS(
                    f"Pinecone 인덱스가 이미 채워져 있습니다. 작업을 건너뜁니다."
                )
            )
            return

        if options["limit"] > 0:
            queryset = queryset[: options["limit"]]

        perfumes = list(queryset)
        total = len(perfumes)
        batch_size = options["batch_size"]
        use_cache = options["use_local_cache"]

        self.stdout.write(
            self.style.SUCCESS(
                f"총 {total}개 향수 인덱싱 시작 (캐시 모드: {use_cache})"
            )
        )

        # --------------------------------------------------------
        # [4. Batch Processing with Smart Caching]
        # 데이터를 배치 단위로 나누어 임베딩을 생성하고 Pinecone에 적재합니다.
        # --------------------------------------------------------
        indexed_count = 0
        skipped_count = 0

        for start in range(0, total, batch_size):
            batch = perfumes[start : start + batch_size]
            upsert_vectors = []
            to_embed_items = (
                []
            )  # 임베딩이 필요한 아이템 목록 (detail, doc, perfume, hash)

            for p in batch:
                if not hasattr(p, "detail"):
                    skipped_count += 1
                    continue

                detail = p.detail
                p_data = detail.data or {}
                embedding_doc = p_data.get("embedding_doc", "").strip()

                if not embedding_doc:
                    skipped_count += 1
                    continue

                # 4-1. Hash 기반 변경 감지
                # embedding_doc의 MD5 해시를 계산하여 내용 변경 여부를 확인합니다.
                current_hash = hashlib.md5(embedding_doc.encode("utf-8")).hexdigest()
                cached_hash = p_data.get("embedding_hash")

                # 캐시 사용 조건: 1) 옵션 활성화 2) 벡터 존재 3) 해시값이 동일(내용 불변)
                if (
                    use_cache
                    and "embedding_vector" in p_data
                    and cached_hash == current_hash
                ):
                    upsert_vectors.append(
                        {
                            "id": str(p.id),
                            "values": p_data["embedding_vector"],
                            "metadata": self._build_metadata(p),
                        }
                    )
                else:
                    # 조건 미충족 시 OpenAI API 호출 대상으로 분류
                    to_embed_items.append((detail, embedding_doc, p, current_hash))

            # 4-2. OpenAI Embedding 생성 (배치 처리)
            if to_embed_items:
                try:
                    docs = [item[1] for item in to_embed_items]
                    response = client.embeddings.create(
                        input=docs, model=embedding_model
                    )

                    for i, (detail, doc, p, doc_hash) in enumerate(to_embed_items):
                        vector = response.data[i].embedding

                        # 차후 재사용을 위해 벡터와 해시를 DB에 캐싱
                        detail.data["embedding_vector"] = vector
                        detail.data["embedding_hash"] = doc_hash
                        detail.save(update_fields=["data"])

                        upsert_vectors.append(
                            {
                                "id": str(p.id),
                                "values": vector,
                                "metadata": self._build_metadata(p),
                            }
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"OpenAI API 에러: {e}"))
                    continue

            # 4-3. Pinecone Upsert
            if upsert_vectors:
                try:
                    index.upsert(vectors=upsert_vectors)
                    indexed_count += len(upsert_vectors)
                    self.stdout.write(f"Progress: {indexed_count}/{total}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Pinecone Upsert 에러: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"인덱싱 완료: {indexed_count}개 성공, {skipped_count}개 제외"
            )
        )

    def _build_metadata(self, p: Perfume) -> dict[str, Any]:
        """
        Pinecone 검색 결과 필터링 및 하이브리드 재정렬에 필요한 메타데이터를 구성합니다.

        Args:
            p (Perfume): 인덱싱할 향수 모델 객체

        Returns:
            dict: Pinecone에 저장될 클리닝된 메타데이터 딕셔너리
        """
        p_data = p.detail.data or {}
        aura = p_data.get("aura_profile", {})

        # 가격 및 통화 변환 (utils 활용)
        from perfumes.utils import convert_to_krw

        price_data = p_data.get("price") or {}
        price_raw = (
            price_data.get("raw", "정보없음")
            if isinstance(price_data, dict)
            else str(price_data)
        )
        price_krw = convert_to_krw(price_data)

        # 구조화된 노트 정보 로드
        pyramid = p_data.get("notes_parsed", {})

        # 메타데이터 맵핑
        metadata = {
            "perfume_id": int(p.id),
            "brand": str(p.brand.name),
            "korean_name": str(p.korean_name),
            "english_name": str(p.english_name),
            "family": str(p.family),
            "product_type": str(p.product_type),
            "release_year": p.release_year or 0,
            # [재정렬 핵심] 아우라 5축 (L2 기준, 개별 축 기본값 0.0)
            "aura_floral": float(aura.get("플로럴", aura.get("플로랄", 0.0))),
            "aura_woody": float(aura.get("우디", 0.0)),
            "aura_amber": float(aura.get("오리엔탈", aura.get("앰버", 0.0))),
            "aura_fresh": float(aura.get("프레시", 0.0)),
            "aura_gourmand": float(aura.get("구르망", 0.0)),
            # 가격 정보
            "price_raw": price_raw,
            "price_krw": price_krw,
            "price_amount": float(
                price_data.get("amount", 0) if isinstance(price_data, dict) else 0
            ),
            "price_currency": str(
                price_data.get("currency", "KRW")
                if isinstance(price_data, dict)
                else "KRW"
            ),
            # 텍스트 정보
            "volume": str(p_data.get("volume", "N/A")),
            "image_url": str(p_data.get("image_url", "")),
            "accords": p_data.get("accords", [])[:5],
            "representative_notes": p_data.get("representative_notes", [])[:5],
            "description": str(p_data.get("description", ""))[:1000],
            # 구조화된 피라미드 (UI 모달용)
            "top_notes": pyramid.get("top", [])[:5],
            "middle_notes": pyramid.get("middle", [])[:5],
            "base_notes": pyramid.get("base", [])[:5],
            "keywords": (
                p_data.get("keywords", [])[:5]
                if isinstance(p_data.get("keywords"), list)
                else []
            ),
        }

        # None 값 제거 및 타입 안정성 확보 (Pinecone 제약)
        return {
            k: (v if isinstance(v, (str, int, float, bool, list)) else str(v))
            for k, v in metadata.items()
            if v is not None
        }

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-15: feat(index_to_pinecone): implement pinecone indexing with smart hash-based caching. (author: @Gloveman)
# 2026-05-13: fix(django): guard migrate schema drift. (author: @nobrain711)
# 2026-05-11: feat(backend): migrate django fragrance apiAdds the Django REST backend, scent engine services, perfume data loa.... (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: index_to_pinecone.py
