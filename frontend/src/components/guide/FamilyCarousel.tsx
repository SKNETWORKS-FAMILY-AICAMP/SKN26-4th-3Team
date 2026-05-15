/**
 * @file FamilyCarousel.tsx
 * @description 향기의 계열(Floral, Woody 등)을 상세히 설명하는 인터랙티브 캐러셀 컴포넌트입니다.
 * 30초 주기 자동 전환 및 인디케이터/버튼을 통한 수동 제어를 지원하며, 계열별 특징과 주요 노트를 소개합니다.
 */

import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight, type LucideIcon } from "lucide-react";

interface Family {
  title: string;
  subtitle: string;
  description: string;
  keyNotes?: string[];
  icon: LucideIcon;
  color: string;
  details: { name: string; desc: string }[];
}

interface FamilyCarouselProps {
  /** 캐러셀에 노출할 향기 계열 데이터 리스트 */
  families: Family[];
}

const ROTATION_DELAY_MS = 30000;

export default function FamilyCarousel({ families }: FamilyCarouselProps) {
  /** 현재 활성화된 패밀리 인덱스 */
  const [activeFamilyIdx, setActiveFamilyIdx] = useState(0);
  const [manualResetKey, setManualResetKey] = useState(0);
  const hasMultipleFamilies = families.length > 1;

  /**
   * 다음 자동 전환을 예약합니다.
   * 활성 슬라이드가 바뀌거나 사용자가 수동 조작할 때마다 기존 예약이 취소되어
   * 수동 전환 직후 곧바로 한 번 더 넘어가는 현상을 막습니다.
   */
  useEffect(() => {
    if (!hasMultipleFamilies) return;

    const timer = window.setTimeout(() => {
      setActiveFamilyIdx((prev) => (prev + 1) % families.length);
    }, ROTATION_DELAY_MS);

    return () => clearTimeout(timer);
  }, [activeFamilyIdx, families.length, hasMultipleFamilies, manualResetKey]);

  const handleManualChange = (index: number) => {
    if (families.length === 0) return;
    setActiveFamilyIdx((index + families.length) % families.length);
    setManualResetKey((key) => key + 1);
  };

  const handlePrev = () => {
    handleManualChange(activeFamilyIdx - 1);
  };

  const handleNext = () => {
    handleManualChange(activeFamilyIdx + 1);
  };

  return (
    <div className="flex flex-col h-full">
      {/* 상단 컨트롤 영역: 타이틀 (인디케이터는 하단으로 이동) */}
      <div className="flex flex-col mb-8 md:mb-10">
        <h3 className="text-[11px] md:text-[12px] font-bold uppercase tracking-[0.2em] text-wood/30 mb-4">
          02. Scent Family (계열의 차이)
        </h3>
        <p 
          className="text-[14px] md:text-[15px] text-wood/60 leading-relaxed break-keep min-h-[3rem] md:min-h-[4.5rem]"
          dangerouslySetInnerHTML={{ __html: "향기 계열은 향수의 성격과 분위기를 결정하는 가장 큰 기준입니다. <br className='hidden sm:inline' /> 비슷한 성질을 가진 향료를 그룹화하여, 향의 지도를 그리는 첫걸음이 됩니다." }}
        />
      </div>

      {/* 메인 슬라이드 영역 */}
      <div className="relative group overflow-hidden flex-1 h-[540px] sm:h-[580px] lg:h-[620px] min-h-[540px]">
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
                  <p className="text-[9px] md:text-[11px] text-wood/70 uppercase tracking-[0.2em]">{f.subtitle}</p>
                </div>
              </div>

              {/* 본문 설명 */}
              <p 
                className="text-[13.5px] sm:text-[16px] leading-[1.7] md:leading-[1.8] text-wood mb-6 md:mb-8 font-light break-keep tracking-tight text-left"
                dangerouslySetInnerHTML={{ __html: f.description }}
              />

              {/* 대표 노트 태그 리스트 */}
              {f.keyNotes && (
                <div className="flex flex-wrap gap-2 mb-8 md:mb-12">
                  {f.keyNotes.map((note) => (
                    <span key={note} className="px-3 py-1 bg-wood/5 rounded-full text-[11px] md:text-[12px] font-medium text-wood/60 border border-wood/10">
                      #{note}
                    </span>
                  ))}
                </div>
              )}

              {/* 하단 성분 상세 목록 */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 md:gap-10 pt-6 md:pt-10 border-t border-wood/10 mt-auto">
                {f.details.map((d) => (
                  <div key={d.name}>
                    <p className="text-[12px] md:text-[14px] font-semibold mb-1 md:mb-2 tracking-wide uppercase text-wood">{d.name}</p>
                    <div className="text-[12px] md:text-[13px] leading-relaxed text-wood/90 break-keep">
                      {d.desc}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}

        {hasMultipleFamilies && (
          <>
            <button
              type="button"
              onClick={handlePrev}
              aria-label="이전 향기 계열 보기"
              className="absolute left-4 top-1/2 -translate-y-1/2 z-10 w-10 h-10 md:w-11 md:h-11 inline-flex items-center justify-center rounded-full bg-cream/85 text-wood border border-wood/10 shadow-sm opacity-0 group-hover:opacity-100 focus-visible:opacity-100 transition-all duration-300 hover:bg-white hover:scale-105"
            >
              <ChevronLeft size={20} strokeWidth={1.5} />
            </button>
            <button
              type="button"
              onClick={handleNext}
              aria-label="다음 향기 계열 보기"
              className="absolute right-4 top-1/2 -translate-y-1/2 z-10 w-10 h-10 md:w-11 md:h-11 inline-flex items-center justify-center rounded-full bg-cream/85 text-wood border border-wood/10 shadow-sm opacity-0 group-hover:opacity-100 focus-visible:opacity-100 transition-all duration-300 hover:bg-white hover:scale-105"
            >
              <ChevronRight size={20} strokeWidth={1.5} />
            </button>
          </>
        )}
      </div>
      
      {/* 하단 점 인디케이터 (수정된 위치 및 스타일) */}
      <div className="flex justify-center gap-2 mt-8">
        {families.map((_, i) => (
          <button 
            key={i}
            type="button"
            onClick={() => handleManualChange(i)}
            aria-label={`${families[i].title} 계열 보기`}
            className={`h-1 rounded-full transition-all duration-500 ease-in-out ${
              activeFamilyIdx === i 
                ? 'w-6 bg-wood' 
                : 'w-1.5 bg-wood/10 hover:bg-wood/20'
            }`}
          />
        ))}
      </div>

      <p className="text-[9px] md:text-[10px] text-wood/30 mt-6 text-center italic uppercase tracking-widest">Automatic rotation every 30 seconds</p>
    </div>
  );
}

// EOF: FamilyCarousel.tsx
