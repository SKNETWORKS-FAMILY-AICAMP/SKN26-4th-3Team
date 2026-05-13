import json
import os
import glob
from copy import deepcopy
import numpy as np
from django.core.management.base import BaseCommand
from perfumes.models import Brand, Perfume, PerfumeDetail, PerfumeRawData
from perfumes.utils import load_master_map
from scent_engine.mapper import VISUAL_TO_FRAGRANCE_RULES, KOREAN_VISUAL_TRIGGERS

class Command(BaseCommand):
    help = 'Load perfumes into MySQL with Symmetric Aura Scoring (v4.0)'

    def handle(self, *args, **options):
        # 데이터 존재 여부 체크 (중복 적재 방지)
        try:
            if Perfume.objects.exists():
                self.stdout.write(self.style.SUCCESS("Data already exists. Skipping load_perfumes..."))
                return
        except Exception:
            pass

        self.stdout.write("DB is empty. Starting intelligent data ingestion...")
        master_map = load_master_map()
        accord_to_cat = master_map["accord_to_category"]
        
        from django.conf import settings
        data_dir = os.path.join(settings.BASE_DIR, 'data', 'raw')
        json_files = glob.glob(os.path.join(data_dir, "*_fragrance_data.json"))

        axes = ["플로럴", "우디", "오리엔탈", "프레시", "구르망"]
        family_mapping = {"FLORAL": "플로럴", "WOODY": "우디", "AMBERY": "오리엔탈", "FRESH": "프레시", "GOURMAND": "구르망"}

        total_count = 0
        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error loading {file_path}: {e}"))
                    continue
                
                if not data: continue
                
                raw_brand_name = data[0].get("brand", "Unknown").upper()
                brand, _ = Brand.objects.get_or_create(name=raw_brand_name)

                brand_count = 0
                for item in data:
                    raw_item = deepcopy(item)
                    # [식별자 무결성 로직]
                    # 1순위: 공식 영문명, 2순위: 정규화된 영문 슬러그, 3순위: 한글명 (최후의 보루)
                    eng_name = item.get("english_name") or item.get("normalized_name")
                    if not eng_name:
                        eng_name = item.get("korean_name")
                    
                    if not eng_name: continue

                    scores = {axis: 0.0 for axis in axes}
                    
                    # 1. Base Scoring (Accords - 2.0)
                    for accord in item.get("accords", []):
                        cat = accord_to_cat.get(accord)
                        if cat in scores: scores[cat] += 2.0

                    # 2. Booster Scoring (Keywords/Notes)
                    perfume_metadata = set(item.get("keywords", []))
                    notes = item.get("notes", [])
                    if isinstance(notes, dict): notes = [n for sub in notes.values() for n in sub]
                    perfume_metadata.update(notes)

                    for kw in perfume_metadata:
                        kw_lower = kw.lower()
                        trigger = None
                        if kw_lower in VISUAL_TO_FRAGRANCE_RULES: trigger = kw_lower
                        elif kw_lower in KOREAN_VISUAL_TRIGGERS: trigger = KOREAN_VISUAL_TRIGGERS[kw_lower]
                        
                        if trigger:
                            rule = VISUAL_TO_FRAGRANCE_RULES[trigger]
                            for fam, weight in rule.get('families', {}).items():
                                std_fam = family_mapping.get(fam)
                                if std_fam in scores: scores[std_fam] += weight

                    # 3. Proportion Normalization
                    total_s = sum(scores.values())
                    if total_s > 0:
                        aura_profile = {k: round(v / total_s, 2) for k, v in scores.items()}
                    else:
                        aura_profile = {k: 0.2 for k in axes}

                    item["aura_profile"] = aura_profile
                    translated_notes = [master_map["note_translations"].get(n, n) for n in notes]
                    item["standardized_notes"] = translated_notes
                    item["representative_notes"] = translated_notes[:5]
                    
                    # 4. Generate Embedding Document
                    brand_name = brand.name
                    k_name = item.get("korean_name") or eng_name
                    desc_summary = item.get("description", "")[:100].strip()
                    p_family = max(scores, key=scores.get) if total_s > 0 else "프레시"
                    std_accords = ", ".join(item.get("accords", [])[:3])
                    std_notes = ", ".join(item["representative_notes"])
                    
                    embedding_doc = f"{brand_name} {k_name} {desc_summary}. {std_accords} 분위기의 {std_notes} 향이 느껴지는 {p_family} 계열 향수."
                    item["embedding_doc"] = embedding_doc

                    # 5. Save to MySQL
                    perfume, _ = Perfume.objects.update_or_create(
                        brand=brand,
                        english_name=eng_name, # 시스템 식별자로 유지
                        defaults={
                            "korean_name": k_name,
                            "product_type": item.get("product_subtype", "perfume"),
                            "family": p_family,
                            "release_year": item.get("meta", {}).get("release_year"),
                        }
                    )
                    PerfumeDetail.objects.update_or_create(
                        perfume=perfume,
                        defaults={"data": item},
                    )
                    PerfumeRawData.objects.update_or_create(
                        perfume=perfume,
                        defaults={
                            "raw_json": raw_item,
                            "source_url": raw_item.get("source_url") or raw_item.get("product_url"),
                        },
                    )
                    brand_count += 1
                
                self.stdout.write(f"Processed {brand_count} perfumes for {raw_brand_name}.")
                total_count += brand_count

        self.stdout.write(self.style.SUCCESS(f"Total {total_count} perfumes loaded into MySQL."))


def build_raw_json(item):
    raw_item = deepcopy(item)
    raw_item.pop("source_url", None)
    return raw_item


DETAIL_DATA_KEYS = {
    "price",
    "description",
    "ingredients_raw",
    "notes",
    "accords",
    "keywords",
    "meta",
    "volume",
    "aura_profile",
    "standardized_notes",
    "representative_notes",
    "notes_parsed",
    "embedding_doc",
}


def build_detail_data(item):
    detail_data = {
        key: deepcopy(item[key])
        for key in DETAIL_DATA_KEYS
        if key in item
    }
    meta = detail_data.get("meta")
    if isinstance(meta, dict):
        meta.pop("release_year", None)
        if not meta:
            detail_data.pop("meta", None)
    return detail_data


def translate_notes_pyramid(notes, master_map):
    return {
        key: [
            master_map["note_translations"].get(note, note)
            for note in value
            if isinstance(note, str)
        ]
        for key, value in notes.items()
        if key in {"top", "middle", "base"} and isinstance(value, list)
    }
