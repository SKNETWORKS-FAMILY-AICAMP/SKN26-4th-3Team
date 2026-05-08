/**
 * @file ProductCarousel.tsx
 * @description 추천된 제품들을 1개씩 자동으로 보여주는 캐러셀 컴포넌트입니다.
 */

import { useCallback } from "react";
import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import { ArrowRight } from "lucide-react";
import type { Product } from "@/data/productData";

interface ProductCarouselProps {
  products: (Product & { similarity: number })[];
  onProductClick: (product: Product) => void;
}

export default function ProductCarousel({ products, onProductClick }: ProductCarouselProps) {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: true }, [
    Autoplay({ delay: 30000, stopOnInteraction: false })
  ]);

  const scrollPrev = useCallback(() => emblaApi && emblaApi.scrollPrev(), [emblaApi]);
  const scrollNext = useCallback(() => emblaApi && emblaApi.scrollNext(), [emblaApi]);

  return (
    <div>
      <div className="relative max-w-4xl mx-auto px-12">
        <div className="overflow-hidden" ref={emblaRef}>
          <div className="flex">
            {products.map((item) => (
              <div key={item.id} className="flex-[0_0_100%] min-w-0 px-4">
                <div 
                  onClick={() => onProductClick(item)}
                  data-family={item.family}
                  className="group cursor-pointer bg-white/50 backdrop-blur-sm border border-wood/5 p-8 sm:p-12 rounded-sm hover:bg-wood hover:border-wood transition-all duration-700 overflow-hidden flex flex-col md:flex-row items-center gap-10"
                >
                  <div className="w-full md:w-1/2 aspect-square overflow-hidden bg-cream/50 rounded-sm relative">
                    <img 
                      src={item.image} 
                      alt={item.name} 
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000" 
                    />
                    <div className="absolute top-4 right-4 bg-wood/80 text-cream px-3 py-1 rounded-full text-[10px] font-mono group-hover:bg-cream group-hover:text-wood transition-colors">
                      {item.similarity}% Match
                    </div>
                  </div>
                  
                  <div className="w-full md:w-1/2 text-left">
                    <p className="text-[11px] uppercase tracking-[0.2em] text-wood/40 group-hover:text-cream/40 mb-2 transition-colors">{item.brand}</p>
                    <h4 className="text-2xl sm:text-3xl font-light text-wood group-hover:text-cream mb-6 break-keep transition-colors leading-tight">
                      {item.name}
                    </h4>
                    
                    <div className="space-y-4 mb-8">
                      <div>
                        <span className="text-[10px] uppercase tracking-widest text-wood/30 group-hover:text-cream/30 block mb-1 transition-colors">Notes</span>
                        <p className="text-sm text-wood/70 group-hover:text-cream/70 line-clamp-2 break-keep transition-colors">
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

        {/* Navigation Buttons */}
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
