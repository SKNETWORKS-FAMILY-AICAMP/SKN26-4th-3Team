/**
 * @file api.ts
 * @module Frontend/Services/API
 * @description
 * Olfít Connect의 통합 API 클라이언트입니다.
 * 프론트엔드에서 발생하는 모든 백엔드 통신(이미지 분석, 추천 요청 등)을 담당하며,
 * 익명 세션 관리(X-Session-ID)와 공통 에러 핸들링 로직이 포함되어 있습니다.
 * 
 * @author Olfít AI Team
 * @version 1.0.0
 */

import axios from 'axios';
import { useOlfitStore } from '@/store/useStore';

/**
 * 백엔드 서버 주소 (환경 변수 또는 로컬 환경)
 */
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // VLM 추론을 위해 넉넉한 타임아웃(60s) 부여
});

// [Interceptor] 응답 공통 처리 및 에러 스토어 연결
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const { setError } = useOlfitStore.getState();
    
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.message || error.message || '서버와의 통신 중 오류가 발생했습니다.';
      setError(message);
      console.error('[API Error]:', message);
    } else {
      setError('알 수 없는 오류가 발생했습니다.');
    }
    
    return Promise.reject(error);
  }
);

/**
 * [Main API] AI 아우라 분석 요청을 백엔드로 전송합니다.
 * 
 * @param base64Image - 사용자가 업로드한 OOTD/무드 이미지 (Base64 형식)
 * @param selectedNotes - 사용자가 선택한 명시적 향기 성분 리스트
 * @returns {Promise<AnalysisResults>} - 분석 점수, 키워드, 추천 제품 리스트가 포함된 결과 객체
 */
export const requestAuraAnalysis = async (base64Image: string, selectedNotes: string[]) => {
  const { setLoading, setError } = useOlfitStore.getState();
  
  // localStorage에서 익명 세션 UUID 획득 (Privacy Consent 단계에서 생성됨)
  const sessionId = localStorage.getItem("olfit_session_id");
  
  try {
    setLoading(true);
    setError(null);
    
    // 백엔드로 POST 요청 (세션 ID 헤더 포함)
    const response = await api.post('/api/analyze/', {
      image: base64Image,
      selectedNotes: selectedNotes,
    }, {
      headers: {
        'X-Session-ID': sessionId || ''
      }
    });
    
    return response.data;
  } finally {
    setLoading(false);
  }
};

export default api;

/**
 * @footer
 * Olfít Connect Project - Unified Frontend API Client
 */
