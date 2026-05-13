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
            PerfumeImage.objects.update_or_create(
                perfume_detail_id=image.perfume_detail_id,
                original_url=image.original_url,
                defaults={"processed_path": image.processed_path},
            )
            synced += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Perfume image extraction finished: "
                f"{result.created} created, {result.skipped} skipped, "
                f"{result.failed} failed, {synced} synced."
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
