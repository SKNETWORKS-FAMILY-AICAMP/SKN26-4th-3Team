"""
@file test_load_perfumes.py
@role
raw perfume data 로드와 이미지 추출 command의 DB 동기화를 검증하는 테스트 파일입니다.
Perfume, PerfumeDetail, PerfumeRawData 정규화 및 갱신 흐름을 다룹니다.
"""

import base64
import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.exceptions import FieldDoesNotExist
from django.core.management import call_command
from django.test import TestCase, override_settings

from perfumes.models import Brand, Perfume, PerfumeDetail, PerfumeImage, PerfumeRawData
from perfumes.services.image_extractor import PerfumeImageMapping

class PerfumeDataModelTest(TestCase):
    @patch("perfumes.management.commands.load_perfumes.load_master_map")
    def test_load_perfumes_populates_normalized_detail_and_raw_data(self, mock_master_map):
        mock_master_map.return_value = {
            "accord_to_category": {"citrus": "프레시"},
            "note_to_accord": {"오렌지": "citrus"},
            "note_translations": {"orange": "오렌지"},
        }
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
        self.assertEqual(perfume.detail.data["aura_profile"]["프레시"], 1.0)
        self.assertNotIn("brand", perfume.detail.data)
        self.assertNotIn("korean_name", perfume.detail.data)
        self.assertNotIn("english_name", perfume.detail.data)
        self.assertNotIn("product_type", perfume.detail.data)
        self.assertNotIn("product_subtype", perfume.detail.data)
        self.assertNotIn("family", perfume.detail.data)
        self.assertNotIn("image_url", perfume.detail.data)
        self.assertNotIn("product_url", perfume.detail.data)
        self.assertNotIn("release_year", perfume.detail.data.get("meta", {}))
        self.assertEqual(perfume.release_year, 2014)
        self.assertEqual(perfume.raw_data.raw_json["english_name"], "Aqva Amara")
        self.assertEqual(perfume.raw_data.raw_json["meta"]["release_year"], 2014)
        self.assertNotIn("source_url", perfume.raw_data.raw_json)
        with self.assertRaises(FieldDoesNotExist):
            PerfumeRawData._meta.get_field("source_url")

    @patch("perfumes.management.commands.load_perfumes.load_master_map")
    def test_load_perfumes_updates_existing_perfume_raw_data(self, mock_master_map):
        mock_master_map.return_value = {
            "accord_to_category": {"우디": "우디", "프레쉬": "프레시"},
            "note_to_accord": {"대나무": "우디"},
            "note_translations": {"대나무": "대나무"},
        }
        brand = Brand.objects.create(name="BVLGARI")
        perfume = Perfume.objects.create(
            brand=brand,
            korean_name="기존 이름",
            english_name="omnia crystalline",
            product_type="perfume",
            family="프레시",
        )
        PerfumeDetail.objects.create(perfume=perfume, data={})
        PerfumeRawData.objects.create(perfume=perfume, raw_json={})

        raw_record = {
            "source": "fraganty",
            "source_country": "IT",
            "brand": "BVLGARI",
            "korean_name": "옴니아 크리스탈린",
            "english_name": "omnia crystalline",
            "normalized_name": "omnia crystalline",
            "product_type": "perfume",
            "product_subtype": "perfume",
            "product_url": "https://fraganty.ai/perfume/omnia-crystalline",
            "image_url": "https://img.fraganty.ai/perfume/152.jpg",
            "notes": ["대나무"],
            "accords": ["우디", "프레쉬"],
            "keywords": ["상쾌한"],
            "meta": {"release_year": None},
            "volume": "65ml",
            "family": "우디",
            "aura_profile": {
                "플로럴": 0.125,
                "우디": 0.125,
                "오리엔탈": 0.125,
                "프레시": 0.5,
                "구르망": 0.125,
            },
        }

        with TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            raw_dir = base_dir / "data" / "raw"
            raw_dir.mkdir(parents=True)
            (raw_dir / "bvlgari_fraganty_fragrance_data.json").write_text(
                json.dumps([raw_record]),
                encoding="utf-8",
            )
            with override_settings(BASE_DIR=base_dir):
                call_command("load_perfumes", verbosity=0)

        perfume.refresh_from_db()
        self.assertEqual(perfume.korean_name, "옴니아 크리스탈린")
        self.assertEqual(perfume.detail.data["volume"], "65ml")
        self.assertEqual(perfume.detail.data["aura_profile"]["프레시"], 0.5547)
        self.assertNotIn("brand", perfume.detail.data)
        self.assertNotIn("korean_name", perfume.detail.data)
        self.assertNotIn("english_name", perfume.detail.data)
        self.assertNotIn("image_url", perfume.detail.data)
        self.assertNotIn("product_url", perfume.detail.data)
        self.assertNotIn("release_year", perfume.detail.data.get("meta", {}))
        self.assertEqual(perfume.raw_data.raw_json["product_url"], raw_record["product_url"])
        self.assertEqual(perfume.raw_data.raw_json["image_url"], raw_record["image_url"])
        self.assertNotIn("source_url", perfume.raw_data.raw_json)

    @patch("perfumes.management.commands.extract_perfume_images.extract_images_from_raw_dir")
    def test_extract_perfume_images_syncs_downloaded_images_to_database(self, mock_extract):
        with TemporaryDirectory() as tmpdir:
            image_path = Path(tmpdir) / "aqva.jpg"
            image_path.write_bytes(b"image-bytes")
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
                    processed_path=image_path.as_posix(),
                    updated_at=updated_at,
                )
            ]

            call_command("extract_perfume_images", verbosity=0)

            image = PerfumeImage.objects.get(perfume_detail=detail)
            self.assertEqual(image.original_url, "https://example.com/images/aqva.jpg")
            self.assertEqual(image.processed_path, image_path.as_posix())
            self.assertEqual(image.base64_data, base64.b64encode(b"image-bytes").decode("ascii"))

            detail.refresh_from_db()
            self.assertNotIn("image_asset", detail.data)


# ----------------------------------------------------------------
# Update History
# 2026-05-18: tests.py에서 PerfumeDataModelTest를 분리하고 파일 역할 header/footer 추가. (worker: nobrain711)
# ----------------------------------------------------------------

# EOF: test_load_perfumes.py


