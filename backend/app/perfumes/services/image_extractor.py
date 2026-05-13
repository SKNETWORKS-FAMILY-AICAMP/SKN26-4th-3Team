import hashlib
import json
import re
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any
from typing import Callable
from urllib.parse import urlparse

import requests


ImageDownloader = Callable[[str], tuple[bytes, str]]
Clock = Callable[[], datetime]
PerfumeDetailIdResolver = Callable[[dict[str, Any]], Any]


@dataclass(frozen=True)
class PerfumeImageMapping:
    perfume_detail_id: Any
    original_url: str
    processed_path: str
    updated_at: datetime

    def as_db_row(self) -> dict[str, Any]:
        return {
            "perfume_detail_id": self.perfume_detail_id,
            "original_url": self.original_url,
            "processed_path": self.processed_path,
            "updated_at": self.updated_at,
        }


@dataclass
class ExtractionResult:
    created: int = 0
    skipped: int = 0
    failed: int = 0
    images: list[PerfumeImageMapping] = field(default_factory=list)


CONTENT_TYPE_EXTENSIONS = {
    "image/avif": "avif",
    "image/gif": "gif",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}
ALLOWED_EXTENSIONS = {"avif", "gif", "jpeg", "jpg", "png", "webp"}


def default_downloader(url: str) -> tuple[bytes, str]:
    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "olfit-image-extractor/1.0"},
    )
    response.raise_for_status()
    return response.content, response.headers.get("Content-Type", "")


def extract_images_from_raw_dir(
    raw_dir: str | Path,
    output_dir: str | Path,
    *,
    downloader: ImageDownloader = default_downloader,
    clock: Clock = lambda: datetime.now(timezone.utc),
    perfume_detail_id_resolver: PerfumeDetailIdResolver | None = None,
) -> ExtractionResult:
    raw_path = Path(raw_dir)
    output_path = Path(output_dir)
    result = ExtractionResult()

    for json_path in sorted(raw_path.glob("*_fragrance_data.json")):
        try:
            records = json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            result.failed += 1
            continue

        if not isinstance(records, list):
            result.failed += 1
            continue

        for record in records:
            if not isinstance(record, dict):
                continue

            image_url = str(record.get("image_url") or "").strip()
            if not image_url:
                continue

            brand_dir = output_path / slugify(record.get("brand") or "unknown")
            filename_base = slugify(
                record.get("english_name")
                or record.get("normalized_name")
                or record.get("korean_name")
                or "unknown"
            )
            url_hash = hashlib.sha1(image_url.encode("utf-8")).hexdigest()[:10]
            existing = list(brand_dir.glob(f"{filename_base}-{url_hash}.*"))
            if existing:
                result.skipped += 1
                result.images.append(
                    build_image_mapping(record, image_url, existing[0], clock, perfume_detail_id_resolver)
                )
                continue

            try:
                content, content_type = downloader(image_url)
                extension = extension_for(image_url, content_type)
                brand_dir.mkdir(parents=True, exist_ok=True)
                image_path = brand_dir / f"{filename_base}-{url_hash}.{extension}"
                image_path.write_bytes(content)
                result.created += 1
                result.images.append(
                    build_image_mapping(record, image_url, image_path, clock, perfume_detail_id_resolver)
                )
            except Exception:
                result.failed += 1

    return result


def build_image_mapping(
    record: dict[str, Any],
    image_url: str,
    image_path: Path,
    clock: Clock,
    perfume_detail_id_resolver: PerfumeDetailIdResolver | None = None,
) -> PerfumeImageMapping:
    perfume_detail_id = (
        perfume_detail_id_resolver(record)
        if perfume_detail_id_resolver is not None
        else record.get("perfume_detail_id")
    )
    return PerfumeImageMapping(
        perfume_detail_id=perfume_detail_id,
        original_url=image_url,
        processed_path=image_path.as_posix(),
        updated_at=clock(),
    )


def slugify(value: object) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "unknown"


def extension_for(url: str, content_type: str) -> str:
    media_type = content_type.split(";", 1)[0].strip().lower()
    if media_type in CONTENT_TYPE_EXTENSIONS:
        return CONTENT_TYPE_EXTENSIONS[media_type]

    suffix = Path(urlparse(url).path).suffix.lower().lstrip(".")
    if suffix in ALLOWED_EXTENSIONS:
        return "jpg" if suffix == "jpeg" else suffix

    return "jpg"
