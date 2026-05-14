import base64
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from perfumes.models import Perfume, PerfumeImage
from perfumes.services.image_extractor import extract_images_from_raw_dir


class Command(BaseCommand):
    help = "Download perfume images from backend/app/data/raw into static/perfumes/images."

    def add_arguments(self, parser):
        parser.add_argument(
            "--raw-dir",
            default=settings.BASE_DIR / "data" / "raw",
            help="Directory containing *_fragrance_data.json files.",
        )
        parser.add_argument(
            "--output-dir",
            default=settings.BASE_DIR / "static" / "perfumes" / "images",
            help="Directory where perfume images will be written.",
        )

    def handle(self, *args, **options):
        result = extract_images_from_raw_dir(
            options["raw_dir"],
            options["output_dir"],
            perfume_detail_id_resolver=resolve_perfume_detail_id,
        )
        synced = 0
        for image in result.images:
            if not image.perfume_detail_id:
                continue
            if sync_image_to_database(image):
                synced += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Perfume image extraction finished: "
                f"{result.created} created, {result.skipped} skipped, "
                f"{result.failed} failed, {synced} synced."
            )
        )
        for failure in result.failures[:20]:
            self.stdout.write(
                self.style.WARNING(
                    "Image download failed: "
                    f"{failure.brand} / {failure.english_name} / "
                    f"{failure.image_url} / {failure.reason}"
                )
            )


def resolve_perfume_detail_id(record):
    brand_name = str(record.get("brand") or "").strip().upper()
    english_name = (
        record.get("english_name")
        or record.get("normalized_name")
        or record.get("korean_name")
    )
    if not brand_name or not english_name:
        return None

    perfume = (
        Perfume.objects.filter(brand__name=brand_name, english_name=english_name)
        .select_related("detail")
        .first()
    )
    if not perfume:
        return None

    detail = getattr(perfume, "detail", None)
    return getattr(detail, "id", None)


def sync_image_to_database(image):
    base64_data = ""
    if image.processed_path and is_enabled(os.getenv("PERFUME_IMAGE_STORE_BASE64", "true")):
        base64_data = encode_file_to_base64(image.processed_path)

    PerfumeImage.objects.update_or_create(
        perfume_detail_id=image.perfume_detail_id,
        original_url=image.original_url,
        defaults={
            "processed_path": image.processed_path,
            "base64_data": base64_data,
        },
    )

    return True


def encode_file_to_base64(path):
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def is_enabled(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}
