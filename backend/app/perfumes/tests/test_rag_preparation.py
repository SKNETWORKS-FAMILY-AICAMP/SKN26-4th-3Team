"""
@file test_rag_preparation.py
@role
RAG 추천 준비 단계의 query, embedding document, vector metadata 생성을 검증하는 테스트 파일입니다.
gold scenario와 experiment scenario가 AuraService의 RAG query 생성 경로를 통과하는지도 확인합니다.
"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, override_settings

from perfumes.models import Brand, Perfume, PerfumeDetail
from perfumes.services.aura_service import AuraService
from perfumes.management.commands.index_to_pinecone import Command as IndexToPineconeCommand

class RagPreparationTest(TestCase):
    RAG_GOLD_SCENARIOS = [
        {
            "brand": "BVLGARI",
            "english_name": "omnia crystalline",
            "korean_name": "옴니아 크리스탈린",
            "vlm_output": {
                "visual_summary": "맑은 물과 하얀 천이 어우러진 깨끗하고 평화로운 분위기입니다.",
                "mood": ["clean", "soft", "bright"],
            },
            "selected_notes": ["베르가못", "화이트 티", "머스크"],
        },
        {
            "brand": "CHANEL",
            "english_name": "bleu de chanel eau de parfum",
            "korean_name": "블루 드 샤넬 오 드 퍼퓸",
            "vlm_output": {
                "visual_summary": "어두운 밤 도시의 건물 사이로 푸른 조명이 비치는 세련된 풍경입니다.",
                "mood": ["modern", "dark", "urban", "luxurious"],
            },
            "selected_notes": ["레몬", "민트", "샌달우드"],
        },
        {
            "brand": "DIOR",
            "english_name": "hypnotic poison",
            "korean_name": "디올 힙노틱 쁘아종",
            "vlm_output": {
                "visual_summary": "붉은 조명 아래 부드러운 드레스를 입은 여성이 앉아있는 유혹적인 무드입니다.",
                "mood": ["sensual", "warm", "romantic"],
            },
            "selected_notes": ["바닐라", "자스민", "머스크"],
        },
        {
            "brand": "BYREDO",
            "english_name": "rose of no man's land",
            "korean_name": "로즈 오브 노 맨즈 랜드",
            "vlm_output": {
                "visual_summary": "건조한 땅 위에 짙은 붉은 장미 한 송이가 놓여있는 고독한 모습입니다.",
                "mood": ["romantic", "natural", "calm"],
            },
            "selected_notes": ["로즈", "핑크 페퍼", "앰버"],
        },
        {
            "brand": "LE LABO",
            "english_name": "santal 33",
            "korean_name": "상탈 33",
            "vlm_output": {
                "visual_summary": "오래된 나무 책상 위에 가죽 책들이 쌓여있는 빈티지한 서재의 모습입니다.",
                "mood": ["warm", "natural", "calm", "modern"],
            },
            "selected_notes": ["샌달우드", "가죽", "아이리스"],
        },
        {
            "brand": "JO MALONE",
            "english_name": "english pear & freesia",
            "korean_name": "잉글리쉬 페어 앤 프리지아",
            "vlm_output": {
                "visual_summary": "햇살 가득한 정원에 황금빛 과일과 하얀 꽃들이 가득 피어있습니다.",
                "mood": ["bright", "fresh", "soft", "romantic"],
            },
            "selected_notes": ["페어", "프리지아", "머스크"],
        },
        {
            "brand": "MAISON FRANCIS KURKDJIAN",
            "english_name": "baccarat rouge 540",
            "korean_name": "바카라 루쥬 540",
            "vlm_output": {
                "visual_summary": "화려한 샹들리에 조명이 빛나는 럭셔리한 호텔 연회장 내부입니다.",
                "mood": ["luxurious", "sensual", "elegant", "modern"],
            },
            "selected_notes": ["사프란", "앰버", "인센스"],
        },
        {
            "brand": "LUSH",
            "english_name": "dirty",
            "korean_name": "더티",
            "vlm_output": {
                "visual_summary": "차가운 파도가 부서지는 바닷가와 민트 잎이 흩날리는 시원한 풍경입니다.",
                "mood": ["clean", "fresh", "bright"],
            },
            "selected_notes": ["민트", "라벤더", "베티버"],
        },
        {
            "brand": "DIOR",
            "english_name": "j'adore",
            "korean_name": "쟈도르",
            "vlm_output": {
                "visual_summary": "금빛 드레스를 입은 여성이 꽃으로 가득 찬 화려한 방에 서 있습니다.",
                "mood": ["luxurious", "elegant", "romantic"],
            },
            "selected_notes": ["자스민", "오렌지 블라썸", "머스크"],
        },
        {
            "brand": "GIORGIO ARMANI",
            "english_name": "acqua di gio",
            "korean_name": "아쿠아 디 지오",
            "vlm_output": {
                "visual_summary": "지중해의 푸른 바다와 강렬한 햇살 아래 하얀 절벽이 보입니다.",
                "mood": ["fresh", "natural", "calm"],
            },
            "selected_notes": ["베르가못", "네롤리", "인센스"],
        },
        {
            "brand": "BYREDO",
            "english_name": "blanche",
            "korean_name": "블랑쉬",
            "vlm_output": {
                "visual_summary": "햇살 아래 하얀 빨래가 널려있는 깨끗하고 부드러운 분위기입니다.",
                "mood": ["clean", "soft", "bright"],
            },
            "selected_notes": ["알데하이드", "네롤리", "머스크"],
        },
        {
            "brand": "LE LABO",
            "english_name": "another 13",
            "korean_name": "ANOTHER13",
            "vlm_output": {
                "visual_summary": "회색빛 콘크리트와 하얀 셔츠가 어우러진 미니멀한 도시 이미지입니다.",
                "mood": ["modern", "urban", "calm", "clean"],
            },
            "selected_notes": ["머스크", "앰버", "자스민"],
        },
        {
            "brand": "CHANEL",
            "english_name": "chanel no 5 eau de parfum",
            "korean_name": "샤넬 N°5 오 드 퍼퓸",
            "vlm_output": {
                "visual_summary": "금빛 조명 아래 우아한 드레스를 입은 여성의 뒷모습입니다.",
                "mood": ["elegant", "luxurious", "sensual"],
            },
            "selected_notes": ["알데하이드", "자스민", "바닐라"],
        },
        {
            "brand": "CREED",
            "english_name": "aventus",
            "korean_name": "아벤투스",
            "vlm_output": {
                "visual_summary": "말을 타고 달리는 전사의 강인함과 성공한 남성의 자신감이 느껴집니다.",
                "mood": ["modern", "luxurious", "dark"],
            },
            "selected_notes": ["베르가못", "핑크 페퍼", "우드"],
        },
        {
            "brand": "DIPTYQUE",
            "english_name": "philosykos",
            "korean_name": "필로시코스",
            "vlm_output": {
                "visual_summary": "그리스의 뜨거운 햇살 아래 무화과 나무 그늘에서의 휴식입니다.",
                "mood": ["natural", "warm", "calm"],
            },
            "selected_notes": ["무화과", "샌달우드", "시더우드"],
        },
        {
            "brand": "TOM FORD",
            "english_name": "white suede",
            "korean_name": "화이트 스웨이드",
            "vlm_output": {
                "visual_summary": "하얀 가죽 장갑과 부드러운 니트가 어우러진 고급스러운 겨울 이미지입니다.",
                "mood": ["soft", "luxurious", "warm"],
            },
            "selected_notes": ["머스크", "가죽", "앰버"],
        },
        {
            "brand": "BYREDO",
            "english_name": "mojave ghost",
            "korean_name": "모하비 고스트",
            "vlm_output": {
                "visual_summary": "메마른 사막 위에 신비롭게 피어난 보랏빛 꽃의 우아한 자태입니다.",
                "mood": ["natural", "elegant", "calm"],
            },
            "selected_notes": ["아이리스", "샌달우드", "앰버"],
        },
        {
            "brand": "CHANEL",
            "english_name": "allure homme sport",
            "korean_name": "알뤼르 옴므 스포츠",
            "vlm_output": {
                "visual_summary": "푸른 바다 위에서 요트를 타고 속도감을 즐기는 남성의 활기찬 모습입니다.",
                "mood": ["fresh", "bright", "modern"],
            },
            "selected_notes": ["베르가못", "알데하이드", "베티버"],
        },
        {
            "brand": "MAISON FRANCIS KURKDJIAN",
            "english_name": "aqua universalis",
            "korean_name": "Aqua Universalis",
            "vlm_output": {
                "visual_summary": "눈부시게 하얀 세탁실에서 느껴지는 투명한 깨끗함과 신선한 공기입니다.",
                "mood": ["clean", "bright", "fresh"],
            },
            "selected_notes": ["베르가못", "레몬", "자스민"],
        },
        {
            "brand": "DIOR",
            "english_name": "sauvage",
            "korean_name": "디올 소바쥬",
            "vlm_output": {
                "visual_summary": "노을 지는 광활한 대지 위에서 자유롭게 서 있는 거친 남성적 이미지입니다.",
                "mood": ["dark", "sensual", "modern"],
            },
            "selected_notes": ["베르가못", "핑크 페퍼", "라벤더"],
        },
    ]

    EXPERIMENT_SCENARIOS = {
        "dual_aura_clash": {
            "vlm_output": {
                "visual_summary": "우아한 실크 드레스와 차분한 숲의 향기가 공존하는 신비로운 스타일.",
                "mood": ["luxurious", "calm", "natural"],
            },
            "selected_notes": ["장미", "샌달우드", "패출리"],
        },
        "citrus_fresh_boost": {
            "vlm_output": {
                "visual_summary": "청량한 바다와 상큼한 레몬이 느껴지는 스포티한 룩.",
                "mood": ["fresh", "bright", "clean"],
            },
            "selected_notes": ["레몬", "베르가못", "민트"],
        },
        "oriental_night": {
            "vlm_output": {
                "visual_summary": "화려한 야경과 벨벳 소재의 옷이 어울리는 고혹적인 밤.",
                "mood": ["sensual", "dark", "modern"],
            },
            "selected_notes": ["바닐라", "앰버", "침향"],
        },
    }

    @patch("perfumes.services.aura_service.map_image_to_fragrance_keywords")
    @patch("perfumes.services.aura_service.load_user_preference_map")
    @patch("perfumes.services.aura_service.load_master_map")
    def test_aura_service_generates_symmetric_query_for_rag(
        self,
        mock_master_map,
        mock_preference_map,
        mock_image_mapping,
    ):
        mock_master_map.return_value = {
            "accord_translations": {"urban": "도시적인", "modern": "모던한"},
            "accord_to_category": {"시트러스": "프레시"},
            "note_to_accord": {"베르가못": "시트러스"},
        }
        mock_preference_map.return_value = {
            "샌달우드": {"axis": "우디"},
        }
        mock_image_mapping.return_value = {
            "components_ko": ["베르가못"],
            "scores": {
                "families": [{"name": "FRESH", "score": 3.0}],
                "subs": [],
                "components_ko": [{"name": "베르가못", "score": 1.0}],
            },
        }
        vl_result = {
            "visual_summary": "검은색 슈트를 입은 세련된 남성",
            "mood": ["urban", "modern"],
        }

        _, _, query_text, search_vector = AuraService().calculate_combined_aura(
            vl_result,
            ["샌달우드"],
        )

        self.assertIn("검은색 슈트를 입은 세련된 남성", query_text)
        self.assertIn("도시적인, 모던한 분위기", query_text)
        self.assertIn("베르가못, 샌달우드 향", query_text)
        self.assertIn("계열 향수", query_text)
        self.assertGreater(search_vector["프레시"], 0)
        self.assertGreater(search_vector["우디"], 0)

    @patch("perfumes.management.commands.load_perfumes.load_master_map")
    def test_load_perfumes_persists_embedding_doc_for_rag(self, mock_master_map):
        mock_master_map.return_value = {
            "accord_to_category": {"시트러스": "프레시", "우디": "우디"},
            "note_to_accord": {"베르가못": "시트러스", "샌달우드": "우디"},
            "note_translations": {"bergamot": "베르가못", "sandalwood": "샌달우드"},
        }
        raw_record = {
            "brand": "CREED",
            "korean_name": "어벤투스",
            "english_name": "Aventus",
            "product_subtype": "perfume",
            "family": "FRESH",
            "description": "강렬하고 산뜻한 시트러스 우디 향.",
            "accords": ["시트러스"],
            "notes": ["bergamot", "sandalwood"],
            "keywords": ["세련된", "자신감"],
            "meta": {"release_year": 2010},
        }

        with TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            raw_dir = base_dir / "data" / "raw"
            raw_dir.mkdir(parents=True)
            (raw_dir / "creed_fragrance_data.json").write_text(
                json.dumps([raw_record]),
                encoding="utf-8",
            )
            with override_settings(BASE_DIR=base_dir):
                call_command("load_perfumes", verbosity=0)

        detail_data = Perfume.objects.get(english_name="Aventus").detail.data
        embedding_doc = detail_data["embedding_doc"]

        self.assertIn("CREED 어벤투스", embedding_doc)
        self.assertIn("강렬하고 산뜻한 시트러스 우디 향", embedding_doc)
        self.assertIn("시트러스 분위기", embedding_doc)
        self.assertIn("베르가못, 샌달우드 향", embedding_doc)
        self.assertIn("프레시 계열 향수", embedding_doc)
        self.assertIn("#세련된 #자신감", embedding_doc)

    def test_index_to_pinecone_metadata_contains_reranking_fields(self):
        brand = Brand.objects.create(name="CREED")
        perfume = Perfume.objects.create(
            brand=brand,
            korean_name="어벤투스",
            english_name="Aventus",
            product_type="perfume",
            family="프레시",
            release_year=2010,
        )
        PerfumeDetail.objects.create(
            perfume=perfume,
            data={
                "price": {"raw": "$150", "amount": 150, "currency": "USD"},
                "volume": "100ml",
                "description": "강렬하고 산뜻한 시트러스 우디 향.",
                "accords": ["시트러스", "우디"],
                "representative_notes": ["베르가못", "샌달우드"],
                "notes_parsed": {
                    "top": ["베르가못"],
                    "middle": ["파인애플"],
                    "base": ["샌달우드"],
                },
                "keywords": ["세련된", "자신감"],
                "aura_profile": {
                    "플로럴": 0.1,
                    "우디": 0.3,
                    "오리엔탈": 0.1,
                    "프레시": 0.8,
                    "구르망": 0.0,
                },
            },
        )

        metadata = IndexToPineconeCommand()._build_metadata(perfume)

        self.assertEqual(metadata["perfume_id"], perfume.id)
        self.assertEqual(metadata["brand"], "CREED")
        self.assertEqual(metadata["korean_name"], "어벤투스")
        self.assertEqual(metadata["family"], "프레시")
        self.assertEqual(metadata["aura_fresh"], 0.8)
        self.assertEqual(metadata["aura_woody"], 0.3)
        self.assertEqual(metadata["price_raw"], "$150")
        self.assertGreater(metadata["price_krw"], 0)
        self.assertEqual(metadata["representative_notes"], ["베르가못", "샌달우드"])
        self.assertEqual(metadata["top_notes"], ["베르가못"])
        self.assertEqual(metadata["middle_notes"], ["파인애플"])
        self.assertEqual(metadata["base_notes"], ["샌달우드"])
        self.assertEqual(metadata["keywords"], ["세련된", "자신감"])

    @patch("perfumes.services.aura_service.map_image_to_fragrance_keywords")
    @patch("perfumes.services.aura_service.load_user_preference_map")
    @patch("perfumes.services.aura_service.load_master_map")
    def test_gold_scenarios_generate_rag_queries(
        self,
        mock_master_map,
        mock_preference_map,
        mock_image_mapping,
    ):
        mock_master_map.return_value = {
            "accord_translations": {
                "clean": "깨끗한",
                "soft": "부드러운",
                "bright": "밝은",
                "modern": "모던한",
                "dark": "어두운",
                "urban": "도시적인",
                "luxurious": "럭셔리한",
                "sensual": "관능적인",
                "warm": "따뜻한",
                "romantic": "로맨틱한",
                "natural": "자연스러운",
                "calm": "차분한",
                "elegant": "우아한",
                "fresh": "프레시한",
            },
            "accord_to_category": {"시트러스": "프레시"},
            "note_to_accord": {"베르가못": "시트러스", "레몬": "시트러스"},
        }
        mock_preference_map.return_value = {
            note: {"axis": "프레시"} for scenario in self.RAG_GOLD_SCENARIOS for note in scenario["selected_notes"]
        }
        mock_image_mapping.return_value = {
            "components_ko": ["베르가못"],
            "scores": {
                "families": [{"name": "FRESH", "score": 3.0}],
                "subs": [],
                "components_ko": [{"name": "베르가못", "score": 1.0}],
            },
        }
        service = AuraService()

        self.assertEqual(len(self.RAG_GOLD_SCENARIOS), 20)
        for scenario in self.RAG_GOLD_SCENARIOS:
            with self.subTest(english_name=scenario["english_name"]):
                _, _, query_text, search_vector = service.calculate_combined_aura(
                    scenario["vlm_output"],
                    scenario["selected_notes"],
                )

                self.assertIn(scenario["vlm_output"]["visual_summary"], query_text)
                self.assertIn("계열 향수", query_text)
                for note in scenario["selected_notes"]:
                    self.assertIn(note, query_text)
                self.assertGreater(search_vector["프레시"], 0)

    @patch("perfumes.services.aura_service.map_image_to_fragrance_keywords")
    @patch("perfumes.services.aura_service.load_user_preference_map")
    @patch("perfumes.services.aura_service.load_master_map")
    def test_experiment_scenarios_generate_rag_queries(
        self,
        mock_master_map,
        mock_preference_map,
        mock_image_mapping,
    ):
        mock_master_map.return_value = {
            "accord_translations": {
                "luxurious": "럭셔리한",
                "calm": "차분한",
                "natural": "자연스러운",
                "fresh": "프레시한",
                "bright": "밝은",
                "clean": "깨끗한",
                "sensual": "관능적인",
                "dark": "어두운",
                "modern": "모던한",
            },
            "accord_to_category": {"시트러스": "프레시"},
            "note_to_accord": {"레몬": "시트러스"},
        }
        mock_preference_map.return_value = {
            "장미": {"axis": "플로럴"},
            "샌달우드": {"axis": "우디"},
            "패출리": {"axis": "우디"},
            "레몬": {"axis": "프레시"},
            "베르가못": {"axis": "프레시"},
            "민트": {"axis": "프레시"},
            "바닐라": {"axis": "구르망"},
            "앰버": {"axis": "오리엔탈"},
            "침향": {"axis": "우디"},
        }
        mock_image_mapping.return_value = {
            "components_ko": ["레몬"],
            "scores": {
                "families": [{"name": "FRESH", "score": 2.0}],
                "subs": [],
                "components_ko": [{"name": "레몬", "score": 1.0}],
            },
        }
        service = AuraService()

        self.assertEqual(
            set(self.EXPERIMENT_SCENARIOS),
            {"dual_aura_clash", "citrus_fresh_boost", "oriental_night"},
        )
        for scenario_name, scenario in self.EXPERIMENT_SCENARIOS.items():
            with self.subTest(scenario_name=scenario_name):
                _, _, query_text, search_vector = service.calculate_combined_aura(
                    scenario["vlm_output"],
                    scenario["selected_notes"],
                )

                self.assertIn(scenario["vlm_output"]["visual_summary"], query_text)
                for note in scenario["selected_notes"]:
                    self.assertIn(note, query_text)
                self.assertTrue(any(value > 0 for value in search_vector.values()))


# ----------------------------------------------------------------
# Update History
# 2026-05-18: tests.py에서 RagPreparationTest를 분리하고 파일 역할 header/footer 추가. (worker: nobrain711)
# ----------------------------------------------------------------

# EOF: test_rag_preparation.py
