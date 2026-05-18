"""
 @backend\app\scent_engine\__init__.py
 @role
Scent Engine 패키지의 진입점(Entry Point)이자 파사드(Facade) 인터페이스 파일입니다.
VLEngine, 매퍼 함수 등 패키지 내부의 핵심 기능을 외부 모듈에서 간결하게 참조할 수 있도록 노출(Export)합니다.
"""

# ----------------------------------------------------------------
# Update History
# 2026-05-11: __init__.py 설정 (worker: Gloveman)
# ----------------------------------------------------------------

from .mapper import map_image_to_fragrance_keywords
from .aliases import normalize_note_keyword, to_korean_note
from .vision import VLEngine

# EOF: __init__.py
