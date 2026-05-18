"""
@file load_perfumes.py
@description
Raw JSON 향수 데이터를 MySQL 데이터베이스로 로드하는 Django 관리 명령어입니다.
단순 데이터 로드를 넘어, 향수 도메인 지식 기반의 '5축 아우라 점수' 산출,
'노트 피라미드 휴리스틱 분류', 'RAG용 대칭형 문서 생성' 등 핵심 데이터 전처리를 수행합니다.

@author Olfít AI Team
@version 4.9.0
"""

import json
import os
import glob
from copy import deepcopy
import numpy as np
from django.core.management.base import BaseCommand
from perfumes.models import Brand, Perfume, PerfumeDetail, PerfumeRawData
from perfumes.utils import load_master_map, split_notes_heuristic, convert_to_krw


class Command(BaseCommand):
    """
    향수 데이터 Ingestion 및 전처리를 담당하는 커맨드 클래스입니다.
    """

    help = "Load perfumes into MySQL with Unified Accord-Note Scoring and Heuristic Pyramid (v4.9)"

    def handle(self, *args, **options):
        """
        명령어 실행의 메인 진입점입니다.
        데이터 디렉토리를 스캔하여 모든 브랜드를 로드하고 각 향수의 프로필을 생성합니다.
        """
        self.stdout.write("Starting unified aura data ingestion with note parsing...")

        # 전역 매핑 사전 로드 (메모리 최적화를 위해 핸들러 외부가 아닌 내부에서 1회 로드)
        master_map = load_master_map()
        accord_to_cat = master_map["accord_to_category"]
        note_to_accord = master_map["note_to_accord"]
        note_trans = master_map["note_translations"]

        from django.conf import settings

        # 데이터 경로 설정 (backend/app/data/raw/*.json)
        data_dir = os.path.join(settings.BASE_DIR, "data", "raw")
        json_files = glob.glob(os.path.join(data_dir, "*_fragrance_data.json"))

        # 시스템 핵심 5축 정의
        axes = ["플로럴", "우디", "오리엔탈", "프레시", "구르망"]

        total_count = 0
        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error loading {file_path}: {e}")
                    )
                    continue

                if not data:
                    continue

                # 파일의 첫 번째 아이템에서 브랜드명 추출
                raw_brand_name = data[0].get("brand", "Unknown").upper()
                brand, _ = Brand.objects.get_or_create(name=raw_brand_name)

                brand_count = 0
                for item in data:
                    # 0. 로우 데이터 보존을 위한 원본 백업
                    raw_item = build_raw_json(item)

                    # 영문명 또는 식별 가능한 이름 추출
                    eng_name = item.get("english_name") or item.get("normalized_name")
                    if not eng_name:
                        eng_name = item.get("korean_name")

                    if not eng_name:
                        continue

                    # --------------------------------------------------------
                    # [1. Score Aggregation Logic]
                    # 향수 도메인 매핑 정보를 기반으로 5축 원천 점수를 합산합니다.
                    # --------------------------------------------------------
                    scores = {axis: 0.0 for axis in axes}

                    # 1-1. 메인 어코드 가중치 (+2.0)
                    # 어코드는 향수의 '전체적인 인상'을 결정하는 가장 큰 지표입니다.
                    accords = item.get("accords", [])
                    for accord in accords:
                        cat = accord_to_cat.get(accord)
                        if cat in scores:
                            scores[cat] += 2.0

                    # 1-2. 세부 성분(Notes) 가중치 (+1.0)
                    # 노트는 향수의 '미세한 뉘앙스'를 보강하는 지표입니다.
                    raw_notes = item.get("notes", [])
                    flat_notes = []
                    # 피라미드 형태(dict)와 리스트 형태 모두 대응
                    if isinstance(raw_notes, dict):
                        for sub_list in raw_notes.values():
                            if isinstance(sub_list, list):
                                flat_notes.extend(sub_list)
                    else:
                        flat_notes = raw_notes

                    for note in flat_notes:
                        # 한글 번역 -> 어코드 매핑 -> 최종 카테고리 매핑 순으로 탐색
                        note_ko = note_trans.get(note, note)
                        mapped_accord = note_to_accord.get(note_ko)
                        if mapped_accord:
                            cat = accord_to_cat.get(mapped_accord)
                            if cat in scores:
                                scores[cat] += 1.0

                    # --------------------------------------------------------
                    # [2. Normalization Logic: L2 Norm]
                    # 코사인 유사도 연산의 정확도를 위해 벡터 크기를 1로 정규화합니다.
                    # --------------------------------------------------------
                    score_vec = np.array([scores[a] for a in axes])
                    norm = np.linalg.norm(score_vec)

                    if norm > 0:
                        normalized_vec = score_vec / norm
                        aura_profile = {
                            axis: round(float(val), 4)
                            for axis, val in zip(axes, normalized_vec)
                        }
                    else:
                        # 데이터가 전혀 없는 경우 모든 축에 균등 가중치(1/sqrt(5)) 부여
                        aura_profile = {axis: 0.4472 for axis in axes}

                    item["aura_profile"] = aura_profile

                    # --------------------------------------------------------
                    # [3. Data Enrichment]
                    # 가격 환산, 노트 분류, RAG 문서 생성 등 부가 데이터를 준비합니다.
                    # --------------------------------------------------------

                    # 3-1. 원화 가격 환산 (인덱싱 및 UI 검색 최적화)
                    price_data = item.get("price") or {}
                    item["price_krw"] = convert_to_krw(price_data)

                    # 3-2. 휴리스틱 노트 피라미드 생성 (Scent Pyramid)
                    # 원천 데이터에 Top/Mid/Base 구분이 없을 경우 알고리즘으로 자동 생성
                    pyramid = split_notes_heuristic(raw_notes)
                    item["notes_parsed"] = {
                        k: [note_trans.get(n, n) for n in v] for k, v in pyramid.items()
                    }

                    # 3-3. 번역 및 대표 노트 추출
                    translated_notes = [note_trans.get(n, n) for n in flat_notes]
                    item["standardized_notes"] = translated_notes
                    item["representative_notes"] = translated_notes[
                        :5
                    ]  # 상위 5개만 추출

                    # 3-4. RAG용 대칭형 임베딩 문서 생성 (Symmetric Embedding)
                    # 사용자의 검색 쿼리 구조와 동일하게 설계하여 검색 정확도 극대화
                    brand_name = brand.name
                    k_name = item.get("korean_name") or eng_name
                    desc_summary = item.get("description", "")[:150].strip()

                    # 도미넌트 아우라 축 추출 (분위기 묘사 보강용)
                    top_axes_items = sorted(
                        aura_profile.items(), key=lambda x: x[1], reverse=True
                    )
                    p_family = top_axes_items[0][0]  # 가장 점수 높은 축
                    axes_str = "와 ".join(
                        [a[0] for a in top_axes_items[:2]]
                    )  # 상위 2개 축

                    std_accords = ", ".join(accords[:5])
                    std_notes = ", ".join(item["representative_notes"])

                    # 키워드를 해시태그 형태로 추가하여 감성적 매칭 강화
                    keywords_list = item.get("keywords", [])
                    keywords_str = (
                        f" #{' #'.join(keywords_list[:5])}"
                        if isinstance(keywords_list, list) and keywords_list
                        else ""
                    )

                    # 최종 자연어 문서 구성
                    embedding_doc = (
                        f"{brand_name} {k_name}. {desc_summary}. "
                        f"{std_accords} 분위기의 {std_notes} 향이 느껴지는 {p_family} 계열 향수. "
                        f"{axes_str} 분위기가 뚜렷하게 느껴지는 제품입니다.{keywords_str}"
                    )
                    item["embedding_doc"] = embedding_doc

                    # --------------------------------------------------------
                    # [4. Persistence]
                    # 가공된 데이터를 MySQL의 3가지 테이블(Main, Detail, Raw)에 저장합니다.
                    # --------------------------------------------------------

                    # 4-1. Perfume (메인 정보)
                    perfume, _ = Perfume.objects.update_or_create(
                        brand=brand,
                        english_name=eng_name,
                        defaults={
                            "korean_name": k_name,
                            "product_type": item.get("product_subtype", "perfume"),
                            "family": p_family,
                            "release_year": item.get("meta", {}).get("release_year"),
                        },
                    )

                    # 4-2. PerfumeDetail (전처리된 풍부한 JSON 데이터)
                    PerfumeDetail.objects.update_or_create(
                        perfume=perfume,
                        defaults={"data": build_detail_data(item)},
                    )

                    # 4-3. PerfumeRawData (크롤링된 로우 데이터 백업)
                    PerfumeRawData.objects.update_or_create(
                        perfume=perfume,
                        defaults={"raw_json": raw_item},
                    )
                    brand_count += 1

                self.stdout.write(
                    f"Processed {brand_count} perfumes for {raw_brand_name}."
                )
                total_count += brand_count

        self.stdout.write(
            self.style.SUCCESS(
                f"Total {total_count} perfumes loaded with persisted aura scores and notes."
            )
        )


