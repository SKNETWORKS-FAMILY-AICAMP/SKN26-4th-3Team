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

from perfumes.models import Brand, Perfume, PerfumeDetail, PerfumeImage, PerfumeRawData
from perfumes.services.image_extractor import PerfumeImageMapping, extract_images_from_raw_dir
from perfumes.services.fragrantica_image_backfill import (
    backfill_raw_files,
    parse_designer_catalog,
    parse_product_page_image_url,
)
from perfumes.services.recommendation_service import RecommendationService

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


class PerfumeDataModelTest(TestCase):
    @patch("perfumes.management.commands.load_perfumes.load_master_map")
    def test_load_perfumes_populates_normalized_detail_and_raw_data(self, mock_master_map):
        mock_master_map.return_value = {
            "accord_to_category": {"citrus": "프레시"},
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
        self.assertEqual(perfume.detail.data["aura_profile"]["프레시"], 0.5)
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


class RecommendationServiceTest(TestCase):
    def test_recommendations_include_perfume_detail_and_image_payload(self):
        brand = Brand.objects.create(name="BVLGARI")
        perfume = Perfume.objects.create(
            brand=brand,
            korean_name="옴니아 크리스탈린",
            english_name="omnia crystalline",
            product_type="perfume",
            family="프레시",
            release_year=2005,
        )
        detail = PerfumeDetail.objects.create(
            perfume=perfume,
            data={
                "price": {"raw": "$150", "amount": 150, "currency": "USD"},
                "description": "옴니아 크리스탈린 설명",
                "notes": ["대나무", "서양배", "연꽃"],
                "representative_notes": ["대나무", "서양배"],
<<<<<<< HEAD
                "notes_parsed": {
                    "top": ["대나무"],
                    "middle": ["서양배"],
                    "base": ["연꽃"],
                },
=======
>>>>>>> 32ea455 (feat(api): include perfume details in recommendations)
                "accords": ["우디", "플로럴"],
                "keywords": {"ko": ["상쾌한", "우아한"], "en": ["Refreshing"]},
                "aura_profile": {
                    "플로럴": 0.1,
                    "우디": 0.1,
                    "오리엔탈": 0.1,
                    "프레시": 0.6,
                    "구르망": 0.1,
                },
                "volume": "65ml",
                "meta": {"original_country": "이탈리아"},
            },
        )
        PerfumeImage.objects.create(
            perfume_detail=detail,
            original_url="https://img.example.com/omnia.jpg",
            processed_path="/backend/app/static/perfumes/images/bvlgari/omnia.jpg",
            base64_data="base64-image",
        )

        service = RecommendationService()
        result = service.recommend(
            {"플로럴": 0.1, "우디": 0.1, "오리엔탈": 0.1, "프레시": 0.6, "구르망": 0.1},
            "",
            ["대나무"],
        )

        self.assertEqual(len(result), 1)
        recommendation = result[0]
        self.assertEqual(recommendation["perfume"]["koreanName"], "옴니아 크리스탈린")
        self.assertEqual(recommendation["perfume"]["price"]["raw"], "$150")
        self.assertEqual(recommendation["perfume"]["description"], "옴니아 크리스탈린 설명")
        self.assertEqual(recommendation["perfume"]["notes"], ["대나무", "서양배", "연꽃"])
        self.assertEqual(recommendation["perfume"]["accords"], ["우디", "플로럴"])
        self.assertEqual(recommendation["perfume"]["keywords"]["ko"], ["상쾌한", "우아한"])
<<<<<<< HEAD
        self.assertEqual(recommendation["details"]["topNotes"], "대나무")
        self.assertEqual(recommendation["details"]["middleNotes"], "서양배")
        self.assertEqual(recommendation["details"]["baseNotes"], "연꽃")
=======
>>>>>>> 32ea455 (feat(api): include perfume details in recommendations)
        self.assertEqual(
            recommendation["imageDetail"]["url"],
            "/static/perfumes/images/bvlgari/omnia.jpg",
        )
        self.assertEqual(recommendation["imageDetail"]["base64"], "base64-image")
        self.assertEqual(recommendation["image"], "/static/perfumes/images/bvlgari/omnia.jpg")
<<<<<<< HEAD

    def test_recommendations_split_flat_notes_when_parsed_notes_are_missing(self):
        brand = Brand.objects.create(name="LE LABO")
        perfume = Perfume.objects.create(
            brand=brand,
            korean_name="네롤리 36",
            english_name="neroli 36",
            product_type="perfume",
            family="프레시",
        )
        PerfumeDetail.objects.create(
            perfume=perfume,
            data={
                "description": "네롤리 36 설명",
                "notes": ["네롤리", "베르가못", "오렌지 블라썸", "시더우드", "나르가모타"],
                "representative_notes": ["네롤리", "베르가못", "오렌지 블라썸", "시더우드", "나르가모타"],
                "aura_profile": {
                    "플로럴": 0.1,
                    "우디": 0.1,
                    "오리엔탈": 0.1,
                    "프레시": 0.6,
                    "구르망": 0.1,
                },
            },
        )

        service = RecommendationService()
        result = service.recommend(
            {"플로럴": 0.1, "우디": 0.1, "오리엔탈": 0.1, "프레시": 0.6, "구르망": 0.1},
            "",
            ["네롤리"],
        )

        recommendation = result[0]
        self.assertEqual(recommendation["details"]["topNotes"], "네롤리, 베르가못")
        self.assertEqual(recommendation["details"]["middleNotes"], "오렌지 블라썸, 시더우드")
        self.assertEqual(recommendation["details"]["baseNotes"], "나르가모타")
=======
>>>>>>> 32ea455 (feat(api): include perfume details in recommendations)
