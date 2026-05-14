"""
@file index_to_pinecone.py
@module Perfumes/Management/Commands/IndexToPinecone
@description
MySQL에 저장된 Perfume 데이터를 Pinecone Vector DB에 인덱싱합니다.

역할:
1. Perfume.data["embedding_doc"]을 읽는다.
2. OpenAI text-embedding-3-small 모델로 임베딩한다.
3. Pinecone에 perfume_id와 metadata를 함께 저장한다.

실행 예시:
    python app/manage.py index_to_pinecone
    python app/manage.py index_to_pinecone --limit 100
    python app/manage.py index_to_pinecone --batch-size 50
    python app/manage.py index_to_pinecone --recreate-index
"""

import os
import time
from typing import Any

from django.core.management.base import BaseCommand

from perfumes.models import Perfume


class Command(BaseCommand):
    help = "Batch index perfumes into Pinecone Vector DB"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=50,
            help="한 번에 임베딩/업로드할 향수 개수",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="테스트용 인덱싱 개수 제한. 0이면 전체 인덱싱",
        )
        parser.add_argument(
            "--recreate-index",
            action="store_true",
            help="기존 Pinecone 인덱스를 삭제 후 재생성",
        )

    def handle(self, *args, **options):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "olfit-perfumes")

        embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        embedding_dimension = int(os.getenv("OPENAI_EMBEDDING_DIMENSION", "1536"))

        if not openai_api_key:
            self.stdout.write(self.style.ERROR("OPENAI_API_KEY가 환경변수에 없습니다."))
            return

        if not pinecone_api_key:
            self.stdout.write(self.style.ERROR("PINECONE_API_KEY가 환경변수에 없습니다."))
            return

        try:
            from openai import OpenAI
            from pinecone import Pinecone, ServerlessSpec
        except ImportError:
            self.stdout.write(
                self.style.ERROR(
                    "필수 라이브러리가 설치되어 있지 않습니다. "
                    "requirements.txt에 openai, pinecone을 추가한 뒤 다시 빌드하세요."
                )
            )
            return

        client = OpenAI(api_key=openai_api_key)
        pc = Pinecone(api_key=pinecone_api_key)

        batch_size = options["batch_size"]
        limit = options["limit"]
        recreate_index = options["recreate_index"]

        self.stdout.write(f"[설정] Pinecone index: {pinecone_index_name}")
        self.stdout.write(f"[설정] Embedding model: {embedding_model}")
        self.stdout.write(f"[설정] Embedding dimension: {embedding_dimension}")

        existing_indexes = pc.list_indexes().names()

        if recreate_index and pinecone_index_name in existing_indexes:
            self.stdout.write(
                self.style.WARNING(f"기존 인덱스 삭제 중: {pinecone_index_name}")
            )
            pc.delete_index(pinecone_index_name)

            for _ in range(30):
                if pinecone_index_name not in pc.list_indexes().names():
                    break
                time.sleep(1)

        if pinecone_index_name not in pc.list_indexes().names():
            self.stdout.write(f"Creating index: {pinecone_index_name}")

            pc.create_index(
                name=pinecone_index_name,
                dimension=embedding_dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=os.getenv("PINECONE_CLOUD", "aws"),
                    region=os.getenv("PINECONE_REGION", "us-east-1"),
                ),
            )

            for _ in range(30):
                if pinecone_index_name in pc.list_indexes().names():
                    break
                time.sleep(1)

        index = pc.Index(pinecone_index_name)

        queryset = Perfume.objects.select_related("brand").all().order_by("id")

        if limit and limit > 0:
            queryset = queryset[:limit]

        perfumes = list(queryset)
        total = len(perfumes)

        if total == 0:
            self.stdout.write(self.style.WARNING("인덱싱할 Perfume 데이터가 없습니다."))
            return

        self.stdout.write(self.style.SUCCESS(f"총 {total}개 향수 인덱싱 시작"))

        indexed_count = 0
        skipped_count = 0

        for start in range(0, total, batch_size):
            batch = perfumes[start : start + batch_size]

            valid_perfumes: list[Perfume] = []
            docs: list[str] = []

            for perfume in batch:
                data = perfume.data or {}
                embedding_doc = str(data.get("embedding_doc", "")).strip()

                if not embedding_doc:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skip perfume_id={perfume.id}: embedding_doc 없음"
                        )
                    )
                    continue

                valid_perfumes.append(perfume)
                docs.append(embedding_doc)

            if not valid_perfumes:
                continue

            try:
                response = client.embeddings.create(
                    model=embedding_model,
                    input=docs,
                )

                embeddings = [item.embedding for item in response.data]

                vectors = []

                for perfume, embedding, embedding_doc in zip(
                    valid_perfumes,
                    embeddings,
                    docs,
                ):
                    vectors.append(
                        {
                            "id": str(perfume.id),
                            "values": embedding,
                            "metadata": self._build_metadata(
                                perfume=perfume,
                                embedding_doc=embedding_doc,
                            ),
                        }
                    )

                index.upsert(vectors=vectors)

                indexed_count += len(vectors)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Indexed batch {start // batch_size + 1}: "
                        f"{len(vectors)} items "
                        f"(누적 {indexed_count}/{total})"
                    )
                )

                time.sleep(0.2)

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error in batch start={start}: {type(e).__name__}: {e}"
                    )
                )
                time.sleep(2)

        self.stdout.write(
            self.style.SUCCESS(
                f"Pinecone indexing complete. "
                f"indexed={indexed_count}, skipped={skipped_count}, total={total}"
            )
        )

    def _build_metadata(self, perfume: Perfume, embedding_doc: str) -> dict[str, Any]:
        """
        Pinecone metadata를 구성합니다.

        실제 상세 정보는 MySQL Perfume.data에서 다시 조회하므로,
        Pinecone에는 검색 결과 연결에 필요한 최소 정보만 저장합니다.
        """

        data = perfume.data or {}

        price = data.get("price") or {}
        if not isinstance(price, dict):
            price = {}

        metadata: dict[str, Any] = {
            "perfume_id": int(perfume.id),
            "brand": str(perfume.brand.name),
            "korean_name": str(perfume.korean_name),
            "english_name": str(perfume.english_name),
            "family": str(perfume.family),
            "product_type": str(perfume.product_type),
            "price_raw": str(price.get("raw", "")),
            "image_url": str(data.get("image_url", "")),
            "embedding_doc_preview": embedding_doc[:1000],
        }

        cleaned = {}

        for key, value in metadata.items():
            if value is None:
                continue

            if isinstance(value, (str, int, float, bool)):
                cleaned[key] = value
            else:
                cleaned[key] = str(value)

        return cleaned