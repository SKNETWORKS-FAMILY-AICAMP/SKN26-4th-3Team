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
}

export default function RecommendationList({ 
  recommendations, 
  onProductClick, 
  slots, 
  sortBy, 
  onSortChange 
}: RecommendationListProps) {
  return (
    <div className="mt-32 pt-24 border-t border-wood/10">
      <div className="flex flex-col items-center mb-16 gap-8">
        <div className="flex items-center gap-2 p-1 bg-wood/5 rounded-full border border-wood/10">
          <button
            onClick={() => onSortChange("recommended")}
            className={`px-6 py-2 rounded-full text-[10px] font-medium uppercase tracking-widest transition-all ${
              sortBy === "recommended" ? "bg-wood text-cream shadow-md" : "text-wood/40 hover:text-wood"
            }`}
          >
            추천순
          </button>
          <button
            onClick={() => onSortChange("price")}
            className={`px-6 py-2 rounded-full text-[10px] font-medium uppercase tracking-widest transition-all ${
              sortBy === "price" ? "bg-wood text-cream shadow-md" : "text-wood/40 hover:text-wood"
            }`}
          >
            가격순
          </button>
        </div>

        <div className="text-center">
          <p className="text-[10px] font-bold uppercase tracking-[0.3em] text-wood/30 mb-2">Matching Selection</p>
          <h3 className="text-2xl font-light tracking-tight text-wood">당신의 스타일을 닮은 향기</h3>
          
          {recommendations.length > 0 && (
            <div className="mt-6 max-w-lg mx-auto px-6 py-4 bg-wood/[0.03] border border-wood/10 rounded-sm">
              <p className="text-[13px] text-wood/70 leading-relaxed italic break-keep text-balance">
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
    </div>
  );
}
