/**
 * @file ProductCarousel.tsx
 * @description AI 분석을 통해 선정된 추천 제품들을 카드 형태로 보여주는 캐러셀 컴포넌트입니다.
 * Embla Carousel을 기반으로 자동 전환, 수동 슬라이드, 제품 피드백(좋아요/싫어요) 기능을 제공합니다.
 */

import { useCallback, useState } from "react";
import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import { ArrowRight, ThumbsUp, ThumbsDown } from "lucide-react";
import { toast } from "sonner";
import type { Product } from "@/data/productData";
import type { ScentNote } from "@/data/noteData";

interface ProductCarouselProps {
  /** 추천된 제품 리스트 (유사도 점수 포함) */
  products: (Product & { similarity: number })[];
  /** 제품 선택 시 호출되는 핸들러 */
  onProductClick: (product: Product) => void;
  /** 사용자가 선택한 노트 정보 */
  slots: {
    Top: ScentNote | null;
    Middle: ScentNote | null;
    Base: ScentNote | null;
  };
}

type Feedback = "like" | "dislike" | null;

export default function ProductCarousel({ products, onProductClick, slots }: ProductCarouselProps) {
  /** 캐러셀 엔진 및 자동 재생 설정 (30초 간격) */
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: true }, [
    Autoplay({ delay: 30000, stopOnInteraction: false })
  ]);
  
  /** 각 제품별 피드백 상태 관리 */
  const [feedbacks, setFeedbacks] = useState<Record<number, Feedback>>({});

  const scrollPrev = useCallback(() => emblaApi && emblaApi.scrollPrev(), [emblaApi]);
  const scrollNext = useCallback(() => emblaApi && emblaApi.scrollNext(), [emblaApi]);

  /**
   * 제품에 대한 긍정/부정 피드백 처리
   */
  const handleFeedback = (e: React.MouseEvent, productId: number, type: Feedback) => {
    e.stopPropagation(); // 카드 클릭(모달 열기) 방지
    
    const currentFeedback = feedbacks[productId];
    const newFeedback = currentFeedback === type ? null : type;
    
    setFeedbacks(prev => ({ ...prev, [productId]: newFeedback }));
    
    // 사용자 경험 향상을 위한 토스트 알림
    if (newFeedback === "like") {
      toast.success("이 향수를 위시리스트에 담았습니다.");
    } else if (newFeedback === "dislike") {
      toast.info("취향 피드백이 반영되었습니다.");
    }
  };

  return (
    <div>
      <div className="relative max-w-4xl mx-auto px-12">
        <div className="overflow-hidden" ref={emblaRef}>
          <div className="flex">
            {products.map((item, index) => (
              <div key={item.id} className="flex-[0_0_100%] min-w-0 px-4">
                <div 
                  onClick={() => onProductClick(item)}
                  data-family={item.family}
                  className="group cursor-pointer bg-white/50 backdrop-blur-sm border border-wood/5 p-8 sm:p-12 rounded-sm hover:bg-wood hover:border-wood transition-all duration-700 overflow-hidden flex flex-col md:flex-row items-center gap-10"
                >
                  {/* 제품 이미지 및 유사도 배지 */}
                  <div className="w-full md:w-1/2 aspect-square overflow-hidden bg-cream/50 rounded-sm relative">
                    <img 
                      src={item.image} 
                      alt={item.name} 
                      crossOrigin="anonymous"
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000" 
                    />
                    <div className="absolute top-4 right-4 bg-wood/80 text-cream px-3 py-1 rounded-full text-[10px] font-mono group-hover:bg-cream group-hover:text-wood transition-colors">
                      {item.similarity}% Match
                    </div>
                  </div>
                  
                  {/* 제품 정보 영역 */}
                  <div className="w-full md:w-1/2 text-left relative">
                    {/* 상단 피드백 버튼 그룹 */}
                    <div className="absolute top-0 right-0 flex gap-2">
                      <button
                        onClick={(e) => handleFeedback(e, item.id, "like")}
                        className={`p-2 rounded-full transition-all duration-300 ${
                          feedbacks[item.id] === "like"
                            ? "bg-wood text-cream group-hover:bg-cream group-hover:text-wood scale-110"
                            : "bg-wood/5 text-wood/40 group-hover:bg-cream/10 group-hover:text-cream/40 hover:scale-110"
                        }`}
                      >
                        <ThumbsUp size={14} fill={feedbacks[item.id] === "like" ? "currentColor" : "none"} />
                      </button>
                      <button
                        onClick={(e) => handleFeedback(e, item.id, "dislike")}
                        className={`p-2 rounded-full transition-all duration-300 ${
                          feedbacks[item.id] === "dislike"
                            ? "bg-red-900/80 text-cream scale-110"
                            : "bg-wood/5 text-wood/40 group-hover:bg-cream/10 group-hover:text-cream/40 hover:scale-110 hover:text-red-400"
                        }`}
                      >
                        <ThumbsDown size={14} fill={feedbacks[item.id] === "dislike" ? "currentColor" : "none"} />
                      </button>
                    </div>

                    {/* 베스트 추천 표시 */}
                    {index === 0 && (
                      <div className="inline-flex items-center justify-center px-2 py-1 bg-wood/10 border border-wood/20 rounded-sm mb-3 group-hover:bg-cream/10 group-hover:border-cream/30 transition-colors">
                        <span className="text-[9px] font-bold text-wood group-hover:text-cream tracking-[0.15em] uppercase leading-none">Best Pick</span>
                      </div>
                    )}
                    <p className="text-[11px] uppercase tracking-[0.2em] text-wood/40 group-hover:text-cream/40 mb-2 transition-colors">{item.brand}</p>
                    <h4 className="text-2xl sm:text-3xl font-light text-wood group-hover:text-cream mb-6 break-keep transition-colors leading-tight pr-16">
                      {item.name}
                    </h4>
                    
                    {/* 요약 상세 정보 */}
                    <div className="space-y-4 mb-8">
                      <div>
                        <span className="text-[10px] uppercase tracking-widest text-wood/30 group-hover:text-cream/30 block mb-1 transition-colors">Notes</span>
                        <p className="text-sm text-wood/70 group-hover:text-cream/70 line-clamp-2 break-keep text-balance transition-colors">
                          {item.notes}
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-x-8 gap-y-4">
                        <div>
                          <span className="text-[10px] uppercase tracking-widest text-wood/30 group-hover:text-cream/30 block mb-1 transition-colors">Family</span>
                          <p className="text-sm font-medium text-wood group-hover:text-cream transition-colors">{item.family}</p>
                        </div>
                        <div>
                          <span className="text-[10px] uppercase tracking-widest text-wood/30 group-hover:text-cream/30 block mb-1 transition-colors">Size</span>
                          <p className="text-sm font-medium text-wood group-hover:text-cream transition-colors">{item.size}</p>
                        </div>
                        <div>
                          <span className="text-[10px] uppercase tracking-widest text-wood/30 group-hover:text-cream/30 block mb-1 transition-colors">Price</span>
                          <p className="text-sm font-medium text-wood group-hover:text-cream transition-colors">{item.price}</p>
                        </div>
                      </div>
                    </div>

                    {/* 추가 블록 2: 매칭 근거 텍스트 (Why This Scent) */}
                    <div className="mb-6 opacity-0 group-hover:opacity-100 transition-opacity duration-700 delay-100">
                      <p className="text-cream/60 text-xs italic break-keep">
                        당신이 설계한 '{slots.Base?.name || slots.Middle?.name || slots.Top?.name || "선택된"}' 향기가 이 향수의 {item.family} 분위기를 완성해 줍니다
                      </p>
                    </div>

                    <div className="inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.2em] text-wood group-hover:text-cream pt-6 border-t border-wood/10 group-hover:border-cream/20 transition-all">
                      <span>Explore Details</span>
                      <ArrowRight size={14} className="group-hover:translate-x-2 transition-transform" />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 좌우 이동 네비게이션 버튼 */}
        <button 
          onClick={scrollPrev}
          className="absolute left-0 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center text-wood/20 hover:text-wood transition-colors"
        >
          <div className="w-full h-px bg-current rotate-[-45deg] absolute transform origin-left scale-x-50" />
          <div className="w-full h-px bg-current rotate-[45deg] absolute transform origin-left scale-x-50" />
          <span className="sr-only">Previous</span>
        </button>
        <button 
          onClick={scrollNext}
          className="absolute right-0 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center text-wood/20 hover:text-wood transition-colors"
        >
          <div className="w-full h-px bg-current rotate-[45deg] absolute transform origin-right scale-x-50" />
          <div className="w-full h-px bg-current rotate-[-45deg] absolute transform origin-right scale-x-50" />
          <span className="sr-only">Next</span>
        </button>
      </div>
      
      <p className="text-[9px] text-wood/20 mt-12 text-center uppercase tracking-[0.3em] italic animate-pulse">
        Automatic rotation every 30 seconds
      </p>
    </div>
  );
}

// EOF: ProductCarousel.tsx
