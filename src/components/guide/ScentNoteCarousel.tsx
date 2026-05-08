/**
 * @file ScentNoteCarousel.tsx
 * @description 향기의 계층(Top, Middle, Base)을 탐색하는 인터랙티브 캐러셀 컴포넌트입니다.
 * 탭 전환, 무한 루프 캐러셀, 10초 주기 자동 재생 및 타이머 초기화 로직을 포함합니다.
 */

import { useState, useEffect, useCallback } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

// 임시 데이터 정의 (Olfit 무드에 맞춰 일부 수정 가능)
const notesData = {
  Top: ['시트러스', '베르가못', '레몬', '오렌지', '자몽', '만다린', '네롤리', '유자'],
  Middle: ['자스민', '로즈', '일랑일랑', '뮤겟', '라벤더', '제라늄', '오키드', '프리지아'],
  Base: ['머스크', '샌달우드', '바닐라', '앰버', '시더우드', '패출리', '오크모스', '베티버'],
};

type NoteType = keyof typeof notesData;

export default function ScentNoteCarousel() {
  const [activeTab, setActiveTab] = useState<NoteType>('Top');
  const [currentIndex, setCurrentIndex] = useState(0);

  const currentNotes = notesData[activeTab];
  const totalNotes = currentNotes.length;

  const handleNext = useCallback(() => {
    setCurrentIndex((prev) => (prev + 1) % totalNotes);
  }, [totalNotes]);

  const handlePrev = useCallback(() => {
    setCurrentIndex((prev) => (prev - 1 + totalNotes) % totalNotes);
  }, [totalNotes]);

  const handleTabChange = (tab: NoteType) => {
    setActiveTab(tab);
    setCurrentIndex(0);
  };

  const handleDotClick = (index: number) => {
    setCurrentIndex(index);
  };

  useEffect(() => {
    const timer = setInterval(() => {
      handleNext();
    }, 10000);

    return () => clearInterval(timer);
  }, [activeTab, currentIndex, handleNext]);

  return (
    <div className="w-full bg-cream/30 rounded-sm border border-wood/5 p-8 md:p-12 flex flex-col items-center mt-12">
      {/* 1. 상단 탭 */}
      <div className="flex gap-6 md:gap-8 mb-12 w-full justify-center">
        {(['Top', 'Middle', 'Base'] as NoteType[]).map((tab) => (
          <button
            key={tab}
            onClick={() => handleTabChange(tab)}
            className={`relative pb-2 text-[11px] md:text-[12px] font-bold uppercase tracking-[0.2em] transition-all duration-300 ${
              activeTab === tab ? 'text-wood' : 'text-wood/30 hover:text-wood/50'
            }`}
          >
            {tab} Note
            {activeTab === tab && (
              <div className="absolute bottom-0 left-0 right-0 h-px bg-wood" />
            )}
          </button>
        ))}
      </div>

      {/* 2. 캐러셀 메인 영역 */}
      <div className="relative w-full flex flex-col items-center">
        <div className="text-[10px] tracking-[0.3em] text-wood/30 uppercase mb-6 font-mono">
          {currentIndex + 1} / {totalNotes}
        </div>

        <div className="flex items-center justify-between w-full max-w-sm">
          <button
            onClick={handlePrev}
            className="p-2 text-wood/30 hover:text-wood transition-colors"
            aria-label="Previous note"
          >
            <ChevronLeft size={20} strokeWidth={1.5} />
          </button>

          <div 
            key={`${activeTab}-${currentIndex}`}
            className="flex-1 text-center animate-in fade-in duration-1000 ease-out"
          >
            <h3 className="text-2xl md:text-3xl font-light tracking-tight text-wood" style={{ fontFamily: "'Playfair Display', serif" }}>
              {currentNotes[currentIndex]}
            </h3>
          </div>

          <button
            onClick={handleNext}
            className="p-2 text-wood/30 hover:text-wood transition-colors"
            aria-label="Next note"
          >
            <ChevronRight size={20} strokeWidth={1.5} />
          </button>
        </div>
      </div>

      {/* 3. 하단 점 인디케이터 */}
      <div className="flex gap-2 mt-12">
        {currentNotes.map((_, idx) => (
          <button
            key={idx}
            onClick={() => handleDotClick(idx)}
            className={`h-1 rounded-full transition-all duration-500 ease-in-out ${
              currentIndex === idx 
                ? 'w-6 bg-wood' 
                : 'w-1.5 bg-wood/10 hover:bg-wood/20'
            }`}
            aria-label={`Go to slide ${idx + 1}`}
          />
        ))}
      </div>

      <p className="mt-10 text-[9px] text-wood/20 tracking-[0.3em] uppercase italic">
        Olfit Scent Layering Guide
      </p>
    </div>
  );
}

// EOF: ScentNoteCarousel.tsx
