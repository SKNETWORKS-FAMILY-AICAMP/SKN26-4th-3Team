import json
import base64
from datetime import datetime, timezone
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.core.exceptions import FieldDoesNotExist
from django.test import override_settings

from perfumes.models import Brand, Perfume, PerfumeDetail, PerfumeImage
from perfumes.services.image_extractor import PerfumeImageMapping, extract_images_from_raw_dir

class AnalyzeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('analyze') 
        self.session_id = "test-session-uuid"

    @patch('scent_engine.VLEngine.analyze_image')
    def test_analyze_success(self, mock_analyze):
        # Mock VLM response
        mock_analyze.return_value = {
            "visual_summary": "검은색 슈트를 입은 세련된 남성",
            "colors": ["black"],
            "objects": ["suit"],
            "scene": ["indoor"],
            "mood": ["urban", "modern"],
            "season": ["autumn"],
            "time": ["night"],
            "raw_keywords": ["chic", "sharp"]
        }

        # Mock Image (1x1 white pixel)
        small_img = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xff\xff\xff\x3f\x00\x05\xfe\x02\xfe\x0dcD\x01\x00\x00\x00\x00IEND\xaeB`\x82').decode()
        
        data = {
            "image": small_img,
            "selectedNotes": ["베르가못", "샌달우드"]
        }
        
        headers = {'HTTP_X_SESSION_ID': self.session_id}
        response = self.client.post(self.url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('recommendations', response.data)
        self.assertIn('radarScores', response.data['analysisMetadata'])
        print(f"Test Success: {response.data['fashionStyle']}")

    def test_analyze_missing_session_id(self):
        data = {"image": "dummy", "selectedNotes": []}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


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


class PerfumeDataModelTest(TestCase):
    def test_load_perfumes_populates_normalized_detail_and_raw_data(self):
        with TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            raw_dir = base_dir / "data" / "raw"
            raw_dir.mkdir(parents=True)
            raw_file = raw_dir / "sample_fragrance_data.json"
            raw_record = {
                "brand": "BVLGARI",
                "korean_name": "아쿠아 아마라",
                "english_name": "Aqva Amara",
                "product_subtype": "perfume",
                "family": "FRESH",
                "accords": ["citrus"],
                "notes": ["orange"],
                "keywords": ["fresh"],
                "image_url": "https://example.com/images/aqva.jpg",
                "source_url": "https://example.com/products/aqva",
                "meta": {"release_year": 2014},
            }
            raw_file.write_text(json.dumps([raw_record]), encoding="utf-8")

            with override_settings(BASE_DIR=base_dir):
                call_command("load_perfumes", verbosity=0)

        perfume = Perfume.objects.get(english_name="Aqva Amara")
        self.assertEqual(perfume.brand.name, "BVLGARI")
        with self.assertRaises(FieldDoesNotExist):
            Perfume._meta.get_field("data")
        self.assertEqual(perfume.detail.data["image_url"], raw_record["image_url"])
        self.assertEqual(perfume.raw_data.raw_json["english_name"], "Aqva Amara")
        self.assertEqual(perfume.raw_data.source_url, raw_record["source_url"])

    @patch("perfumes.management.commands.extract_perfume_images.extract_images_from_raw_dir")
    def test_extract_perfume_images_syncs_downloaded_images_to_database(self, mock_extract):
        brand = Brand.objects.create(name="BVLGARI")
        perfume = Perfume.objects.create(
            brand=brand,
            korean_name="아쿠아 아마라",
            english_name="Aqva Amara",
            product_type="perfume",
            family="프레시",
        )
        detail = PerfumeDetail.objects.create(perfume=perfume, data={})
        updated_at = datetime(2026, 5, 13, tzinfo=timezone.utc)
        mock_extract.return_value.created = 1
        mock_extract.return_value.skipped = 0
        mock_extract.return_value.failed = 0
        mock_extract.return_value.images = [
            PerfumeImageMapping(
                perfume_detail_id=detail.id,
                original_url="https://example.com/images/aqva.jpg",
                processed_path="/backend/app/static/perfumes/images/bvlgari/aqva.jpg",
                updated_at=updated_at,
            )
        ]

        call_command("extract_perfume_images", verbosity=0)

        image = PerfumeImage.objects.get(perfume_detail=detail)
        self.assertEqual(image.original_url, "https://example.com/images/aqva.jpg")
        self.assertEqual(
            image.processed_path,
            "/backend/app/static/perfumes/images/bvlgari/aqva.jpg",
        )
