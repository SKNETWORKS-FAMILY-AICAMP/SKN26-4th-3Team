/**
 * @file HeroSection.tsx
 * @description 사이트의 첫 인상을 결정하는 메인 히어로 섹션입니다.
 * 고해상도 배경 이미지, 브랜드 로고 애니메이션, 그리고 사용자의 여정을 시작하게 하는 CTA(Call to Action) 요소를 배치합니다.
 */

import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { ArrowRight } from "lucide-react";
import OlfitLogo from "@/components/common/OlfitLogo";

export default function HeroSection() {
  /** 뷰포트 진입 감지를 통한 애니메이션 트리거 (threshold 0.1) */
  const { ref, isVisible } = useIntersectionObserver({ threshold: 0.1 });

  return (
    <section 
      ref={ref}
      className="relative h-screen min-h-[600px] w-full overflow-hidden bg-wood"
    >
      {/* 배경 레이어: 대형 이미지와 시네마틱 오버레이 그라데이션 */}
      <div className="absolute inset-0 z-0 scale-110">
        <img
          src="/hero_bg.jpg"
          alt="Luxury Perfume Background"
          className={`w-full h-full object-cover transition-transform duration-[3000ms] ease-out ${
            isVisible ? "scale-100 opacity-60" : "scale-110 opacity-40"
          }`}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-wood/40 via-transparent to-wood/60" />
      </div>

      {/* 햇빛 레이어 1: 상단 중앙 메인 광원 (웜 앰버) */}
      <div
        className="absolute inset-0 z-[1] pointer-events-none animate-sunray-1"
        style={{
          background: "radial-gradient(ellipse 55% 40% at 52% 28%, rgba(210,170,100,0.55) 0%, rgba(180,130,70,0.15) 45%, transparent 70%)",
          mixBlendMode: "screen",
        }}
      />

      {/* 햇빛 레이어 2: 우측 상단 골드 하이라이트 */}
      <div
        className="absolute inset-0 z-[1] pointer-events-none animate-sunray-2"
        style={{
          background: "radial-gradient(ellipse 40% 35% at 72% 18%, rgba(240,200,130,0.40) 0%, rgba(200,155,80,0.10) 50%, transparent 72%)",
          mixBlendMode: "screen",
        }}
      />

      {/* 햇빛 레이어 3: 좌측 중앙 딥 앰버 깊이감 */}
      <div
        className="absolute inset-0 z-[1] pointer-events-none animate-sunray-3"
        style={{
          background: "radial-gradient(ellipse 35% 45% at 28% 35%, rgba(190,140,80,0.30) 0%, rgba(160,110,55,0.08) 55%, transparent 75%)",
          mixBlendMode: "screen",
        }}
      />

      {/* 중앙 콘텐츠: 메인 로고 및 슬로건 */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center z-10 px-6">
        <div 
          className={`transition-all duration-1000 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <OlfitLogo 
            width="auto" 
            height="clamp(60px, 15vw, 120px)" 
            color="#FDFCF0" 
          />
        </div>
        <p 
          className={`text-cream/60 text-[10px] sm:text-sm md:text-base tracking-[0.2em] sm:tracking-[0.3em] uppercase mt-8 transition-all duration-1000 delay-300 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          }`}
        >
          Your Style Translated into Scent
        </p>
      </div>

      {/* 플로팅 CTA 카드: 원료 선택 가이드로 이동 */}
      <a
        href="#guide"
        className="absolute bottom-6 right-6 md:bottom-8 md:right-8 group z-20"
      >
        <div className="bg-wood/40 backdrop-blur-md p-4 md:p-5 w-[calc(100vw-48px)] sm:w-[300px] md:w-[340px] max-w-[340px] border border-cream/10 shadow-2xl hover:shadow-editorial transition-all duration-400 hover:-translate-y-1">
          <div className="flex gap-3 sm:gap-4">
            {/* 카드 내 시각적 썸네일 */}
            <div className="w-12 h-12 sm:w-16 sm:h-16 md:w-20 md:h-20 bg-cream/10 flex-shrink-0 overflow-hidden">
              <img
                src="https://www.byredo.com/cdn-cgi/image/width=auto,height=1200,fit=scale-down,gravity=auto,format=webp,quality=70/https://www.byredo.com/media/catalog/product/cache/74c1057f7991b4edb2bc7bdaa94de933/8/0/806014_1_full_no.jpg"
                alt="Scent Exploration"
                className="w-full h-full object-cover mix-blend-lighten opacity-90"
              />
            </div>
            {/* 텍스트 영역 */}
            <div className="flex flex-col justify-between py-0.5">
              <div>
                <p className="text-[9px] sm:text-[10px] font-medium uppercase tracking-widest text-cream/60 mb-1">
                  Ingredient Discovery
                </p>
                <p className="text-[13px] sm:text-sm font-medium leading-snug text-cream break-keep">
                  취향에 맞는 3가지 원료를 선택해 <br className="hidden sm:inline" /> 
                  당신의 향을 발견하세요
                </p>
              </div>
              <div className="flex items-center gap-2 text-[10px] uppercase tracking-widest text-cream/80 mt-2 group-hover:text-cream transition-colors">
                <span>Explore Ingredients</span>
                <ArrowRight size={12} className="group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </div>
        </div>
      </a>

      {/* 하단 스크롤 유도 애니메이션 지표 */}
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 z-10">
        <span className="text-[9px] uppercase tracking-[0.3em] text-cream/40">Scroll</span>
        <div className="w-px h-10 bg-cream/30 overflow-hidden">
          <div className="w-full h-full bg-cream origin-top animate-pulse-line" />
        </div>
      </div>
    </section>
  );
}

// EOF: HeroSection.tsx
