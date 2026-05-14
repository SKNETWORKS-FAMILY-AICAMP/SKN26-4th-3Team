/**
 * @file SafetyValuesSection.tsx
 * @description 브랜드가 지향하는 핵심 가치(안전성, 윤리성, 기능성)를 시각적으로 전달하는 섹션입니다.
 * 세 가지 핵심 가치를 아이콘과 상세 설명을 통해 그리드 레이아웃으로 구성합니다.
 */

import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { Shield, Leaf, Clock } from "lucide-react";

/**
 * 브랜드 가치 정의 데이터
 */
const values = [
  {
    icon: Shield,
    title: "알레르기 안전성",
    description:
      "성분별 알레르기 유발 물질 데이터베이스와 교차 분석해 사용자의 건강 정보를 반영한 안전한 추천을 제공합니다.",
  },
  {
    icon: Leaf,
    title: "비건 & 에코 인증",
    description:
      "동물성 원료 제외 및 지속가능성 인증을 받은 브랜드만을 선별하여 가치 소비를 지원합니다.",
  },
  {
    icon: Clock,
    title: "TPO 기반 스타일링",
    description:
      "사용자의 일상과 상황(Time, Context, Occasion)을 고려하여 현재의 무드에 최적화된 향기 스타일을 제안합니다.",
  },
];

export default function SafetyValuesSection() {
  /** 뷰포트 진입 감지 */
  const { ref, isVisible } = useIntersectionObserver();

  return (
    <section id="safety" className="bg-wood text-cream py-24 md:py-40">
      <div className="max-w-[1440px] mx-auto px-6 md:px-8">
        <div ref={ref} className={`transition-all duration-800 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          
          <div className="text-center mb-16">
            <p className="label-upper text-cream/40 mb-4">Trust & Values</p>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-light tracking-tight" style={{ fontFamily: "'Playfair Display', serif" }}>
              믿을 수 있는 기준
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-16 md:gap-8 lg:gap-16">
            {values.map((v, i) => (
              <div
                key={v.title}
                className="text-center md:text-left group"
                style={{
                  opacity: isVisible ? 1 : 0,
                  transform: isVisible ? "translateY(0)" : "translateY(20px)",
                  transition: `all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${i * 100 + 200}ms`,
                }}
              >
                {/* 상징 아이콘 */}
                <div className="w-10 h-10 flex items-center justify-center mb-6 mx-auto md:mx-0 bg-cream/5 rounded-full">
                  <v.icon size={20} strokeWidth={1.2} className="text-cream/60 group-hover:text-cream transition-colors duration-400" />
                </div>
                {/* 콘텐츠 영역 */}
                <h3 className="text-lg font-medium mb-4 tracking-tight">{v.title}</h3>
                <p className="text-[14px] leading-relaxed text-cream/50 break-keep">{v.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

// EOF: SafetyValuesSection.tsx
