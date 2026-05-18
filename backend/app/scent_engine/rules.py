"""
@file scent_engine/rules.py
@role
시각적 요소(색상, 사물, 장면 등)와 향기 속성 간의 매핑 규칙 및 가중치(Score) 데이터를 정의합니다.
디자인된 도메인 규칙을 바탕으로 시각적 입력을 향수 도메인의 전문적인 속성으로 변환하는 기준을 제공합니다.
"""

# ----------------------------------------------------------------
# Update History
# 2026-05-11: 기존 mapper에서 점수 할당 매핑 규칙 부분을 별도 파일로 분리. (worker: Gloveman)
# ----------------------------------------------------------------


def _mapping(
    families: dict[str, float],
    subs: dict[str, float],
    components: dict[str, float],
    descriptors: dict[str, float],
) -> dict[str, dict[str, float]]:
    return {
        "families": families,
        "subs": subs,
        "components": components,
        "descriptors": descriptors,
    }


VISUAL_TO_FRAGRANCE_RULES: dict[str, dict[str, dict[str, float]]] = {
    # -----------------------------------------------------
    # colors
    # -----------------------------------------------------
    "black": _mapping(
        families={"WOODY": 0.8, "AMBERY": 0.5},
        subs={"Dry Woods": 0.6, "Soft Amber": 0.5},
        components={
            "Leather": 0.5,
            "Incense": 0.4,
            "Oud": 0.4,
            "Patchouli": 0.3,
            "Musk": 0.5,
        },
        descriptors={
            "깊은": 0.7,
            "차분한": 0.6,
            "세련된": 0.6,
            "묵직한": 0.3,
            "스모키한": 0.3,
        },
    ),
    "brown": _mapping(
        families={"WOODY": 1.4, "AMBERY": 1.0},
        subs={"Woods": 1.2, "Woody Amber": 1.0, "Dry Woods": 0.6},
        components={
            "Sandalwood": 1.3,
            "Cedarwood": 1.1,
            "Amber": 1.0,
            "Tobacco": 0.6,
        },
        descriptors={
            "따뜻한": 1.3,
            "안정감": 1.0,
            "깊은": 0.9,
            "묵직한": 0.5,
        },
    ),
    "gold": _mapping(
        families={"AMBERY": 1.6, "FLORAL": 0.5},
        subs={"Amber": 1.4, "Soft Amber": 1.1, "Floral Amber": 0.7},
        components={
            "Amber": 1.6,
            "Vanilla": 1.0,
            "Musk": 0.8,
        },
        descriptors={
            "따뜻한": 1.2,
            "포근한": 0.9,
            "찬란한": 1.1,
            "매력적인": 1.0,
        },
    ),
    "green": _mapping(
        families={"FRESH": 1.8, "WOODY": 0.7},
        subs={"Green": 1.8, "Mossy Woods": 0.8, "Aromatic": 0.7},
        components={
            "Green Note": 1.8,
            "Oakmoss": 0.9,
            "Vetiver": 0.8,
            "Basil": 0.8,
            "Bergamot": 0.5,
        },
        descriptors={
            "청량한": 1.5,
            "신선한": 1.5,
            "상쾌한": 1.3,
            "청정한": 1.0,
        },
    ),
    "blue": _mapping(
        families={"FRESH": 1.8},
        subs={"Water": 1.5, "Citrus": 0.8},
        components={
            "Marine": 1.4,
            "Ozonic": 1.2,
            "Bergamot": 0.8,
            "Lemon": 0.7,
            "Musk": 0.4,
        },
        descriptors={
            "시원한": 1.5,
            "상쾌한": 1.3,
            "가벼운": 1.0,
            "깨끗한": 0.9,
        },
    ),
    "white": _mapping(
        families={"FRESH": 1.3, "FLORAL": 1.0, "AMBERY": 0.4},
        subs={"Green": 0.8, "Soft Floral": 1.1, "Soft Amber": 0.6},
        components={
            "Musk": 1.3,
            "Iris": 1.0,
            "Lily": 0.9,
            "Bergamot": 0.5,
        },
        descriptors={
            "깨끗한": 1.5,
            "부드러운": 1.3,
            "맑은": 1.0,
            "가벼운": 0.9,
        },
    ),
    "pink": _mapping(
        families={"FLORAL": 1.7, "FRESH": 0.8},
        subs={"Floral": 1.5, "Soft Floral": 1.0, "Fruity": 0.8},
        components={
            "Absolute Rose": 1.5,
            "Peony": 1.3,
            "Berry, Apple, Peach": 0.8,
            "Musk": 0.4,
        },
        descriptors={
            "우아한": 1.2,
            "달콤한": 1.0,
            "밝은": 1.0,
            "감미로운": 1.0,
            "부드러운": 0.8,
        },
    ),
    "red": _mapping(
        families={"FLORAL": 1.0, "AMBERY": 1.0, "FRESH": 0.5},
        subs={"Floral Amber": 1.3, "Fruity": 1.0, "Amber": 0.7},
        components={
            "Absolute Rose": 1.2,
            "Pepper": 0.9,
            "Spicy": 0.9,
            "Berry, Apple, Peach": 1.0,
        },
        descriptors={
            "감각적인": 1.3,
            "달콤한": 1.1,
            "강한": 1.0,
            "매력적인": 1.0,
        },
    ),
    "beige": _mapping(
        families={"FLORAL": 0.9, "AMBERY": 1.1, "WOODY": 0.5},
        subs={"Soft Floral": 1.0, "Soft Amber": 1.2, "Woods": 0.4},
        components={
            "Musk": 1.2,
            "Iris": 1.0,
            "Vanilla": 1.0,
            "Sandalwood": 0.7,
        },
        descriptors={
            "부드러운": 1.5,
            "포근한": 1.2,
            "온화한": 1.0,
            "따뜻한": 0.8,
        },
    ),
    "gray": _mapping(
        families={"FRESH": 0.8, "WOODY": 0.6, "AMBERY": 0.4},
        subs={"Water": 0.8, "Mossy Woods": 0.6, "Soft Amber": 0.4},
        components={
            "Musk": 1.0,
            "Vetiver": 0.7,
            "Ozonic": 0.8,
            "Oakmoss": 0.5,
        },
        descriptors={
            "차분한": 1.2,
            "깨끗한": 1.0,
            "시원한": 0.8,
        },
    ),
    # -----------------------------------------------------
    # objects
    # -----------------------------------------------------
    "dress": _mapping(
        families={"FLORAL": 1.2, "FRESH": 1.0},
        subs={"Soft Floral": 1.1, "Floral": 1.0, "Green": 0.7},
        components={
            "Peony": 1.1,
            "Absolute Rose": 1.0,
            "Musk": 0.9,
            "Iris": 0.7,
            "Bergamot": 0.6,
        },
        descriptors={
            "우아한": 1.2,
            "부드러운": 1.1,
            "밝은": 0.8,
            "감미로운": 0.8,
        },
    ),
    "handbag": _mapping(
        families={"FLORAL": 0.8, "AMBERY": 0.6, "FRESH": 0.6},
        subs={"Soft Floral": 0.8, "Soft Amber": 0.6},
        components={
            "Musk": 0.9,
            "Iris": 0.7,
            "Absolute Rose": 0.6,
        },
        descriptors={
            "세련된": 1.0,
            "우아한": 0.9,
            "부드러운": 0.6,
        },
    ),
    "necklace": _mapping(
        families={"FLORAL": 0.8, "AMBERY": 0.6},
        subs={"Soft Floral": 0.7, "Floral Amber": 0.5},
        components={
            "Musk": 0.7,
            "Absolute Rose": 0.6,
            "Amber": 0.5,
        },
        descriptors={
            "우아한": 1.0,
            "찬란한": 0.6,
            "매력적인": 0.7,
        },
    ),
    "wood": _mapping(
        families={"WOODY": 2.0},
        subs={"Woods": 1.6, "Dry Woods": 0.9, "Woody Amber": 0.8},
        components={
            "Wood Scent": 1.5,
            "Cedarwood": 1.4,
            "Sandalwood": 1.4,
            "Vetiver": 1.0,
        },
        descriptors={
            "따뜻한": 1.1,
            "안정감": 1.1,
            "깊은": 1.0,
            "묵직한": 0.7,
        },
    ),
    "tree": _mapping(
        families={"WOODY": 1.3, "FRESH": 1.0},
        subs={"Woods": 1.0, "Green": 1.0},
        components={
            "Pine tree": 1.0,
            "Cedarwood": 0.9,
            "Green Note": 1.0,
            "Vetiver": 0.8,
        },
        descriptors={
            "신선한": 1.0,
            "상쾌한": 0.9,
            "안정감": 0.8,
            "깊은": 0.6,
        },
    ),
    "leather": _mapping(
        families={"WOODY": 2.0, "AMBERY": 0.8},
        subs={"Dry Woods": 2.0, "Woody Amber": 0.8},
        components={
            "Leather": 2.5,
            "Tobacco": 1.0,
            "Incense": 1.0,
            "Saffron": 0.8,
        },
        descriptors={
            "스모키한": 1.7,
            "따뜻한": 1.2,
            "묵직한": 1.5,
            "감각적인": 1.3,
        },
    ),
    "flower": _mapping(
        families={"FLORAL": 2.0},
        subs={"Floral": 1.6, "Soft Floral": 1.0},
        components={
            "Absolute Rose": 1.3,
            "Absolute Jasmin": 1.3,
            "Peony": 1.1,
            "Lily": 0.9,
        },
        descriptors={
            "우아한": 1.3,
            "섬세한": 1.2,
            "부드러운": 1.1,
            "감미로운": 1.0,
        },
    ),
    "ocean": _mapping(
        families={"FRESH": 2.0},
        subs={"Water": 1.8, "Citrus": 0.6},
        components={
            "Marine": 1.8,
            "Ozonic": 1.4,
            "Bergamot": 0.6,
        },
        descriptors={
            "시원한": 1.6,
            "짭짤한": 1.2,
            "축축한": 1.0,
            "청량한": 1.2,
        },
    ),
    "coffee": _mapping(
        families={"AMBERY": 1.7},
        subs={"Soft Amber": 1.2, "Amber": 1.0},
        components={
            "Vanilla": 1.2,
            "Amber": 1.1,
            "Musk": 0.8,
        },
        descriptors={
            "따뜻한": 1.4,
            "포근한": 1.2,
            "달콤한": 1.2,
            "깊은": 1.0,
        },
    ),
    "candle": _mapping(
        families={"AMBERY": 1.4, "WOODY": 0.8},
        subs={"Soft Amber": 1.2, "Dry Woods": 0.8},
        components={
            "Incense": 1.4,
            "Amber": 1.2,
            "Musk": 0.8,
        },
        descriptors={
            "신비로운": 1.2,
            "따뜻한": 1.1,
            "포근한": 1.1,
            "차분한": 1.0,
        },
    ),
    "book": _mapping(
        families={"WOODY": 1.0, "AMBERY": 0.6},
        subs={"Woods": 0.9, "Soft Amber": 0.7},
        components={
            "Cedarwood": 0.8,
            "Sandalwood": 0.8,
            "Musk": 0.6,
        },
        descriptors={
            "차분한": 1.2,
            "부드러운": 0.9,
            "깊은": 0.8,
        },
    ),
    "fabric": _mapping(
        families={"FRESH": 0.8, "FLORAL": 0.8, "AMBERY": 0.5},
        subs={"Soft Floral": 0.9, "Soft Amber": 0.7},
        components={
            "Musk": 1.0,
            "Iris": 0.8,
            "Lily": 0.6,
        },
        descriptors={
            "부드러운": 1.2,
            "깨끗한": 1.0,
            "포근한": 0.8,
        },
    ),
    "fruit": _mapping(
        families={"FRESH": 1.6},
        subs={"Fruity": 1.6, "Citrus": 0.8},
        components={
            "Berry, Apple, Peach": 1.4,
            "Tropical Fruit": 1.0,
            "Orange": 0.8,
        },
        descriptors={
            "달콤한": 1.4,
            "밝은": 1.1,
            "시원한": 0.8,
        },
    ),
    # -----------------------------------------------------
    # scenes
    # -----------------------------------------------------
    "indoor": _mapping(
        families={"AMBERY": 0.3, "FLORAL": 0.3},
        subs={"Soft Amber": 0.3, "Soft Floral": 0.3},
        components={
            "Musk": 0.4,
            "Iris": 0.3,
        },
        descriptors={
            "차분한": 0.4,
            "부드러운": 0.3,
        },
    ),
    "room": _mapping(
        families={"AMBERY": 0.3, "FLORAL": 0.3},
        subs={"Soft Amber": 0.3, "Soft Floral": 0.3},
        components={
            "Musk": 0.4,
            "Iris": 0.3,
        },
        descriptors={
            "차분한": 0.4,
            "부드러운": 0.3,
        },
    ),
    "forest": _mapping(
        families={"WOODY": 1.8, "FRESH": 1.2},
        subs={"Mossy Woods": 1.6, "Green": 1.2, "Woods": 0.8},
        components={
            "Oakmoss": 1.5,
            "Vetiver": 1.3,
            "Green Note": 1.2,
            "Pine tree": 1.0,
        },
        descriptors={
            "신선한": 1.2,
            "상쾌한": 1.1,
            "깊은": 1.0,
            "묵직한": 0.8,
        },
    ),
    "beach": _mapping(
        families={"FRESH": 2.0},
        subs={"Water": 1.6, "Citrus": 1.0},
        components={
            "Marine": 1.6,
            "Ozonic": 1.2,
            "Bergamot": 0.9,
            "Lemon": 0.8,
        },
        descriptors={
            "시원한": 1.5,
            "청량한": 1.3,
            "상쾌한": 1.2,
            "가벼운": 1.0,
        },
    ),
    "cafe": _mapping(
        families={"AMBERY": 1.5, "WOODY": 0.5},
        subs={"Soft Amber": 1.3, "Amber": 0.8},
        components={
            "Vanilla": 1.4,
            "Amber": 1.0,
            "Musk": 0.8,
            "Sandalwood": 0.6,
        },
        descriptors={
            "따뜻한": 1.4,
            "포근한": 1.3,
            "달콤한": 1.1,
            "부드러운": 1.0,
        },
    ),
    "bar": _mapping(
        families={"WOODY": 1.5, "AMBERY": 1.5},
        subs={"Dry Woods": 1.4, "Amber": 1.2, "Woody Amber": 1.0},
        components={
            "Leather": 1.5,
            "Tobacco": 1.4,
            "Amber": 1.2,
            "Incense": 1.0,
        },
        descriptors={
            "스모키한": 1.3,
            "묵직한": 1.3,
            "감각적인": 1.2,
            "깊은": 1.0,
        },
    ),
    "garden": _mapping(
        families={"FLORAL": 1.5, "FRESH": 1.0},
        subs={"Floral": 1.3, "Green": 0.9, "Soft Floral": 0.8},
        components={
            "Absolute Rose": 1.2,
            "Peony": 1.0,
            "Green Note": 0.9,
            "Bergamot": 0.7,
        },
        descriptors={
            "우아한": 1.1,
            "신선한": 1.0,
            "상쾌한": 0.9,
            "밝은": 0.8,
        },
    ),
    "rainy street": _mapping(
        families={"FRESH": 1.4, "WOODY": 0.9},
        subs={"Water": 1.3, "Mossy Woods": 1.0},
        components={
            "Ozonic": 1.4,
            "Marine": 0.9,
            "Oakmoss": 1.0,
            "Vetiver": 0.8,
        },
        descriptors={
            "축축한": 1.4,
            "시원한": 1.2,
            "깊은": 0.8,
            "청정한": 0.8,
        },
    ),
    "city": _mapping(
        families={"FRESH": 0.8, "WOODY": 0.7, "AMBERY": 0.5},
        subs={"Aromatic": 0.7, "Dry Woods": 0.5, "Soft Amber": 0.5},
        components={
            "Musk": 0.9,
            "Vetiver": 0.7,
            "Cedarwood": 0.5,
        },
        descriptors={
            "세련된": 1.2,
            "깨끗한": 0.8,
            "차분한": 0.8,
        },
    ),
    "office": _mapping(
        families={"FRESH": 1.2},
        subs={"Green": 0.8, "Citrus": 0.8},
        components={
            "Musk": 1.0,
            "Bergamot": 0.8,
            "Green tea": 0.7,
        },
        descriptors={
            "깨끗한": 1.2,
            "가벼운": 0.9,
            "단정한": 0.9,
        },
    ),
    "bedroom": _mapping(
        families={"AMBERY": 0.8, "FLORAL": 0.8},
        subs={"Soft Amber": 0.8, "Soft Floral": 0.8},
        components={
            "Musk": 1.0,
            "Vanilla": 0.7,
            "Iris": 0.8,
        },
        descriptors={
            "포근한": 1.0,
            "부드러운": 1.0,
            "차분한": 0.8,
        },
    ),
    # -----------------------------------------------------
    # moods / raw keywords
    # -----------------------------------------------------
    "modern": _mapping(
        families={"FRESH": 1.1, "FLORAL": 0.7, "WOODY": 0.4},
        subs={"Green": 0.8, "Citrus": 0.7, "Soft Floral": 0.6},
        components={
            "Musk": 1.0,
            "Bergamot": 0.8,
            "Green Note": 0.7,
            "Iris": 0.5,
        },
        descriptors={
            "세련된": 1.4,
            "깨끗한": 1.0,
            "상쾌한": 0.8,
            "가벼운": 0.7,
        },
    ),
    "fashion": _mapping(
        families={"FLORAL": 1.2, "FRESH": 1.0, "AMBERY": 0.4},
        subs={"Soft Floral": 1.0, "Floral": 0.8, "Green": 0.6},
        components={
            "Musk": 1.1,
            "Iris": 0.9,
            "Peony": 0.9,
            "Absolute Rose": 0.8,
            "Bergamot": 0.6,
        },
        descriptors={
            "세련된": 1.3,
            "우아한": 1.1,
            "부드러운": 0.8,
            "밝은": 0.6,
        },
    ),
    "style": _mapping(
        families={"FLORAL": 0.8, "FRESH": 0.8},
        subs={"Soft Floral": 0.7, "Green": 0.5},
        components={
            "Musk": 0.8,
            "Iris": 0.7,
            "Bergamot": 0.5,
        },
        descriptors={
            "세련된": 1.1,
            "우아한": 0.7,
            "깨끗한": 0.5,
        },
    ),
    "feminine": _mapping(
        families={"FLORAL": 1.6, "FRESH": 0.8},
        subs={"Floral": 1.2, "Soft Floral": 1.2, "Fruity": 0.5},
        components={
            "Peony": 1.2,
            "Absolute Rose": 1.2,
            "Absolute Jasmin": 0.9,
            "Iris": 0.8,
            "Musk": 0.7,
        },
        descriptors={
            "우아한": 1.4,
            "섬세한": 1.1,
            "부드러운": 1.0,
            "감미로운": 0.8,
        },
    ),
    "elegant": _mapping(
        families={"FLORAL": 1.4, "AMBERY": 0.8, "FRESH": 0.6},
        subs={"Soft Floral": 1.2, "Floral": 0.9, "Soft Amber": 0.6},
        components={
            "Iris": 1.2,
            "Musk": 1.1,
            "Absolute Rose": 1.0,
            "Peony": 0.8,
        },
        descriptors={
            "우아한": 1.8,
            "부드러운": 1.0,
            "섬세한": 0.9,
            "매력적인": 0.7,
        },
    ),
    "luxury": _mapping(
        families={"AMBERY": 1.0, "FLORAL": 0.8, "WOODY": 0.5},
        subs={"Amber": 0.8, "Soft Amber": 0.7, "Floral Amber": 0.6},
        components={
            "Amber": 1.0,
            "Musk": 0.8,
            "Absolute Rose": 0.7,
            "Sandalwood": 0.6,
        },
        descriptors={
            "우아한": 1.1,
            "매력적인": 1.0,
            "세련된": 0.9,
            "깊은": 0.6,
        },
    ),
    "contemporary": _mapping(
        families={"FRESH": 1.0, "FLORAL": 0.7},
        subs={"Green": 0.7, "Citrus": 0.6, "Soft Floral": 0.5},
        components={
            "Musk": 0.9,
            "Bergamot": 0.8,
            "Green Note": 0.6,
        },
        descriptors={
            "세련된": 1.2,
            "깨끗한": 0.8,
            "가벼운": 0.6,
        },
    ),
    "warm": _mapping(
        families={"AMBERY": 1.6, "WOODY": 1.0},
        subs={"Amber": 1.4, "Soft Amber": 1.2, "Woody Amber": 0.8},
        components={
            "Amber": 1.5,
            "Vanilla": 1.2,
            "Sandalwood": 1.0,
            "Tobacco": 0.7,
        },
        descriptors={
            "따뜻한": 2.0,
            "포근한": 1.3,
            "깊은": 0.8,
        },
    ),
    "dark": _mapping(
        families={"WOODY": 1.5, "AMBERY": 1.2},
        subs={"Dry Woods": 1.5, "Soft Amber": 0.8},
        components={
            "Leather": 1.3,
            "Incense": 1.3,
            "Oud": 1.2,
            "Patchouli": 1.0,
        },
        descriptors={
            "스모키한": 1.4,
            "묵직한": 1.5,
            "신비로운": 1.2,
            "깊은": 1.2,
        },
    ),
    "luxurious": _mapping(
        families={"AMBERY": 1.2, "WOODY": 0.9, "FLORAL": 0.9},
        subs={"Amber": 1.0, "Woody Amber": 0.8, "Floral Amber": 0.8},
        components={
            "Amber": 1.1,
            "Sandalwood": 0.9,
            "Absolute Rose": 0.9,
            "Musk": 0.8,
        },
        descriptors={
            "우아한": 1.2,
            "감각적인": 1.0,
            "매력적인": 1.1,
            "깊은": 0.7,
        },
    ),
    "clean": _mapping(
        families={"FRESH": 1.8},
        subs={"Green": 1.0, "Citrus": 1.0, "Water": 0.8},
        components={
            "Musk": 1.3,
            "Bergamot": 1.0,
            "Green tea": 0.9,
            "Lemon": 0.8,
        },
        descriptors={
            "깨끗한": 2.0,
            "청량한": 1.2,
            "상쾌한": 1.0,
            "가벼운": 1.0,
        },
    ),
    "fresh": _mapping(
        families={"FRESH": 2.0},
        subs={"Citrus": 1.3, "Green": 1.1, "Water": 0.8},
        components={
            "Bergamot": 1.2,
            "Lemon": 1.1,
            "Mandarin": 0.9,
            "Green Note": 0.9,
            "Marine": 0.7,
        },
        descriptors={
            "상쾌한": 1.8,
            "시원한": 1.2,
            "산뜻한": 1.2,
            "가벼운": 1.0,
        },
    ),
    "romantic": _mapping(
        families={"FLORAL": 1.8},
        subs={"Floral": 1.4, "Soft Floral": 1.2},
        components={
            "Absolute Rose": 1.4,
            "Peony": 1.1,
            "Absolute Jasmin": 1.0,
            "Iris": 0.8,
        },
        descriptors={
            "우아한": 1.4,
            "섬세한": 1.2,
            "부드러운": 1.2,
            "감미로운": 1.0,
        },
    ),
    "sensual": _mapping(
        families={"AMBERY": 1.5, "WOODY": 1.0, "FLORAL": 0.8},
        subs={"Floral Amber": 1.2, "Woody Amber": 1.0, "Dry Woods": 0.7},
        components={
            "Amber": 1.4,
            "Leather": 0.9,
            "Vanilla": 1.0,
            "Patchouli": 0.8,
            "Absolute Rose": 0.8,
        },
        descriptors={
            "감각적인": 1.8,
            "따뜻한": 1.1,
            "깊은": 0.9,
            "매력적인": 1.2,
        },
    ),
    "soft": _mapping(
        families={"FLORAL": 1.0, "AMBERY": 1.0},
        subs={"Soft Floral": 1.3, "Soft Amber": 1.2},
        components={
            "Musk": 1.2,
            "Iris": 1.0,
            "Vanilla": 0.8,
            "Lily": 0.7,
        },
        descriptors={
            "부드러운": 2.0,
            "포근한": 1.0,
            "온화한": 0.9,
        },
    ),
    "natural": _mapping(
        families={"FRESH": 1.3, "WOODY": 1.0},
        subs={"Green": 1.2, "Mossy Woods": 0.9, "Aromatic": 0.8},
        components={
            "Green Note": 1.2,
            "Oakmoss": 0.9,
            "Vetiver": 0.8,
            "Basil": 0.8,
        },
        descriptors={
            "신선한": 1.3,
            "청정한": 1.2,
            "상쾌한": 1.0,
        },
    ),
    "urban": _mapping(
        families={"FRESH": 0.8, "WOODY": 0.7, "AMBERY": 0.5},
        subs={"Aromatic": 0.8, "Soft Amber": 0.5},
        components={
            "Musk": 1.0,
            "Vetiver": 0.7,
            "Bergamot": 0.6,
        },
        descriptors={
            "도시적인": 1.3,
            "세련된": 1.1,
            "깨끗한": 0.7,
        },
    ),
    "calm": _mapping(
        families={"AMBERY": 0.8, "FRESH": 0.8, "WOODY": 0.6},
        subs={"Soft Amber": 0.8, "Green": 0.7, "Woods": 0.5},
        components={
            "Musk": 1.0,
            "Sandalwood": 0.7,
            "Green tea": 0.7,
        },
        descriptors={
            "차분한": 1.8,
            "부드러운": 0.9,
            "안정감": 0.8,
        },
    ),
    "bright": _mapping(
        families={"FRESH": 1.4, "FLORAL": 0.8},
        subs={"Citrus": 1.2, "Fruity": 0.8, "Floral": 0.7},
        components={
            "Bergamot": 1.1,
            "Lemon": 1.0,
            "Orange": 1.0,
            "Peony": 0.6,
        },
        descriptors={
            "밝은": 1.8,
            "상큼한": 1.2,
            "가벼운": 1.0,
        },
    ),
    "cozy": _mapping(
        families={"AMBERY": 1.3, "WOODY": 0.6},
        subs={"Soft Amber": 1.3, "Amber": 0.7},
        components={
            "Vanilla": 1.3,
            "Musk": 1.0,
            "Amber": 1.0,
            "Sandalwood": 0.6,
        },
        descriptors={
            "포근한": 1.8,
            "따뜻한": 1.2,
            "부드러운": 1.0,
        },
    ),
    # -----------------------------------------------------
    # season / time
    # -----------------------------------------------------
    "spring": _mapping(
        families={"FLORAL": 1.4, "FRESH": 1.3},
        subs={"Floral": 1.1, "Soft Floral": 1.0, "Green": 1.0, "Citrus": 0.6},
        components={
            "Peony": 1.2,
            "Absolute Rose": 1.0,
            "Green Note": 1.0,
            "Bergamot": 0.8,
            "Musk": 0.5,
        },
        descriptors={
            "신선한": 1.2,
            "상쾌한": 1.1,
            "밝은": 1.0,
            "부드러운": 0.8,
        },
    ),
    "summer": _mapping(
        families={"FRESH": 1.6},
        subs={"Citrus": 1.2, "Water": 1.0, "Green": 0.8},
        components={
            "Bergamot": 1.1,
            "Lemon": 1.0,
            "Marine": 0.9,
            "Green Note": 0.8,
        },
        descriptors={
            "시원한": 1.3,
            "상쾌한": 1.3,
            "가벼운": 1.0,
        },
    ),
    "autumn": _mapping(
        families={"WOODY": 1.2, "AMBERY": 1.0},
        subs={"Woods": 1.0, "Woody Amber": 0.9, "Amber": 0.8},
        components={
            "Sandalwood": 1.0,
            "Amber": 1.0,
            "Patchouli": 0.8,
            "Cedarwood": 0.8,
        },
        descriptors={
            "따뜻한": 1.0,
            "깊은": 0.9,
            "차분한": 0.8,
        },
    ),
    "winter": _mapping(
        families={"AMBERY": 1.4, "WOODY": 1.0},
        subs={"Amber": 1.2, "Soft Amber": 1.0, "Dry Woods": 0.8},
        components={
            "Amber": 1.3,
            "Vanilla": 1.0,
            "Incense": 0.8,
            "Sandalwood": 0.7,
        },
        descriptors={
            "따뜻한": 1.3,
            "포근한": 1.1,
            "묵직한": 0.8,
        },
    ),
    "morning": _mapping(
        families={"FRESH": 1.0},
        subs={"Citrus": 0.9, "Green": 0.8},
        components={
            "Bergamot": 0.9,
            "Lemon": 0.8,
            "Green Note": 0.7,
        },
        descriptors={
            "상쾌한": 1.0,
            "깨끗한": 0.8,
            "가벼운": 0.8,
        },
    ),
    "afternoon": _mapping(
        families={"FRESH": 0.9, "FLORAL": 0.7},
        subs={"Green": 0.7, "Soft Floral": 0.6, "Citrus": 0.5},
        components={
            "Bergamot": 0.7,
            "Green Note": 0.7,
            "Musk": 0.6,
            "Peony": 0.5,
        },
        descriptors={
            "밝은": 0.8,
            "상쾌한": 0.8,
            "가벼운": 0.7,
        },
    ),
    "evening": _mapping(
        families={"AMBERY": 1.0, "WOODY": 0.8},
        subs={"Soft Amber": 0.9, "Woody Amber": 0.7},
        components={
            "Amber": 1.0,
            "Musk": 0.8,
            "Sandalwood": 0.7,
        },
        descriptors={
            "따뜻한": 0.9,
            "차분한": 0.8,
            "깊은": 0.7,
        },
    ),
    "night": _mapping(
        families={"WOODY": 1.2, "AMBERY": 1.2},
        subs={"Dry Woods": 1.0, "Amber": 1.0, "Soft Amber": 0.8},
        components={
            "Leather": 0.9,
            "Amber": 1.0,
            "Incense": 0.9,
            "Musk": 0.8,
        },
        descriptors={
            "깊은": 1.1,
            "감각적인": 0.9,
            "묵직한": 0.8,
            "신비로운": 0.8,
        },
    ),
}


