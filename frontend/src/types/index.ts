/**
 * @file types.ts
 * @description 애플리케이션 전역에서 사용되는 인터페이스 및 공통 타입들을 정의합니다.
 */

/**
 * 향기 분석 서비스 타입 (확장성을 고려한 정의)
 */
export type ScentType = "personal";

/**
 * AI 인터뷰 최종 분석 결과 데이터 구조
 */
export interface AnalysisResults {
  /** 분석 타입 */
  type: ScentType;
  /** 이미지 분석을 통해 도출된 핵심 무드 키워드 */
  personalMood?: string;
  /** 향수 관련 변환 키워드 */
  perfumeKeywords?: string[];
  /** 이미지 분석을 통해 도출된 패션 스타일 키워드 */
  fashionStyle?: string;
  /** 분석 과정에서 사용된 원천 데이터 및 메타데이터 */
  analysisMetadata?: {
    /** 분석에 사용된 원본 이미지 (Base64) */
    base64Image: string;
    /** 사용자가 직접 선택한 선호 향기 노트 리스트 */
    selectedNotes: string[];
    /** 백엔드에서 계산된 레이더 차트 수치 */
    radarScores?: Record<string, number>;
  };
  /** 백엔드에서 추천된 향수 리스트 */
  recommendations?: any[];
}

// EOF: types.ts
