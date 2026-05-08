/**
 * @file ScentNoteCarousel.tsx
 * @description 향기의 계층(Top, Middle, Base)별로 하나의 원료를 선택하여 조화로운 향의 피라미드를 시각적으로 완성하는 캐러셀입니다.
 * SVG 피라미드 UI, 카테고리별 교체 로직, 10초 주기 자동 재생 기능을 포함합니다.
 */

import { useState, useEffect, useCallback } from 'react';
import { ChevronLeft, ChevronRight, Check, RefreshCw, Info } from 'lucide-react';
import { scentNotes } from "@/data/noteData";
import type { ScentNote } from "@/data/noteData";

interface ScentNoteCarouselProps {
  /** 선택된 노드들이 변경될 때 부모 컴포넌트로 전달하는 콜백 */
  onNotesChange?: (notes: string[]) => void;
}

export default function ScentNoteCarousel({ onNotesChange }: ScentNoteCarouselProps) {
  const [activeTab, setActiveTab] = useState<"Top" | "Middle" | "Base">('Top');
  const [currentIndex, setCurrentIndex] = useState(0);
  
  /** 
   * 슬롯 기반 선택 상태 관리 
   */
  const [slots, setSlots] = useState<Record<string, ScentNote | null>>({
    Top: null,
    Middle: null,
    Base: null
  });

  const currentNotes = scentNotes.filter(n => n.category === activeTab);
  const totalNotes = currentNotes.length;
  const currentNote = currentNotes[currentIndex];

  const handleNext = useCallback(() => {
    setCurrentIndex((prev) => (prev + 1) % totalNotes);
  }, [totalNotes]);

  const handlePrev = useCallback(() => {
    setCurrentIndex((prev) => (prev - 1 + totalNotes) % totalNotes);
  }, [totalNotes]);

  const handleTabChange = (tab: "Top" | "Middle" | "Base") => {
    setActiveTab(tab);
    setCurrentIndex(0);
  };

  const handleDotClick = (index: number) => {
    setCurrentIndex(index);
  };

  /**
   * 노트를 피라미드 슬롯에 담거나 교체하는 핸들러
   */
  const toggleNote = (note: ScentNote) => {
    setSlots(prev => {
      const isAlreadySelected = prev[note.category]?.enName === note.enName;
      const newSlots = {
        ...prev,
        [note.category]: isAlreadySelected ? null : note
      };

      if (onNotesChange) {
        const selectedNames = Object.values(newSlots)
          .filter((n): n is ScentNote => n !== null)
          .map(n => n.name);
        onNotesChange(selectedNames);
      }
      
      return newSlots;
    });
  };

  const resetNotes = () => {
    const emptySlots = { Top: null, Middle: null, Base: null };
    setSlots(emptySlots);
    if (onNotesChange) onNotesChange([]);
  };

  useEffect(() => {
    const timer = setInterval(() => {
      handleNext();
    }, 10000);

    return () => clearInterval(timer);
  }, [activeTab, currentIndex, handleNext]);

  const isSelected = slots[activeTab]?.enName === currentNote?.enName;
  const isAllSelected = slots.Top && slots.Middle && slots.Base;

  return (
    <div className="w-full bg-cream/30 rounded-sm border border-wood/5 p-8 md:p-16 flex flex-col items-center mt-12 relative overflow-hidden">
      {/* 배경 장식 (모든 슬롯이 채워졌을 때 우아한 광채 효과) */}
      <div className={`absolute inset-0 bg-wood/[0.03] transition-opacity duration-[2000ms] ${isAllSelected ? 'opacity-100' : 'opacity-0'}`} />

      {/* 상단 섹션: 텍스트 가이드와 비주얼 피라미드 */}
      <div className="relative z-10 w-full flex flex-col lg:flex-row items-center justify-between mb-20 gap-12 lg:gap-24">
        
        {/* 가이드 텍스트 */}
        <div className="text-center lg:text-left max-w-sm order-2 lg:order-1">
          <h3 className="text-[11px] md:text-[12px] font-bold uppercase tracking-[0.2em] text-wood/30 mb-4">
            03. Scent Pyramid (향의 구조 설계)
          </h3>
          <p className="text-[13px] md:text-[14px] text-wood/60 leading-relaxed break-keep mb-8 font-light">
            {isAllSelected 
              ? "완벽한 향의 삼각형이 완성되었습니다. 당신의 감각이 조화롭게 정렬되었습니다. 이제 아래 분석 버튼을 눌러 당신만의 향수를 찾아보세요." 
              : "탑, 미들, 베이스 노트에서 각각 가장 마음에 드는 원료를 하나씩 골라 조화를 완성하세요. 완성된 피라미드는 당신의 페르소나와 결합됩니다."}
          </p>
          <div className="flex flex-col sm:flex-row items-center gap-6">
            <button 
              onClick={resetNotes}
              className="flex items-center gap-2 text-[10px] uppercase tracking-[0.2em] text-wood/30 hover:text-wood transition-colors group"
            >
              <RefreshCw size={12} className="group-hover:rotate-180 transition-transform duration-700" />
              Reset Pyramid
            </button>
            {isAllSelected && (
              <div className="flex items-center gap-2 text-emerald-700/60 text-[10px] uppercase tracking-widest animate-pulse font-medium">
                <Check size={12} />
                Pyramid Complete
              </div>
            )}
          </div>
        </div>

        {/* 비주얼 피라미드 슬롯 */}
        <div className="relative w-72 h-64 md:w-80 md:h-72 flex flex-col items-center order-1 lg:order-2 group">
          {/* 피라미드 가이드 라인 (SVG) */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none drop-shadow-sm" viewBox="0 0 100 90">
            <path 
              d="M50 5 L95 85 L5 85 Z" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="0.3" 
              className="text-wood/20"
            />
            {/* 수평 분할선 */}
            <line x1="33" y1="31.5" x2="67" y2="31.5" stroke="currentColor" strokeWidth="0.2" className="text-wood/10" />
            <line x1="16.5" y1="58.5" x2="83.5" y2="58.5" stroke="currentColor" strokeWidth="0.2" className="text-wood/10" />
          </svg>

          {/* 슬롯 레이어들 */}
          <div className="w-full h-full flex flex-col items-center py-1">
            
            {/* TOP SLOT */}
            <div 
              onClick={() => handleTabChange('Top')}
              className={`relative z-10 w-1/3 h-[30%] flex flex-col items-center justify-end pb-3 cursor-pointer transition-all duration-700 ${
                slots.Top ? 'text-wood' : 'text-wood/20'
              } ${activeTab === 'Top' ? 'scale-110' : 'hover:scale-105'}`}
            >
              <div className={`absolute inset-x-0 bottom-0 h-full transition-all duration-1000 ${slots.Top ? 'bg-wood/10 opacity-100 shadow-[0_0_20px_rgba(var(--wood-rgb),0.05)]' : 'opacity-0'}`} 
                   style={{ clipPath: 'polygon(50% 0%, 100% 100%, 0% 100%)' }} />
              <span className="text-[7px] uppercase tracking-[0.2em] mb-1 font-bold">Top</span>
              <span className="text-[10px] md:text-[11px] font-medium tracking-tight truncate max-w-[60px] text-center">
                {slots.Top ? slots.Top.name : "Select"}
              </span>
            </div>

            {/* MIDDLE SLOT */}
            <div 
              onClick={() => handleTabChange('Middle')}
              className={`relative z-10 w-2/3 h-[30%] flex flex-col items-center justify-center cursor-pointer transition-all duration-700 ${
                slots.Middle ? 'text-wood' : 'text-wood/20'
              } ${activeTab === 'Middle' ? 'scale-110' : 'hover:scale-105'}`}
            >
              <div className={`absolute inset-x-0 bottom-0 h-full transition-all duration-1000 ${slots.Middle ? 'bg-wood/10 opacity-100' : 'opacity-0'}`}
                   style={{ clipPath: 'polygon(25% 0%, 75% 0%, 100% 100%, 0% 100%)' }} />
              <span className="text-[7px] uppercase tracking-[0.2em] mb-1 font-bold">Middle</span>
              <span className="text-[10px] md:text-[11px] font-medium tracking-tight text-center">
                {slots.Middle ? slots.Middle.name : "Select"}
              </span>
            </div>

            {/* BASE SLOT */}
            <div 
              onClick={() => handleTabChange('Base')}
              className={`relative z-10 w-full h-[30%] flex flex-col items-center justify-start pt-4 cursor-pointer transition-all duration-700 ${
                slots.Base ? 'text-wood' : 'text-wood/20'
              } ${activeTab === 'Base' ? 'scale-110' : 'hover:scale-105'}`}
            >
              <div className={`absolute inset-x-0 bottom-0 h-full transition-all duration-1000 ${slots.Base ? 'bg-wood/10 opacity-100' : 'opacity-0'}`}
                   style={{ clipPath: 'polygon(15% 0%, 85% 0%, 100% 100%, 0% 100%)' }} />
              <span className="text-[7px] uppercase tracking-[0.2em] mb-1 font-bold">Base</span>
              <span className="text-[10px] md:text-[11px] font-medium tracking-tight text-center">
                {slots.Base ? slots.Base.name : "Select"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 1. 탭 네비게이션 */}
      <div className="relative z-10 flex gap-6 md:gap-8 mb-16 w-full justify-center">
        {(['Top', 'Middle', 'Base'] as const).map((tab) => (
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
            {slots[tab] && (
              <div className="absolute -top-1 -right-2 w-1 h-1 bg-wood rounded-full" />
            )}
          </button>
        ))}
      </div>

      {/* 2. 캐러셀 메인 영역 */}
      <div className="relative z-10 w-full flex flex-col items-center max-w-2xl">
        <div className="text-[10px] tracking-[0.3em] text-wood/30 uppercase mb-8 font-mono">
          {currentIndex + 1} / {totalNotes}
        </div>

        <div className="flex items-center justify-between w-full mb-12 gap-4 sm:gap-16">
          <button
            onClick={handlePrev}
            className="p-4 text-wood/20 hover:text-wood transition-colors flex-shrink-0"
            aria-label="Previous note"
          >
            <ChevronLeft size={28} strokeWidth={1} />
          </button>

          <div 
            key={`${activeTab}-${currentIndex}`}
            className="flex-1 text-center animate-in fade-in slide-in-from-bottom-2 duration-1000 ease-out cursor-pointer group/card"
            onClick={() => toggleNote(currentNote)}
          >
            <div className="relative inline-block mb-4">
              <h3 className={`text-3xl md:text-5xl font-light tracking-tight transition-all duration-700 ${isSelected ? 'text-wood scale-105' : 'text-wood/80'} mb-2`} style={{ fontFamily: "'Playfair Display', serif" }}>
                {currentNote?.name}
              </h3>
              {isSelected && (
                <div className="absolute -top-2 -right-6 text-wood animate-in zoom-in duration-500">
                  <Check size={20} strokeWidth={3} />
                </div>
              )}
            </div>
            <p className="text-[10px] uppercase tracking-[0.4em] text-wood/30 mb-8">{currentNote?.enName}</p>
            
            <div className="max-w-md mx-auto space-y-8">
              <p className="text-[16px] md:text-[18px] leading-relaxed text-wood/70 break-keep font-light transition-colors group-hover/card:text-wood/90 italic">
                "{currentNote?.description}"
              </p>
              
              <div className="flex flex-col items-center gap-1.5 opacity-60 group-hover/card:opacity-100 transition-opacity">
                <span className="text-[8px] uppercase tracking-[0.2em] text-wood/40">Scent Origin</span>
                <p className="text-[12px] text-wood/60 font-medium tracking-wide">{currentNote?.origin}</p>
              </div>
            </div>
          </div>

          <button
            onClick={handleNext}
            className="p-4 text-wood/20 hover:text-wood transition-colors flex-shrink-0"
            aria-label="Next note"
          >
            <ChevronRight size={28} strokeWidth={1} />
          </button>
        </div>

        <button
          onClick={() => toggleNote(currentNote)}
          className={`px-12 py-4 rounded-full text-[11px] uppercase tracking-[0.2em] transition-all duration-500 border ${
            isSelected 
              ? 'bg-wood text-cream border-wood shadow-xl scale-105' 
              : 'bg-transparent text-wood/60 border-wood/20 hover:border-wood/40 hover:text-wood hover:bg-wood/5'
          }`}
        >
          {isSelected ? 'Placed in Pyramid' : `Place as ${activeTab} Note`}
        </button>
      </div>

      {/* 3. 하단 점 인디케이터 */}
      <div className="relative z-10 flex gap-2 mt-16">
        {currentNotes.map((note, idx) => {
          const isNoteSelected = Object.values(slots).some(n => n?.enName === note.enName);
          return (
            <button
              key={idx}
              onClick={() => handleDotClick(idx)}
              className={`h-1 rounded-full transition-all duration-500 ease-in-out relative ${
                currentIndex === idx 
                  ? 'w-10 bg-wood' 
                  : 'w-2.5 bg-wood/10 hover:bg-wood/20'
              }`}
            >
              {isNoteSelected && currentIndex !== idx && (
                <div className="absolute -top-1.5 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-wood rounded-full shadow-sm" />
              )}
            </button>
          );
        })}
      </div>

      <div className="relative z-10 mt-16 flex items-center gap-3 text-[10px] text-wood/20 tracking-[0.3em] uppercase italic">
        <Info size={12} strokeWidth={1.5} />
        <span>Balanced selection ensures a more accurate AI style match</span>
      </div>
    </div>
  );
}




// EOF: ScentNoteCarousel.tsx
