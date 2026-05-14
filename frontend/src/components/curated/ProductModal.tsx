/**
 * @file ProductModal.tsx
 * @description 특정 향수 제품의 상세 정보를 아름답고 상세하게 보여주는 전체 화면 모달 컴포넌트입니다.
 * 제품의 비주얼, 조향 스토리, 노트 피라미드 및 추천 사용 상황 정보를 제공합니다.
 */

import { X, MapPin, Sparkles, Wind } from "lucide-react";
import type { Product } from "@/data/productData";

interface ProductModalProps {
  /** 표시할 제품의 상세 데이터 객체 */
  product: Product;
  /** 모달을 닫는 함수 */
  onClose: () => void;
}

export default function ProductModal({ product, onClose }: ProductModalProps) {
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 md:p-10">
      {/* 백드롭 레이어: 클릭 시 모달 닫힘 */}
      <div 
        className="absolute inset-0 bg-wood/60 backdrop-blur-md animate-in fade-in duration-500" 
        onClick={onClose} 
      />
      
      {/* 모달 콘텐츠 레이아웃 */}
      <div className="relative bg-cream w-full max-w-5xl max-h-[90vh] overflow-y-auto rounded-sm shadow-2xl animate-in zoom-in-95 fade-in duration-500 flex flex-col md:flex-row">
        {/* 우측 상단 닫기 버튼 */}
        <button 
          onClick={onClose}
          className="absolute top-6 right-6 z-10 p-2 hover:bg-wood/5 rounded-full transition-colors"
          aria-label="모달 닫기"
        >
          <X size={24} className="text-wood" />
        </button>

        {/* 좌측 섹션: 제품 대형 이미지 */}
        <div className="md:w-1/2 bg-stone-100 flex items-center justify-center p-8 md:p-12">
          <div className="aspect-[3/4] w-full max-w-[360px] shadow-editorial overflow-hidden">
            <img 
              src={product.image} 
              alt={product.name} 
              className="w-full h-full object-cover mix-blend-multiply opacity-90"
            />
          </div>
        </div>

        {/* 우측 섹션: 텍스트 정보 및 상세 명세 */}
        <div className="md:w-1/2 p-8 md:p-16 flex flex-col text-wood">
          <div className="mb-10">
            {/* 태그 리스트 */}
            <div className="flex gap-2 mb-4">
              {product.tags.map(tag => (
                <span key={tag} className="text-[9px] uppercase tracking-widest border border-wood/20 px-2 py-0.5">{tag}</span>
              ))}
            </div>
            <p className="text-[11px] uppercase tracking-[0.3em] text-wood/40 mb-2" style={{ fontFamily: "'Playfair Display', serif" }}>{product.brand}</p>
            <h3 className="text-3xl md:text-4xl font-light tracking-tight mb-4" style={{ fontFamily: "'Playfair Display', serif" }}>{product.name}</h3>
            <p className="text-xl font-light opacity-80">{product.price}</p>
          </div>

          {/* 감성 스토리 영역 */}
          <div className="mb-12">
            <h4 className="text-[10px] font-bold uppercase tracking-[0.2em] text-wood/30 mb-4 flex items-center gap-2">
              <Sparkles size={12} /> The Story
            </h4>
            <p className="text-[15px] leading-relaxed break-keep font-light italic text-wood/80">
              "{product.details.story}"
            </p>
          </div>

          {/* 노트 피라미드 영역 (Top, Mid, Base) */}
          <div className="space-y-6 mb-12">
            <h4 className="text-[10px] font-bold uppercase tracking-[0.2em] text-wood/30 mb-4 flex items-center gap-2">
              <Wind size={12} /> Scent Pyramid
            </h4>
            <div className="grid grid-cols-1 gap-4">
              <div className="flex items-start gap-4">
                <span className="text-[10px] uppercase tracking-widest text-wood/40 mt-1 w-12">Top</span>
                <p className="text-sm font-medium">{product.details.topNotes}</p>
              </div>
              <div className="flex items-start gap-4">
                <span className="text-[10px] uppercase tracking-widest text-wood/40 mt-1 w-12">Mid</span>
                <p className="text-sm font-medium">{product.details.middleNotes}</p>
              </div>
              <div className="flex items-start gap-4">
                <span className="text-[10px] uppercase tracking-widest text-wood/40 mt-1 w-12">Base</span>
                <p className="text-sm font-medium">{product.details.baseNotes}</p>
              </div>
            </div>
          </div>

          {/* 하단: 베스트 추천 상황 */}
          <div className="mt-auto pt-8 border-t border-wood/10">
            <div className="flex items-start gap-3 text-wood/60 italic text-[13px]">
              <MapPin size={16} className="mt-0.5 flex-shrink-0" />
              <p className="break-keep">{product.details.bestFor}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// EOF: ProductModal.tsx
