/**
 * @file FamilyCarousel.tsx
 * @description 향기의 계열(Floral, Woody 등)을 상세히 설명하는 인터랙티브 캐러셀 컴포넌트입니다.
 * 10초 주기 자동 전환 및 인디케이터를 통한 수동 제어를 지원하며, 계열별 특징과 주요 노트를 소개합니다.
 */

import { useState, useEffect } from "react";
import type { LucideIcon } from "lucide-react";

interface Family {
  title: string;
  subtitle: string;
  description: string;
  icon: LucideIcon;
  color: string;
  details: { name: string; desc: string }[];
}

interface FamilyCarouselProps {
  /** 캐러셀에 노출할 향기 계열 데이터 리스트 */
  families: Family[];
}

export default function FamilyCarousel({ families }: FamilyCarouselProps) {
  /** 현재 활성화된 패밀리 인덱스 */
  const [activeFamilyIdx, setActiveFamilyIdx] = useState(0);

  /**
   * 10초마다 다음 슬라이드로 자동 전환하는 루프 설정
   */
  useEffect(() => {
    const timer = setInterval(() => {
      setActiveFamilyIdx((prev) => (prev + 1) % families.length);
    }, 10000);
    return () => clearInterval(timer);
  }, [families.length]);

  return (
    <div className="flex flex-col h-full">
      {/* 상단 컨트롤 영역: 타이틀 (인디케이터는 하단으로 이동) */}
      <div className="flex justify-between items-center mb-8 md:mb-10">
        <h3 className="text-[11px] md:text-[12px] font-bold uppercase tracking-[0.2em] text-wood/30">
          02. Scent Family (계열의 차이)
        </h3>
      </div>

      {/* 메인 슬라이드 영역 */}
      <div className="relative overflow-hidden flex-1 h-[440px] sm:h-[480px] lg:h-auto min-h-[440px]">
        {families.map((f, idx) => (
          <div 
            key={f.title} 
            className={`absolute inset-0 transition-all duration-1000 ease-[cubic-bezier(0.23,1,0.32,1)] ${
              idx === activeFamilyIdx 
                ? 'opacity-100 translate-x-0' 
                : idx < activeFamilyIdx 
                  ? 'opacity-0 -translate-x-10' 
                  : 'opacity-0 translate-x-10'
            }`}
          >
            <div className={`${f.color} p-6 sm:p-8 md:p-12 h-full rounded-sm border border-wood/5 flex flex-col text-wood`}>
              {/* 계열 헤더: 아이콘 및 타이틀 */}
              <div className="flex items-center gap-3 md:gap-4 mb-6">
                <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-wood/5 flex items-center justify-center">
                  <f.icon size={22} strokeWidth={1.2} />
                </div>
                <div>
                  <h4 className="text-xl md:text-2xl font-light tracking-tight">{f.title}</h4>
                  <p className="text-[9px] md:text-[11px] text-wood/40 uppercase tracking-[0.2em]">{f.subtitle}</p>
                </div>
              </div>

              {/* 본문 설명 */}
              <p className="text-[13.5px] sm:text-[16px] leading-[1.7] md:leading-[1.8] text-wood/70 mb-8 md:mb-12 font-light break-keep tracking-tight text-left">
                {f.description}
              </p>              
              {/* 하단 성분 상세 목록 */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 md:gap-10 pt-6 md:pt-10 border-t border-wood/10 mt-auto">
                {f.details.map((d) => (
                  <div key={d.name}>
                    <p className="text-[12px] md:text-[14px] font-semibold mb-1 md:mb-2 tracking-wide uppercase text-wood/80">{d.name}</p>
                    <div className="text-[12px] md:text-[13px] leading-relaxed text-wood/60 break-keep">
                      {d.desc}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* 하단 점 인디케이터 (수정된 위치 및 스타일) */}
      <div className="flex justify-center gap-2 mt-8">
        {families.map((_, i) => (
          <button 
            key={i}
            onClick={() => setActiveFamilyIdx(i)}
            aria-label={`${families[i].title} 계열 보기`}
            className={`h-1 rounded-full transition-all duration-500 ease-in-out ${
              activeFamilyIdx === i 
                ? 'w-6 bg-wood' 
                : 'w-1.5 bg-wood/10 hover:bg-wood/20'
            }`}
          />
        ))}
      </div>

      <p className="text-[9px] md:text-[10px] text-wood/30 mt-6 text-center italic uppercase tracking-widest">Automatic rotation every 10 seconds</p>
    </div>
  );
}

// EOF: FamilyCarousel.tsx