def build_raw_json(item):
    """
    저장 가치가 없는 일회성 URL 필드 등을 제거한 뒤 원본 데이터를 딥카피하여 반환합니다.
    """
    raw_item = deepcopy(item)
    raw_item.pop("source_url", None)
    return raw_item


# DB(PerfumeDetail)에 영구 저장할 핵심 키 목록
DETAIL_DATA_KEYS = {
    "price",
    "price_krw",
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
    """
    가공된 전체 아이템에서 핵심 데이터(DETAIL_DATA_KEYS)만 추출하여 Detail 테이블 저장용 딕셔너리를 구성합니다.
    """
    detail_data = {key: deepcopy(item[key]) for key in DETAIL_DATA_KEYS if key in item}

    # 메타 정보 내 불필요한 필드 정리
    meta = detail_data.get("meta")
    if isinstance(meta, dict):
        meta.pop("release_year", None)  # 메인 Perfume 테이블에 저장되므로 중복 제거
        if not meta:
            detail_data.pop("meta", None)

    return detail_data

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header와 파일 책임을 기록하는 Update History/EOF footer 추가. (worker: @nobrain711)
# 2026-05-15: fix(load_perfumes): remove unexpected indentation in load_pefumes.py. (author: @Gloveman)
# 2026-05-15: feat(load_perfumes): enhance data ingestion and scoring logic. (author: @Gloveman)
# 2026-05-14: fix(recommendations): split scent pyramid notes. (author: @nobrain711)
# 2026-05-13: feat(perfumes): persist perfume image assets. (author: @nobrain711)
# 2026-05-13: fix(django): guard migrate schema drift. (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: load_perfumes.py
