"""
@file image_extractor.py
@role
Downloads, normalizes, and synchronizes perfume image assets from raw data sources.
"""

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
    """raw data 이미지 한 건을 PerfumeImage DB row로 동기화하기 위한 중간 표현."""

    perfume_detail_id: Any
    original_url: str
    processed_path: str
    updated_at: datetime

    def as_db_row(self) -> dict[str, Any]:
        """ORM bulk 작업에 사용할 수 있는 딕셔너리 형태로 변환한다."""
        return {
            "perfume_detail_id": self.perfume_detail_id,
            "original_url": self.original_url,
            "processed_path": self.processed_path,
            "updated_at": self.updated_at,
        }


@dataclass(frozen=True)
class ImageExtractionFailure:
    """이미지 다운로드 또는 저장 실패 정보를 기록한다."""

    brand: str
    english_name: str
    image_url: str
    reason: str


@dataclass
class ExtractionResult:
    """이미지 추출 작업의 집계 결과와 동기화 대상 목록을 담는다."""

    created: int = 0
    skipped: int = 0
    failed: int = 0
    images: list[PerfumeImageMapping] = field(default_factory=list)
    failures: list[ImageExtractionFailure] = field(default_factory=list)


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
    """requests로 이미지를 내려받고, 403 응답은 Scrapling 기반 downloader로 재시도한다."""
    try:
        response = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "olfit-image-extractor/1.0"},
        )
        response.raise_for_status()
        return response.content, response.headers.get("Content-Type", "")
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        if status_code != 403:
            raise

    return scrapling_downloader(url)


def scrapling_downloader(url: str) -> tuple[bytes, str]:
    """Scrapling Fetcher를 사용해 bot 차단 가능성이 있는 이미지 URL을 내려받는다."""
    try:
        from scrapling.fetchers import Fetcher
    except ImportError as exc:
        raise RuntimeError("Scrapling fetchers are not installed") from exc

    page = Fetcher.get(
        url,
        impersonate="chrome",
        http3=False,
        stealthy_headers=True,
        timeout=30,
        retries=2,
    )

    if page.status >= 400:
        raise RuntimeError(f"Scrapling fetch failed with HTTP {page.status}: {page.reason}")

    content_type = page.headers.get("content-type") or page.headers.get("Content-Type") or ""
    return page.body, content_type


def extract_images_from_raw_dir(
    raw_dir: str | Path,
    output_dir: str | Path,
    *,
    downloader: ImageDownloader = default_downloader,
    clock: Clock = lambda: datetime.now(timezone.utc),
    perfume_detail_id_resolver: PerfumeDetailIdResolver | None = None,
) -> ExtractionResult:
    """raw perfume JSON 디렉터리에서 이미지 URL을 찾아 정적 파일로 저장한다."""
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
            except Exception as exc:
                result.failed += 1
                result.images.append(
                    PerfumeImageMapping(
                        perfume_detail_id=resolve_perfume_detail_id(record, perfume_detail_id_resolver),
                        original_url=image_url,
                        processed_path="",
                        updated_at=clock(),
                    )
                )
                result.failures.append(
                    ImageExtractionFailure(
                        brand=str(record.get("brand") or ""),
                        english_name=str(
                            record.get("english_name")
                            or record.get("normalized_name")
                            or record.get("korean_name")
                            or ""
                        ),
                        image_url=image_url,
                        reason=str(exc),
                    )
                )

    return result


def build_image_mapping(
    record: dict[str, Any],
    image_url: str,
    image_path: Path,
    clock: Clock,
    perfume_detail_id_resolver: PerfumeDetailIdResolver | None = None,
) -> PerfumeImageMapping:
    """저장된 이미지 파일 경로와 원본 record를 DB 동기화용 mapping으로 묶는다."""
    perfume_detail_id = (
        resolve_perfume_detail_id(record, perfume_detail_id_resolver)
    )
    return PerfumeImageMapping(
        perfume_detail_id=perfume_detail_id,
        original_url=image_url,
        processed_path=image_path.as_posix(),
        updated_at=clock(),
    )


def resolve_perfume_detail_id(
    record: dict[str, Any],
    perfume_detail_id_resolver: PerfumeDetailIdResolver | None = None,
) -> Any:
    """외부 resolver가 있으면 사용하고, 없으면 record의 perfume_detail_id를 반환한다."""
    if perfume_detail_id_resolver is not None:
        return perfume_detail_id_resolver(record)
    return record.get("perfume_detail_id")


def slugify(value: object) -> str:
    """브랜드명과 상품명을 파일/디렉터리 이름에 안전한 slug로 변환한다."""
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "unknown"


def extension_for(url: str, content_type: str) -> str:
    """Content-Type을 우선하고 URL suffix를 fallback으로 사용해 이미지 확장자를 결정한다."""
    media_type = content_type.split(";", 1)[0].strip().lower()
    if media_type in CONTENT_TYPE_EXTENSIONS:
        return CONTENT_TYPE_EXTENSIONS[media_type]

    suffix = Path(urlparse(url).path).suffix.lower().lstrip(".")
    if suffix in ALLOWED_EXTENSIONS:
        return "jpg" if suffix == "jpeg" else suffix

    return "jpg"

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-13: feat(perfumes): persist perfume image assets. (author: @nobrain711)
# 2026-05-13: fix(django): guard migrate schema drift. (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: image_extractor.py
