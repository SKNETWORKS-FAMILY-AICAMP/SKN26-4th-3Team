import { memo, useCallback } from "react"; // 🛠️ REFACTOR (성능 최적화): memo, useCallback 도입
import { Check, RotateCcw, Share2 } from "lucide-react";
import ProductCarousel from "./ProductCarousel";
import type { Product } from "@/data/productData";
import type { ScentNote } from "@/data/noteData";

interface RecommendationListProps {
  recommendations: (Product & { similarity: number, matchReason: string })[];
  onProductClick: (product: Product) => void;
  slots: {
    Top: ScentNote | null;
    Middle: ScentNote | null;
    Base: ScentNote | null;
  };
  sortBy: "recommended" | "price";
  onSortChange: (sort: "recommended" | "price") => void;
  onRestart: () => void;
  isSaving: boolean;
  feedback: string | null;
  onShare: () => void;
}

function RecommendationList({ 
  recommendations, 
  onProductClick, 
  slots, 
  sortBy, 
  onSortChange,
  onRestart,
  isSaving,
  feedback,
  onShare
}: RecommendationListProps) {
  const sortButtonClass = "h-8 min-w-[72px] px-5 inline-flex items-center justify-center rounded-full text-[10px] leading-none font-medium uppercase tracking-widest [text-indent:0.15em] transition-all hover:font-bold";
  const sortLabelClass = "inline-block leading-none translate-y-[1.5px]";

  // 🛠️ REFACTOR (성능 최적화): 핸들러 메모이제이션으로 하위 컴포넌트 리렌더링 방지
  const handleRecommendedSort = useCallback(() => onSortChange("recommended"), [onSortChange]);
  const handlePriceSort = useCallback(() => onSortChange("price"), [onSortChange]);
  const handleRestart = useCallback(() => onRestart(), [onRestart]);
  const handleShare = useCallback(() => onShare(), [onShare]);

  return (
    <div className="mt-32 pt-24 border-t border-wood/10">
      <div className="flex flex-col items-center mb-16 gap-8">
        <div
          className="inline-flex h-10 items-center gap-1 p-1 bg-wood/5 rounded-full border border-wood/10"
          data-capture-sort-group={sortBy}
        >
          <button
            type="button"
            onClick={handleRecommendedSort}
            className={`${sortButtonClass} ${
              sortBy === "recommended" ? "bg-wood text-cream shadow-md" : "text-wood"
            }`}
            data-capture-pill="sort"
          >
            <span className={sortLabelClass}>추천순</span>
          </button>
          <button
            type="button"
            onClick={handlePriceSort}
            className={`${sortButtonClass} ${
              sortBy === "price" ? "bg-wood text-cream shadow-md" : "text-wood"
            }`}
            data-capture-pill="sort"
          >
            <span className={sortLabelClass}>가격순</span>
          </button>
        </div>

        <div className="text-center">
          <p className="text-[10px] font-bold uppercase tracking-[0.3em] text-wood/30 mb-2">Matching Selection</p>
          <h3 className="text-2xl font-light tracking-tight text-wood">당신의 스타일을 닮은 향기</h3>
          
          {recommendations.length > 0 && (
            <div
              className="mt-6 max-w-lg mx-auto px-6 py-4 bg-wood/[0.03] border border-wood/10 rounded-sm"
              data-capture-exclude="true"
            >
              <p className="text-[13px] text-wood leading-relaxed italic break-keep text-balance">
                "{recommendations[0].matchReason}"
              </p>
            </div>
          )}
        </div>
      </div>

      <ProductCarousel 
        products={recommendations} 
        onProductClick={onProductClick} 
        slots={slots}
      />

      <div className="mt-16 flex flex-col items-center gap-5 px-4" data-capture-exclude="true">
        <p className="max-w-xl text-center text-[12px] leading-relaxed text-wood/50 break-keep">
          저장하고 싶은 향수 카드를 화면에 띄운 뒤 Share & Save Report를 눌러주세요.
        </p>
        <div className="grid w-full max-w-3xl grid-cols-1 gap-3 sm:grid-cols-2">
          <button
            type="button"
            onClick={handleShare}
            onDoubleClick={(e) => e.preventDefault()}
            disabled={isSaving || !!feedback}
            className={`group inline-flex h-12 items-center justify-center gap-3 rounded-sm border px-8 text-[11px] font-bold uppercase tracking-widest transition-all duration-300 active:scale-[0.99] ${
              isSaving
                ? "border-wood/10 bg-wood/5 text-wood/30 cursor-not-allowed"
                : feedback
                  ? "border-green-200 bg-green-50 text-green-600"
                  : "border-wood bg-wood text-cream hover:bg-wood/90 hover:shadow-lg"
            }`}
          >
            {isSaving ? (
              <>
                <div className="w-3 h-3 border-2 border-wood/20 border-t-wood rounded-full animate-spin" />
                <span className="hidden sm:inline">고화질 리포트 생성 중</span>
                <span className="sm:hidden">생성 중</span>
              </>
            ) : feedback ? (
              <>
                <Check size={15} />
                <span>{feedback}</span>
              </>
            ) : (
              <>
                <Share2 size={15} className="transition-transform group-hover:rotate-12" />
                <span>Share & Save Report</span>
              </>
            )}
          </button>

          <button
            type="button"
            onClick={handleRestart}
            className="group inline-flex h-12 items-center justify-center gap-3 rounded-sm border border-wood/20 px-8 text-[11px] font-bold uppercase tracking-widest text-wood transition-all duration-300 hover:bg-wood/[0.06] active:scale-[0.99]"
          >
            <RotateCcw size={14} className="transition-transform duration-300 group-hover:-rotate-45" />
            <span>분석 리포트 다시해보기</span>
          </button>
        </div>
      </div>
    </div>
  );
}

// 🛠️ REFACTOR (성능 최적화): 결과 리스트 컴포넌트 메모이제이션
export default memo(RecommendationList);
