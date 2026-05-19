"""
@file backfill_perfume_image_urls.py
@role
Runs Fragrantica image URL backfill as a Django management command.
"""

from django.conf import settings
from django.core.management.base import BaseCommand
import json
from pathlib import Path

from perfumes.models import PerfumeRawData
from perfumes.services.fragrantica_image_backfill import backfill_raw_files


class Command(BaseCommand):
    """Fragrantica 이미지 URL 보강 작업을 실행하는 Django management command."""

    help = "Backfill missing Fragrantica image_url values into raw files and PerfumeRawData."

    def add_arguments(self, parser):
        """raw 파일 위치, 처리 제한, dry-run 옵션을 등록한다."""
        parser.add_argument(
            "--raw-dir",
            default=settings.BASE_DIR / "data" / "raw",
            help="Directory containing *_fragrance_data.json files.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of missing records to check.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Fetch and match images without writing files or database rows.",
        )

    def handle(self, *args, **options):
        """raw 파일 backfill을 실행하고 필요 시 PerfumeRawData까지 동기화한다."""
        result = backfill_raw_files(
            options["raw_dir"],
            limit=options["limit"],
            dry_run=options["dry_run"],
        )
        db_updated = 0
        if not options["dry_run"]:
            db_updated = sync_database_raw_json(options["raw_dir"])

        self.stdout.write(
            self.style.SUCCESS(
                "Fragrantica image URL backfill finished: "
                f"{result.checked} checked, {result.updated} raw records updated, "
                f"{db_updated} database records synced, {len(result.unmatched or [])} unmatched."
            )
        )
        for name in (result.unmatched or [])[:20]:
            self.stdout.write(self.style.WARNING(f"Image URL not matched: {name}"))


def sync_database_raw_json(raw_dir):
    """backfill된 raw 파일의 image_url/product_url을 PerfumeRawData.raw_json에 반영한다."""
    updated = 0
    records_by_key = {}
    for json_path in sorted(Path(raw_dir).glob("*_fragrance_data.json")):
        records = json.loads(json_path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            brand_name = str(record.get("brand") or "").strip().upper()
            english_name = record.get("english_name") or record.get("normalized_name") or record.get("korean_name")
            image_url = str(record.get("image_url") or "").strip()
            if not brand_name or not english_name or not image_url:
                continue
            records_by_key[(brand_name, str(english_name))] = record

    for raw_data in PerfumeRawData.objects.select_related("perfume__brand"):
        brand_name = raw_data.perfume.brand.name
        english_name = raw_data.perfume.english_name
        record = records_by_key.get((brand_name, english_name))
        if not record:
            continue

        raw_json = raw_data.raw_json
        if not isinstance(raw_json, dict):
            continue

        image_url = str(record.get("image_url") or "").strip()
        if not image_url or raw_json.get("image_url") == image_url:
            continue

        raw_json["image_url"] = image_url
        raw_json["product_url"] = record.get("product_url", raw_json.get("product_url", ""))
        raw_data.raw_json = raw_json
        raw_data.save(update_fields=["raw_json"])
        updated += 1
    return updated

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-13: feat(perfumes): persist perfume image assets. (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: backfill_perfume_image_urls.py
