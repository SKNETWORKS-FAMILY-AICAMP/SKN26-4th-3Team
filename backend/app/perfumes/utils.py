"""
@file utils.py
@description
Olfít 프로젝트 전반에서 공통으로 사용되는 유틸리티 함수 모음입니다.
데이터 매핑 사전 로드, 향수 노트의 휴리스틱 피라미드 분류, 통화 환산 등
비즈니스 로직에 필요한 핵심 도우미 기능들을 포함하고 있습니다.

@author Olfít AI Team
@version 4.9.0
"""

import json
import os
from django.conf import settings

# ----------------------------------------------------------------
# [Data Loading Helpers]
# ----------------------------------------------------------------


def load_master_map():
    """
    향수 도메인 지식 베이스(번역, 어코드 매핑 등)가 담긴 마스터 맵을 로드합니다.
    @return: dict (master_fragrance_map.json 내용)
    """
    path = os.path.join(
        settings.BASE_DIR, "perfumes", "data", "mappings", "master_fragrance_map.json"
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_user_preference_map():
    """
    사용자의 선호 노트와 향수 데이터 간의 매핑 및 확장 규칙 정보를 로드합니다.
    @return: dict (user_preference_map.json 내용)
    """
    path = os.path.join(
        settings.BASE_DIR, "perfumes", "data", "mappings", "user_preference_map.json"
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_mood_descriptors():
    """
    향수의 분위기 설명자(Mood Descriptors) 정보를 로드합니다.
    @return: dict (fragrance_mood_descriptors.json 내용)
    """
    path = os.path.join(
        settings.BASE_DIR,
        "perfumes",
        "data",
        "mappings",
        "fragrance_mood_descriptors.json",
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_preference_expansion():
    """
    사용자 선호 노트를 더 넓은 범위의 검색 키워드로 확장하는 매핑 정보를 로드합니다.
    (load_user_preference_map과 동일한 데이터를 참조합니다.)
    """
    return load_user_preference_map()


# ----------------------------------------------------------------
# [Heuristic Note Pyramid Splitting]
# ----------------------------------------------------------------

# 탑 노트로 분류될 가능성이 높은 향기 지표들 (시트러스, 그린, 허벌 계열)
TOP_INDICATORS = [
    "레몬",
    "자몽",
    "베르가못",
    "만다린",
    "오렌지",
    "라임",
    "유자",
    "탄제린",
    "시트러스",
    "비터 오렌지",
    "블러드 오렌지",
    "금귤",
    "깔라만시",
    "포멜로",
    "민트",
    "박하",
    "바질",
    "로즈마리",
    "세이지",
    "타임",
    "클래리 세이지",
    "유칼립투스",
    "사과",
    "서양배",
    "리치",
    "알데하이드",
    "그린",
    "네롤리",
    "페티그레인",
    "핑크 페퍼",
    "주니퍼",
    "코리앤더",
    "샴페인",
    "보드카",
    "오이",
    "대나무",
    "마린",
    "워터",
    "오조닉",
    "아독살",
    "라벤더",
    "lemon",
    "grapefruit",
    "bergamot",
    "mandarin",
    "orange",
    "lime",
    "yuzu",
    "tangerine",
    "citrus",
    "mint",
    "basil",
    "rosemary",
    "sage",
    "thyme",
    "apple",
    "pear",
    "green",
    "aldehyde",
]

# 베이스 노트로 분류될 가능성이 높은 향기 지표들 (우디, 머스크, 오리엔탈 계열)
BASE_INDICATORS = [
    "머스크",
    "앰버",
    "샌달우드",
    "시더우드",
    "패출리",
    "베티버",
    "바닐라",
    "오드",
    "아가우드",
    "침향",
    "가죽",
    "레더",
    "스웨이드",
    "인센스",
    "몰약",
    "벤조인",
    "올리바넘",
    "오포포낙스",
    "라브다넘",
    "스티락스",
    "발삼",
    "톤카 빈",
    "오크모스",
    "가약",
    "과약",
    "캐시머란",
    "캐시미어",
    "앰브록산",
    "이소 이 슈퍼",
    "클리어우드",
    "카라멜",
    "초콜릿",
    "설탕",
    "꿀",
    "프랄린",
    "누가",
    "마시멜로",
    "쿠마린",
    "타바코",
    "연기",
    "스모크",
    "위스키",
    "럼",
    "커피",
    "카카오",
    "애니멀",
    "사향",
    "시벳",
    "musk",
    "amber",
    "sandalwood",
    "cedar",
    "patchouli",
    "vetiver",
    "vanilla",
    "oud",
    "leather",
    "incense",
    "benzoin",
    "tonka",
    "oakmoss",
    "tobacco",
]


def split_notes_heuristic(notes):
    """
    구조화되지 않은 향수 노트 리스트를 어코드 특성에 따라 탑/미들/베이스 피라미드로 자동 분리합니다.

    분류 기준:
    1. TOP_INDICATORS 포함 시 -> Top
    2. BASE_INDICATORS 포함 시 -> Base
    3. 그 외 (주로 플로럴, 스파이시) -> Middle

    보정 로직:
    - 결과가 특정 층에만 쏠리지 않도록 최소한의 데이터가 있을 경우 골고루 배분합니다.
    """
    if not notes:
        return {"top": [], "middle": [], "base": []}

    # 이미 구조화된 딕셔너리 형태라면 키값 대소문자 보정 후 반환
    if isinstance(notes, dict):
        return {
            "top": notes.get("top") or notes.get("Top") or [],
            "middle": notes.get("middle")
            or notes.get("Middle")
            or notes.get("heart")
            or [],
            "base": notes.get("base") or notes.get("Base") or [],
        }

    top, middle, base = [], [], []

    for note in notes:
        note_lower = note.lower()
        is_top = any(ind in note_lower for ind in TOP_INDICATORS)
        is_base = any(ind in note_lower for ind in BASE_INDICATORS)

        if is_top:
            top.append(note)
        elif is_base:
            base.append(note)
        else:
            middle.append(note)

    # [보정 로직] 데이터가 충분할 경우 최소 하나씩은 채워주기 위한 재배치
    total_count = len(notes)
    if total_count >= 1:
        if not top:
            if middle:
                top.append(middle.pop(0))
            elif base:
                top.append(base.pop(0))

        if not base and total_count >= 2:
            if middle:
                base.append(middle.pop())
            elif top and len(top) > 1:
                base.append(top.pop())

        if not middle and total_count >= 3:
            if len(top) > len(base):
                middle.append(top.pop())
            else:
                middle.append(base.pop(0))

    return {"top": top, "middle": middle, "base": base}


# ----------------------------------------------------------------
# [Pricing & Currency Conversion]
# ----------------------------------------------------------------

# 실시간 환율 정보 (Last Modified 기준)
EXCHANGE_RATES = {
    "USD": 1491,  # 2026-05-15 기준
    "EUR": 1744,
    "GBP": 2003,
    "KRW": 1,
}


def convert_to_krw(price_data):
    """
    다양한 국가의 통화 가격 정보를 원화(KRW)로 환산합니다.

    Args:
        price_data (dict): {"amount": float, "currency": "USD"} 형태의 데이터

    Returns:
        int: 환산된 원화 가격 (실패 시 0)
    """
    if not price_data or not isinstance(price_data, dict):
        return 0

    amount = price_data.get("amount", 0)
    currency = str(price_data.get("currency", "KRW")).upper()

    # 정의되지 않은 통화의 경우 기본 환율 1350원 적용
    rate = EXCHANGE_RATES.get(currency, 1350)

    try:
        return int(float(amount) * rate)
    except (TypeError, ValueError):
        return 0


# ----------------------------------------------------------------
# Last Modified: 2026-05-15
# Modified By: 이창우
# ----------------------------------------------------------------

# EOF: utils.py
