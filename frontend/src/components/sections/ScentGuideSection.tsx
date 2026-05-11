/**
 * @file ScentGuideSection.tsx
 * @description 향기에 대한 심도 있는 교육 정보와 가이드를 제공하는 섹션입니다.
 * 부향률 체계, 향기 계열(Family), 그리고 주요 향기 노트 사전을 유기적으로 배치합니다.
 */

import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import ConcentrationList from "@/components/guide/ConcentrationList";
import FamilyCarousel from "@/components/guide/FamilyCarousel";
import ScentNoteCarousel from "@/components/guide/ScentNoteCarousel";
import { scentFamilies, concentrations } from "@/data/scentData";

interface ScentGuideSectionProps {
  /** 사용자가 노트를 선택했을 때 상태를 부모 컴포넌트로 전달하는 콜백 */
  onNotesChange?: (notes: string[]) => void;
}

export default function ScentGuideSection({ onNotesChange }: ScentGuideSectionProps) {
  /** 뷰포트 진입 감지 */
  const { ref, isVisible } = useIntersectionObserver();

  return (
    <section id="guide" className="bg-beige py-24 md:py-40">
      <div className="max-w-[1440px] mx-auto px-6 md:px-8">
        <div ref={ref} className={`transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          
          {/* 도입부 헤더 영역 */}
          <div className="max-w-3xl mb-16 md:mb-20">
            <p className="label-upper text-wood/40 mb-4">Scent Education</p>
            <h2 className="text-2xl sm:text-4xl md:text-5xl font-light tracking-tight mb-6 md:mb-8 text-wood break-keep text-wood" style={{ fontFamily: "'Playfair Display', serif" }}>
              향기를 이해하는,&nbsp;<span className="hidden sm:inline"><br /></span>가장 쉬운 방법
            </h2>
            <p className="text-wood/60 leading-relaxed text-[15px] sm:text-lg break-keep max-w-3xl text-wood">
              복잡한 용어 대신 향기가 가진 고유의 성격에 집중해 보세요. <br className="hidden lg:inline" />
              당신의 분위기를 완성하는 마지막 퍼즐 조각을 찾는 과정입니다. <br className="hidden lg:inline" />
              개인의 스타일을 완성하는 향수학의 기초부터 심화까지 모든 향기를 아우릅니다.
            </p>
          </div>

          {/* 지식 가이드 그리드 영역 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-stretch mb-20">
            {/* 01. 부향률(Concentration) 가이드 */}
            <ConcentrationList concentrations={concentrations} />

            {/* 02. 향기 계열(Family) 가로 스크롤 가이드 */}
            <FamilyCarousel families={scentFamilies} />
          </div>

          {/* 03. 향기의 계층 (Note Carousel & Selection) */}
          <ScentNoteCarousel onNotesChange={onNotesChange} />
        </div>
      </div>
    </section>
  );
}

// EOF: ScentGuideSection.tsx
