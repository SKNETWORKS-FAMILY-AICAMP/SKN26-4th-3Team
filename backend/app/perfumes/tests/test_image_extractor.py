"""
@file test_image_extractor.py
@role
향수 이미지 추출 및 이미지 URL backfill 로직을 검증하는 테스트 파일입니다.
raw JSON 기반 이미지 다운로드, 기존 파일 skip, 실패 URL 기록, Fragrantica parser를 다룹니다.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from django.test import TestCase

from perfumes.services.image_extractor import extract_images_from_raw_dir
from perfumes.services.fragrantica_image_backfill import (
    backfill_raw_files,
    parse_designer_catalog,
    parse_product_page_image_url,
)

class PerfumeImageExtractorTest(TestCase):
    def test_extracts_images_from_raw_json_into_brand_directories(self):
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            raw_dir = tmp_path / "raw"
            output_dir = tmp_path / "static" / "perfumes" / "images"
            raw_dir.mkdir()
            raw_file = raw_dir / "sample_fragrance_data.json"
            raw_file.write_text(
                json.dumps(
                    [
                        {
                            "perfume_detail_id": 42,
                            "brand": "BVLGARI",
                            "english_name": "Aqva Amara",
                            "image_url": "https://example.com/images/aqva.jpg",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            def downloader(url):
                return b"image-bytes", "image/jpeg"

            updated_at = datetime(2026, 5, 13, tzinfo=timezone.utc)
            result = extract_images_from_raw_dir(
                raw_dir,
                output_dir,
                downloader=downloader,
                clock=lambda: updated_at,
            )

            self.assertEqual(result.created, 1)
            self.assertEqual(result.skipped, 0)
            self.assertEqual(result.failed, 0)
            image_files = list((output_dir / "bvlgari").glob("aqva-amara-*.jpg"))
            self.assertEqual(len(image_files), 1)
            self.assertEqual(image_files[0].read_bytes(), b"image-bytes")
            self.assertEqual(len(result.images), 1)
            self.assertEqual(
                result.images[0].as_db_row(),
                {
                    "perfume_detail_id": 42,
                    "original_url": "https://example.com/images/aqva.jpg",
                    "processed_path": image_files[0].as_posix(),
                    "updated_at": updated_at,
                },
            )

    def test_skips_existing_images_without_downloading_again(self):
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            raw_dir = tmp_path / "raw"
            output_dir = tmp_path / "static" / "perfumes" / "images"
            target_dir = output_dir / "bvlgari"
            raw_dir.mkdir()
            target_dir.mkdir(parents=True)
            raw_file = raw_dir / "sample_fragrance_data.json"
            raw_file.write_text(
                json.dumps(
                    [
                        {
                            "perfume_detail_id": 42,
                            "brand": "BVLGARI",
                            "english_name": "Aqva Amara",
                            "image_url": "https://example.com/images/aqva.jpg",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            first = extract_images_from_raw_dir(
                raw_dir,
                output_dir,
                downloader=lambda url: (b"image-bytes", "image/jpeg"),
            )

            def fail_if_called(url):
                raise AssertionError("downloader should not be called for existing image")

            updated_at = datetime(2026, 5, 13, tzinfo=timezone.utc)
            second = extract_images_from_raw_dir(
                raw_dir,
                output_dir,
                downloader=fail_if_called,
                clock=lambda: updated_at,
            )

            self.assertEqual(first.created, 1)
            self.assertEqual(second.created, 0)
            self.assertEqual(second.skipped, 1)
            image_files = list((output_dir / "bvlgari").glob("aqva-amara-*.jpg"))
            self.assertEqual(
                second.images[0].as_db_row(),
                {
                    "perfume_detail_id": 42,
                    "original_url": "https://example.com/images/aqva.jpg",
                    "processed_path": image_files[0].as_posix(),
                    "updated_at": updated_at,
                },
            )

    def test_records_failed_image_url_for_database_sync(self):
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            raw_dir = tmp_path / "raw"
            output_dir = tmp_path / "static" / "perfumes" / "images"
            raw_dir.mkdir()
            raw_file = raw_dir / "sample_fragrance_data.json"
            raw_file.write_text(
                json.dumps(
                    [
                        {
                            "perfume_detail_id": 42,
                            "brand": "JOMALONE",
                            "english_name": "Blackberry & Bay Cologne",
                            "image_url": "https://example.com/blocked.png",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            def blocked_downloader(url):
                raise RuntimeError("403 forbidden")

            updated_at = datetime(2026, 5, 13, tzinfo=timezone.utc)
            result = extract_images_from_raw_dir(
                raw_dir,
                output_dir,
                downloader=blocked_downloader,
                clock=lambda: updated_at,
            )

            self.assertEqual(result.created, 0)
            self.assertEqual(result.failed, 1)
            self.assertEqual(len(result.images), 1)
            self.assertEqual(
                result.images[0].as_db_row(),
                {
                    "perfume_detail_id": 42,
                    "original_url": "https://example.com/blocked.png",
                    "processed_path": "",
                    "updated_at": updated_at,
                },
            )

    def test_backfills_fragrantica_image_urls_from_designer_catalog(self):
        designer_html = """
        <a href="/perfume/Maison-Francis-Kurkdjian/724-75754.html"
           class="group prefumeHbox tw-gridlist-card-base">
          <picture>
            <source type="image/jpeg"
              srcset="https://fimgs.net/mdimg/perfume-thumbs/270x270.75754.jpg 1x">
            <img src="https://fimgs.net/mdimg/perfume-thumbs/270x270.75754.jpg"
              alt="perfume 724">
          </picture>
          <h3 class="tw-grid-perfume-title">724</h3>
        </a>
        """
        catalog = parse_designer_catalog(
            designer_html,
            base_url="https://www.fragrantica.com/designers/Maison-Francis-Kurkdjian.html",
        )

        self.assertEqual(
            catalog["724"].image_url,
            "https://fimgs.net/mdimg/perfume-thumbs/270x270.75754.jpg",
        )
        self.assertEqual(
            catalog["724"].page_url,
            "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/724-75754.html",
        )

    def test_backfills_raw_file_image_url_and_product_url(self):
        with TemporaryDirectory() as tmpdir:
            raw_dir = Path(tmpdir) / "raw"
            raw_dir.mkdir()
            raw_file = raw_dir / "mfk_fragrantica_fragrance_data.json"
            raw_file.write_text(
                json.dumps(
                    [
                        {
                            "source": "fragrantica",
                            "brand": "MAISON FRANCIS KURKDJIAN",
                            "english_name": "724",
                            "product_url": "https://www.fragrantica.com/perfume/maison-francis-kurkdjian/724.html",
                            "image_url": "",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            def fetcher(url):
                self.assertEqual(
                    url,
                    "https://www.fragrantica.com/designers/Maison-Francis-Kurkdjian.html",
                )
                return """
                <a href="/perfume/Maison-Francis-Kurkdjian/724-75754.html"
                   class="group prefumeHbox tw-gridlist-card-base">
                  <img src="https://fimgs.net/mdimg/perfume-thumbs/270x270.75754.jpg">
                  <h3 class="tw-grid-perfume-title">724</h3>
                </a>
                """

            result = backfill_raw_files(raw_dir, fetcher=fetcher)

            self.assertEqual(result.checked, 1)
            self.assertEqual(result.updated, 1)
            updated = json.loads(raw_file.read_text(encoding="utf-8"))[0]
            self.assertEqual(
                updated["image_url"],
                "https://fimgs.net/mdimg/perfume-thumbs/270x270.75754.jpg",
            )
            self.assertEqual(
                updated["product_url"],
                "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/724-75754.html",
            )

    def test_parses_product_page_json_ld_image(self):
        html_text = """
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "Product",
          "name": "Chance",
          "image": "https://www.chanel.com/images/chance-packshot.jpg"
        }
        </script>
        """

        self.assertEqual(
            parse_product_page_image_url(html_text),
            "https://www.chanel.com/images/chance-packshot.jpg",
        )


# ----------------------------------------------------------------
# Update History
# 2026-05-18: tests.py에서 PerfumeImageExtractorTest를 분리하고 파일 역할 header/footer 추가. (worker: nobrain711)
# ----------------------------------------------------------------

# EOF: test_image_extractor.py
