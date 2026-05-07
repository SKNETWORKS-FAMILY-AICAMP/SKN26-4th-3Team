/**
 * @file HeroSection.tsx
 * @description 사이트의 첫 인상을 결정하는 메인 히어로 섹션입니다.
 * 배경 이미지, 중앙 로고 애니메이션, 그리고 AI 인터뷰로 유도하는 플로팅 카드를 포함합니다.
 */

import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { ArrowRight } from "lucide-react";

export default function HeroSection() {
  // 섹션이 화면에 나타나는지 감지 (페이드인 애니메이션용)
  const { ref, isVisible } = useIntersectionObserver({ threshold: 0.1 });

  return (
    <section 
      ref={ref}
      className="relative h-screen min-h-[600px] w-full overflow-hidden bg-wood"
    >
      {/* 배경 레이어: 이미지 + 어두운 오버레이 */}
      <div className="absolute inset-0 z-0 scale-110">
        <img
          src="/hero_bg.jpg"
          alt="Luxury Perfume Background"
          className={`w-full h-full object-cover transition-transform duration-[3000ms] ease-out ${
            isVisible ? "scale-100 opacity-60" : "scale-110 opacity-40" // 등장 시 서서히 줌아웃 효과
          }`}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-wood/40 via-transparent to-wood/60" />
      </div>

      {/* 중앙 로고 및 서브타이틀 영역 */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center z-10 px-6">
        <div className="overflow-hidden mb-2">
          <h1 
            className={`text-4xl sm:text-6xl md:text-7xl lg:text-8xl font-light tracking-[0.2em] uppercase text-cream transition-all duration-1000 ${
              isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            }`}
          >
            Olfit
          </h1>
        </div>
        <p 
          className={`text-cream/60 text-[10px] sm:text-sm md:text-base tracking-[0.2em] sm:tracking-[0.3em] uppercase mt-4 transition-all duration-1000 delay-300 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          }`}
        >
          Your Style Translated into Scent
        </p>
      </div>

      {/* 우측 하단 플로팅 액션 카드 (CTA: Call to Action) */}
      <a
        href="#guide"
        className="absolute bottom-6 right-6 md:bottom-8 md:right-8 group z-20"
      >
        <div className="bg-wood/40 backdrop-blur-md p-4 md:p-5 w-[calc(100vw-48px)] sm:w-[300px] md:w-[340px] max-w-[340px] border border-cream/10 shadow-2xl hover:shadow-editorial transition-all duration-400 hover:-translate-y-1">
          <div className="flex gap-3 sm:gap-4">
            {/* 카드 내 썸네일 이미지 */}
            <div className="w-12 h-12 sm:w-16 sm:h-16 md:w-20 md:h-20 bg-cream/10 flex-shrink-0 overflow-hidden">
              <img
                src="/product_1.jpg"
                alt="Scent Exploration"
                className="w-full h-full object-cover mix-blend-lighten opacity-90"
              />
            </div>
            {/* 카드 텍스트 콘텐츠 */}
            <div className="flex flex-col justify-between py-0.5">
              <div>
                <p className="text-[9px] sm:text-[10px] font-medium uppercase tracking-widest text-cream/60 mb-1">
                  Ingredient Discovery
                </p>
                <p className="text-[13px] sm:text-sm font-medium leading-snug text-cream break-keep">
                  취향에 맞는 3가지 원료를 선택해 <br className="hidden sm:inline" /> 
                  당신만의 시그니처 향을 발견하세요
                </p>
              </div>
              {/* 시작하기 링크 버튼 */}
              <div className="flex items-center gap-2 text-[10px] uppercase tracking-widest text-cream/80 mt-2 group-hover:text-cream transition-colors">
                <span>Explore Ingredients</span>
                <ArrowRight size={12} className="group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </div>
        </div>
      </a>

      {/* 하단 스크롤 유도 애니메이션 */}
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 z-10">
        <span className="text-[9px] uppercase tracking-[0.3em] text-cream/40">Scroll</span>
        <div className="w-px h-10 bg-cream/30 overflow-hidden">
          {/* 애니메이션 라인 */}
          <div className="w-full h-full bg-cream origin-top animate-pulse-line" />
        </div>
      </div>
    </section>
  );
}
