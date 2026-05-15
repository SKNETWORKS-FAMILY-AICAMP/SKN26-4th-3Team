/**
 * @file SafetyValuesSection.tsx
 * @description 브랜드가 지향하는 핵심 가치(안전성, 윤리성, 기능성)를 시각적으로 전달하는 섹션입니다.
 * 세 가지 핵심 가치를 아이콘과 상세 설명을 통해 그리드 레이아웃으로 구성합니다.
 */

import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { Shield, Leaf, Clock } from "lucide-react";
import { useState } from "react";

/**
 * 브랜드 가치 정의 데이터
 */
const values = [
  {
    icon: Shield,
    title: "IFRA 성분 가이드",
    description:
      "국제향료협회(IFRA) 기준을 참고한 성분 데이터로 알레르기 유발 가능 성분을 미리 확인할 수 있도록 안내합니다.",
    details: [
      "제품별 Ingredients 데이터 기준",
      "알레르기 유발 가능 성분 사전 확인",
      "제품 상세 정보와 함께 검토",
    ],
  },
  {
    icon: Leaf,
    title: "브랜드 윤리성 공개",
    description:
      "브랜드별 지속 가능성 정책과 크루얼티 프리 여부를 정리해 가치 소비 기준을 함께 비교할 수 있게 합니다.",
    details: [
      "브랜드별 윤리 데이터 기준",
      "지속 가능성 정책 여부 정리",
      "크루얼티 프리 정보 확인",
    ],
  },
  {
    icon: Clock,
    title: "아우라 매칭 알고리즘",
    description:
      "시각적 무드와 향기의 어코드를 연결해 당신의 스타일이 가장 돋보이는 향기를 제안합니다.",
    details: [
      "이미지 기반 시각 무드 분석",
      "5축 향기 아우라 스코어 계산",
      "향수 어코드와 사용자 무드 매칭",
    ],
  },
];

export default function SafetyValuesSection() {
  /** 뷰포트 진입 감지 */
  const { ref, isVisible } = useIntersectionObserver();
  const [activeValueIdx, setActiveValueIdx] = useState(0);

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
                <button
                  type="button"
                  onClick={() => setActiveValueIdx(i)}
                  aria-label={`${v.title} 확인 기준 보기`}
                  aria-pressed={activeValueIdx === i}
                  aria-expanded={activeValueIdx === i}
                  aria-controls={`trust-value-details-${i}`}
                  className={`w-10 h-10 flex items-center justify-center mb-6 mx-auto md:mx-0 rounded-full border transition-all duration-300 ${
                    activeValueIdx === i
                      ? "bg-cream text-wood border-cream shadow-[0_0_24px_rgba(253,252,240,0.16)]"
                      : "bg-cream/5 text-cream/60 border-cream/0 hover:bg-cream/10 hover:text-cream hover:border-cream/10"
                  }`}
                >
                  <v.icon size={20} strokeWidth={1.2} />
                </button>
                {/* 콘텐츠 영역 */}
                <h3 className="text-lg font-medium mb-4 tracking-tight">{v.title}</h3>
                <p className="text-[14px] leading-relaxed text-cream/50 break-keep">{v.description}</p>
                {activeValueIdx === i && (
                  <div
                    id={`trust-value-details-${i}`}
                    className="mt-6 border-t border-cream/10 pt-5 text-left animate-in fade-in slide-in-from-top-1 duration-300"
                  >
                    <p className="text-[10px] uppercase tracking-[0.24em] text-cream/30 mb-3">확인 기준</p>
                    <ul className="space-y-2">
                      {v.details.map((detail) => (
                        <li key={detail} className="flex items-start gap-2 text-[12px] leading-relaxed text-cream/60 break-keep">
                          <span className="mt-[0.55em] h-1 w-1 shrink-0 rounded-full bg-cream/35" />
                          <span>{detail}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

// EOF: SafetyValuesSection.tsx
