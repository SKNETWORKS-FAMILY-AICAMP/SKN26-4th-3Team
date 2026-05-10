import { create } from 'zustand';
import type { AnalysisResults } from '@/types';
import type { Product } from '@/data/productData';

interface OlfitState {
  /** AI 분석 결과 */
  analysisResults: AnalysisResults | null;
  /** 사용자가 선택한 향기 노트 */
  selectedNotes: string[];
  /** 개인정보 동의 여부 */
  hasConsented: boolean;
  /** 선택된 상세 제품 */
  selectedProduct: Product | null;
  /** 로딩 상태 */
  isLoading: boolean;
  /** 에러 메시지 */
  error: string | null;

  // Actions
  setAnalysisResults: (results: AnalysisResults | null) => void;
  setSelectedNotes: (notes: string[]) => void;
  setHasConsented: (consented: boolean) => void;
  setSelectedProduct: (product: Product | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  resetAll: () => void;
}

export const useOlfitStore = create<OlfitState>((set) => ({
  analysisResults: null,
  selectedNotes: [],
  hasConsented: (() => {
    if (typeof window === "undefined") return false;
    const consented = localStorage.getItem("olfit_consent") === "true";
    const sessionId = localStorage.getItem("olfit_session_id");
    return !!(consented && sessionId);
  })(),
  selectedProduct: null,
  isLoading: false,
  error: null,

  setAnalysisResults: (results) => set({ analysisResults: results }),
  setSelectedNotes: (notes) => set({ selectedNotes: notes }),
  setHasConsented: (consented) => set({ hasConsented: consented }),
  setSelectedProduct: (product) => set({ selectedProduct: product }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error: error }),
  resetAll: () => set({
    analysisResults: null,
    selectedNotes: [],
    selectedProduct: null,
    error: null
  }),
}));
