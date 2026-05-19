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
    """이미지 추출 서비스와 Fragrantica image URL backfill parser를 검증한다."""

    def test_extracts_images_from_raw_json_into_brand_directories(self):
        """raw JSON의 image_url을 브랜드 디렉터리 아래 이미지 파일로 저장하는지 확인한다."""
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
                """테스트용 이미지 bytes와 content type을 반환한다."""
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
        """동일 이미지 파일이 이미 있으면 downloader 호출 없이 skip하는지 확인한다."""
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
                """기존 파일이 있을 때 downloader가 호출되면 테스트를 실패시킨다."""
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
        """이미지 다운로드 실패도 DB 동기화용 빈 processed_path mapping으로 남기는지 확인한다."""
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
                """차단된 이미지 URL을 시뮬레이션한다."""
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
        """Fragrantica designer catalog HTML에서 상품 이미지와 상세 URL을 추출하는지 확인한다."""
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
        """raw file의 빈 image_url/product_url을 catalog 후보로 보강하는지 확인한다."""
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
                """테스트용 Fragrantica catalog HTML을 반환한다."""
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
        """상품 상세 페이지 JSON-LD에서 대표 이미지 URL을 추출하는지 확인한다."""
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
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-18: test(perfumes): expand backend coverage and split test modules. (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: test_image_extractor.py