KOREAN_VISUAL_TRIGGERS: dict[str, str] = {
    "검정": "black",
    "검은": "black",
    "갈색": "brown",
    "브라운": "brown",
    "금색": "gold",
    "골드": "gold",
    "초록": "green",
    "녹색": "green",
    "파랑": "blue",
    "파란": "blue",
    "청록": "green",
    "흰색": "white",
    "하얀": "white",
    "분홍": "pink",
    "핑크": "pink",
    "빨강": "red",
    "빨간": "red",
    "베이지": "beige",
    "회색": "gray",
    "그레이": "gray",
    "드레스": "dress",
    "핸드백": "handbag",
    "가방": "handbag",
    "손가방": "handbag",
    "목걸이": "necklace",
    "주얼리": "necklace",
    "나무": "wood",
    "목재": "wood",
    "가죽": "leather",
    "레더": "leather",
    "꽃": "flower",
    "바다": "ocean",
    "커피": "coffee",
    "캔들": "candle",
    "책": "book",
    "천": "fabric",
    "패브릭": "fabric",
    "숲": "forest",
    "해변": "beach",
    "카페": "cafe",
    "바 ": "bar",
    "술집": "bar",
    "정원": "garden",
    "비": "rainy street",
    "도시": "city",
    "방": "room",
    "실내": "indoor",
    "오피스": "office",
    "사무실": "office",
    "현대적인": "modern",
    "모던": "modern",
    "패션": "fashion",
    "스타일": "style",
    "여성": "feminine",
    "여성적": "feminine",
    "우아": "elegant",
    "엘레강스": "elegant",
    "동시대": "contemporary",
    "세련": "contemporary",
    "럭셔리": "luxury",
    "고급": "luxurious",
    "따뜻": "warm",
    "어두": "dark",
    "깨끗": "clean",
    "상쾌": "fresh",
    "신선": "fresh",
    "로맨틱": "romantic",
    "감각": "sensual",
    "관능": "sensual",
    "자연": "natural",
    "차분": "calm",
    "포근": "cozy",
    "밝": "bright",
    "부드": "soft",
    "봄": "spring",
    "여름": "summer",
    "가을": "autumn",
    "겨울": "winter",
    "오전": "morning",
    "아침": "morning",
    "오후": "afternoon",
    "저녁": "evening",
    "밤": "night",
}


# EOF: scent_engine/rules.py
