import base64
import json
import re
from io import BytesIO
from pathlib import Path
from typing import Any
from PIL import Image

MAX_ITEMS = {
    "colors": 5,
    "objects": 6,
    "scene": 3,
    "mood": 4,
    "season": 1,
    "time": 1,
    "raw_keywords": 8,
}

def encode_image_to_base64(
    image_path_or_file: Any,
    max_size: int = 768,
    quality: int = 85,
) -> str:
    """
    이미지를 자동 리사이즈 후 base64로 변환한다.
    """
    if isinstance(image_path_or_file, (str, Path)):
        img = Image.open(image_path_or_file).convert("RGB")
    else:
        img = Image.open(image_path_or_file).convert("RGB")

    img.thumbnail((max_size, max_size))
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def _dedupe_list(values: list[str], max_items: int | None = None) -> list[str]:
    seen = set()
    result = []
    for value in values:
        cleaned = str(value).strip().lower()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
        if max_items is not None and len(result) >= max_items:
            break
    return result

def _ensure_list(value: Any, key: str) -> list[str]:
    if value is None:
        values = []
    elif isinstance(value, list):
        values = [str(v).strip().lower() for v in value if str(v).strip()]
    elif isinstance(value, str):
        values = [value.strip().lower()] if value.strip() else []
    else:
        values = [str(value).strip().lower()] if str(value).strip() else []
    return _dedupe_list(values, MAX_ITEMS.get(key))

def normalize_vlm_result(data: dict[str, Any]) -> dict[str, Any]:
    """
    이미지 분석 결과의 키와 타입을 고정한다.
    """
    return {
        "visual_summary": str(data.get("visual_summary", "")).strip(),
        "colors": _ensure_list(data.get("colors", []), "colors"),
        "objects": _ensure_list(data.get("objects", []), "objects"),
        "scene": _ensure_list(data.get("scene", []), "scene"),
        "mood": _ensure_list(data.get("mood", []), "mood"),
        "season": _ensure_list(data.get("season", []), "season"),
        "time": _ensure_list(data.get("time", []), "time"),
        "raw_keywords": _ensure_list(data.get("raw_keywords", []), "raw_keywords"),
    }

def extract_json_from_text(text: str) -> dict[str, Any]:
    """
    텍스트에서 JSON을 추출하고 실패 시 부분 복구를 시도한다.
    """
    text = text.strip()
    # 1. Clean markdown blocks
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    
    # 2. Try direct load
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 3. Try to find the outermost {}
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and start < end:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    # 4. Fallback: Robust field extraction
    return _fallback_parse_partial_json(text)

def _extract_string_field(text: str, key: str) -> str:
    pattern = rf'"{re.escape(key)}"\s*:\s*"([^"]*)"'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

def _extract_array_field(text: str, key: str, max_items: int) -> list[str]:
    key_pattern = rf'"{re.escape(key)}"\s*:\s*'
    key_match = re.search(key_pattern, text)
    if not key_match:
        return []
    start = key_match.end()
    remaining = text[start:].lstrip()
    if remaining.startswith('"'):
        val = re.match(r'"([^"]*)"', remaining, re.DOTALL)
        return _dedupe_list([val.group(1)], max_items) if val else []
    if not remaining.startswith("["):
        return []
    
    # Extract strings within brackets
    chunk_match = re.search(r'\[(.*?)\]', remaining, re.DOTALL)
    if chunk_match:
        values = re.findall(r'"([^"]+)"', chunk_match.group(1))
        return _dedupe_list(values, max_items)
    return []

def _fallback_parse_partial_json(text: str) -> dict[str, Any]:
    recovered = {
        "visual_summary": _extract_string_field(text, "visual_summary"),
        "colors": _extract_array_field(text, "colors", MAX_ITEMS["colors"]),
        "objects": _extract_array_field(text, "objects", MAX_ITEMS["objects"]),
        "scene": _extract_array_field(text, "scene", MAX_ITEMS["scene"]),
        "mood": _extract_array_field(text, "mood", MAX_ITEMS["mood"]),
        "season": _extract_array_field(text, "season", MAX_ITEMS["season"]),
        "time": _extract_array_field(text, "time", MAX_ITEMS["time"]),
        "raw_keywords": _extract_array_field(text, "raw_keywords", MAX_ITEMS["raw_keywords"]),
    }
    return normalize_vlm_result(recovered)
