/**
 * @file types.ts
 * @description 애플리케이션 전역에서 사용되는 인터페이스 및 공통 타입들을 정의합니다.
 */

export type ScentType = "personal";

export interface Product {
  id: number;
  name: string;
  brand: string;
  price: string;
  size: string;
  image: string;
  tags: string[];
  notes: string;
  family: string;
  mainAccords?: string[];   // ✅ optional로 변경 (백엔드 미제공)
  moods?: string[];         // ✅ optional로 변경 (백엔드 미제공)
  occasions?: string[];     // ✅ optional로 변경 (백엔드 미제공)
  featured?: boolean;
  category: "Personal";
  similarity?: number;
  matchReason?: string;
  details: {
    story: string;
    topNotes: string;
    middleNotes: string;
    baseNotes: string;
    bestFor: string;
  };
}

export interface AnalysisResults {
  type: ScentType;
  personalMood?: string;
  perfumeKeywords?: string[];
  fashionStyle?: string;
  readableQuery?: string;   // ✅ 백엔드가 내려주는 필드 추가
  analysisMetadata?: {
    base64Image: string;
    selectedNotes: string[];
    radarScores?: Record<string, number>;
  };
  recommendations?: (Product & { similarity: number; matchReason: string })[];
}

// EOF: types.ts
