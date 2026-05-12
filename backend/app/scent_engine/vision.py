"""
@file vision.py
@module ScentEngine/Vision
@description
NVIDIA NIM API를 통해 시각적 요소를 텍스트 맥락으로 변환하는 Vision-Language 엔진입니다.
이미지 내의 색상, 사물, 전체적인 무드를 추출하여 향수 매칭의 첫 단추를 제공합니다.

@author Olfít AI Team
@version 4.0.0
"""

import os
import json
import time
from openai import OpenAI
from .utils import extract_json_from_text, normalize_vlm_result
from .prompts import IMAGE_ANALYSIS_PROMPT

class VLEngine:
    """
    [Core VLM Engine]
    NVIDIA NIM (Gemma-VLM) 또는 OpenAI/Gemini 계열 모델을 사용하여
    이미지의 시각적 속성을 Olfít 표준 데이터 규격으로 추출합니다.
    """
    
    def __init__(self, api_key=None, model="google/gemma-3n-e4b-it", temperature=0.1):
        """
        엔진 초기화 및 API 설정 로드.
        """
        from dotenv import load_dotenv
        load_dotenv()
        
        # NVIDIA NIM API 엔드포인트 설정
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = model 
        self.temperature = temperature
        
        if self.api_key:
            print(f"[VLEngine] ✅ Engine Ready | Provider: NVIDIA | Model: {self.model}")
        else:
            print("[VLEngine] ❌ Critical: NVIDIA_API_KEY not found in environment.")

    def analyze_image(self, image_base64):
        """
        이미지를 분석하여 구조화된 JSON 결과를 반환합니다.
        
        @param image_base64: 분석할 이미지의 Base64 인코딩 문자열
        @return: 정규화된 분석 결과 (visual_summary, mood, colors 등)
        """
        if not self.api_key:
            print("[VLEngine] ⚠️ No API Key detected. Falling back to DUMMY MODE.")
            return self._get_dummy_result()

        # [Pre-processing] 데이터 URI 접두사 제거 및 정제
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]
        image_base64 = image_base64.strip()

        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

        try:
            print(f"\n[VLEngine] >>> ATTEMPTING NVIDIA API CALL <<<")
            start_t = time.time()
            
            # NVIDIA NIM API 호출 (OpenAI SDK 호환)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": IMAGE_ANALYSIS_PROMPT}, # lib/scent_engine/prompts.py 참조
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                temperature=self.temperature,
                timeout=50.0
            )
            
            content = response.choices[0].message.content
            duration = time.time() - start_t
            
            print(f"[VLEngine] <<< NVIDIA API RESPONDED ({duration:.2f}s) >>>")
            
            # [Parsing] 텍스트에서 JSON 추출 및 정규화
            parsed = extract_json_from_text(content)
            
            # [Post-processing] 한국어 문장 마무리 정제 (마침표 기준)
            if "visual_summary" in parsed and isinstance(parsed["visual_summary"], str):
                summary = parsed["visual_summary"].strip()
                if "." in summary:
                    parsed["visual_summary"] = summary[:summary.rfind(".")+1]
                
                if not parsed["visual_summary"]:
                    parsed["visual_summary"] = "스타일리시한 분위기가 느껴지는 이미지입니다."

            return normalize_vlm_result(parsed) # lib/scent_engine/utils.py 참조

        except Exception as e:
            print(f"[VLEngine] ❌ Analysis Failed: {e}")
            return self._get_dummy_result()

    def _get_dummy_result(self):
        """API 호출 실패 시 서비스 중단을 방지하기 위한 Fallback 데이터"""
        return {
            "visual_summary": "도시적인 세련미가 느껴지는 현대적인 스타일입니다.",
            "colors": ["black", "gray", "white"],
            "objects": ["handbag", "dress"],
            "scene": ["city", "indoor"],
            "mood": ["modern", "urban", "luxurious"],
            "season": ["autumn"],
            "time": ["afternoon"],
            "raw_keywords": ["세련된", "미니멀", "시크한"]
        }

# EOF: vision.py
