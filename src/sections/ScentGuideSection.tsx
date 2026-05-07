/**
 * @file ScentGuideSection.tsx
 * @description 향기에 대한 종합적인 교육 정보를 제공하는 섹션입니다.
 * 부향률, 향기 계열, 그리고 주요 원료 사전을 포함합니다.
 */

import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import ConcentrationList from "@/components/guide/ConcentrationList";
import FamilyCarousel from "@/components/guide/FamilyCarousel";
import NoteGlossary from "@/components/guide/NoteGlossary";
import { scentFamilies, concentrations } from "@/data/scentData";

export default function ScentGuideSection({ onNotesChange }: { onNotesChange?: (notes: string[]) => void }) {
  const { ref, isVisible } = useIntersectionObserver();

  return (
    <section id="guide" className="bg-beige py-24 md:py-40">
      <div className="max-w-[1440px] mx-auto px-6 md:px-8">
        <div ref={ref} className={`transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          
          {/* 섹션 헤더 */}
          <div className="max-w-3xl mb-16 md:mb-20">
            <p className="label-upper text-wood/40 mb-4">Scent Education</p>
            <h2 className="text-2xl sm:text-4xl md:text-5xl font-light tracking-tight mb-6 md:mb-8 text-wood break-keep text-wood">
              향기를 이해하는,&nbsp;<span className="hidden sm:inline"><br /></span>가장 쉬운 방법
            </h2>
            <p className="text-wood/60 leading-relaxed text-[15px] sm:text-lg break-keep max-w-3xl text-wood">
              복잡한 용어 대신 향기가 가진 고유의 성격에 집중해 보세요. <br className="hidden lg:inline" />
              당신의 분위기를 완성하는 마지막 퍼즐 조각을 찾는 과정입니다. <br className="hidden lg:inline" />
              개인의 스타일을 완성하는 향수학의 기초부터 심화까지 모든 향기를 아우릅니다.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-stretch">
            {/* 01. 부향률 가이드 영역 */}
            <ConcentrationList concentrations={concentrations} />

            {/* 02. 향기 계열 심층 가이드 영역 */}
            <FamilyCarousel families={scentFamilies} />
          </div>

          {/* 03. 향기 원료 사전 (Note Glossary) */}
          <NoteGlossary onNotesChange={onNotesChange} />
        </div>
      </div>
    </section>
  );
}
