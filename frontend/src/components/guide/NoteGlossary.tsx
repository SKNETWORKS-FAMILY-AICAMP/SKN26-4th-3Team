/**
 * @file NoteGlossary.tsx
 * @description 향수의 주요 원료(Note) 정보를 카드 형태로 시각화하고, 사용자의 선호 원료를 수집하는 인터랙티브 컴포넌트입니다.
 * 탑, 미들, 베이스 노트별 분류를 제공하며, 최대 3개의 원료를 선택할 수 있는 기능을 포함합니다.
 */

import { useState } from "react";
import { scentNotes } from "@/data/noteData";
import { Check, RefreshCw } from "lucide-react";
import type { ScentNote } from "@/data/noteData";

interface NoteGlossaryProps {
  /** 선택된 노드들이 변경될 때 부모 컴포넌트로 전달하는 콜백 */
  onNotesChange?: (notes: string[]) => void;
}

export default function NoteGlossary({ onNotesChange }: NoteGlossaryProps) {
  /** 현재 마우스가 올라가 있는 노트 ID */
  const [hoveredNote, setHoveredNote] = useState<string | null>(null);
  /** 현재 사용자가 선택한 노트 객체 리스트 (최대 3개) */
  const [selectedNotes, setSelectedNotes] = useState<ScentNote[]>([]);

  /**
   * 노트를 선택하거나 해제하는 핸들러
   */
  const toggleNote = (note: ScentNote) => {
    let newNotes;
    // 이미 선택된 경우 제거
    if (selectedNotes.find((n) => n.enName === note.enName)) {
      newNotes = selectedNotes.filter((n) => n.enName !== note.enName);
    } 
    // 선택되지 않았고 3개 미만인 경우 추가
    else if (selectedNotes.length < 3) {
      newNotes = [...selectedNotes, note];
    } 
    // 3개 초과 선택 시 무시
    else {
      return;
    }
    
    setSelectedNotes(newNotes);
    if (onNotesChange) {
      onNotesChange(newNotes.map(n => n.name));
    }
  };

  /**
   * 선택된 모든 노트를 초기화
   */
  const resetNotes = () => {
    setSelectedNotes([]);
    if (onNotesChange) onNotesChange([]);
  };

  /**
   * 개별 노트 카드를 렌더링합니다.
   */
  const renderNoteCard = (note: ScentNote) => {
    const isSelected = selectedNotes.find((n) => n.enName === note.enName);
    return (
      <div
        key={note.enName}
        className={`group relative h-40 md:h-44 border rounded-sm p-4 cursor-pointer transition-all duration-500 overflow-hidden ${
          isSelected 
            ? 'bg-wood border-wood shadow-lg' 
            : 'bg-white/40 border-wood/5 hover:border-wood/20'
        }`}
        onClick={() => toggleNote(note)}
        onMouseEnter={() => setHoveredNote(note.enName)}
        onMouseLeave={() => setHoveredNote(null)}
      >
        {/* 선택 완료 체크 아이콘 */}
        {isSelected && (
          <div className="absolute top-3 right-3 text-cream animate-in zoom-in duration-300">
            <Check size={14} strokeWidth={3} />
          </div>
        )}

        {/* 기본 정보 레이어 */}
        <div className={`flex flex-col justify-between h-full transition-all duration-300 ${hoveredNote === note.enName && !isSelected ? 'opacity-0 scale-95' : 'opacity-100 scale-100'}`}>
          <span className={`text-[9px] uppercase tracking-widest ${isSelected ? 'text-cream/40' : 'text-wood/40'}`}>
            {note.category} Note
          </span>
          <div>
            <h4 className={`text-sm md:text-base font-medium transition-colors ${isSelected ? 'text-cream' : 'text-wood'}`}>
              {note.name}
            </h4>
            <p className={`text-[9px] uppercase tracking-tighter ${isSelected ? 'text-cream/30' : 'text-wood/20'}`}>
              {note.enName}
            </p>
          </div>
        </div>

        {/* 호버 정보 레이어 (설명 및 원산지) */}
        {!isSelected && (
          <div className={`absolute inset-0 p-4 flex flex-col justify-center transition-all duration-500 ${hoveredNote === note.enName ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'}`}>
            <p className="text-[11px] leading-relaxed text-wood/80 break-keep mb-3">
              {note.description}
            </p>
            <div className="pt-2 border-t border-wood/10">
              <p className="text-[8px] uppercase tracking-widest text-wood/30 mb-0.5">Origin</p>
              <p className="text-[9px] text-wood/50 line-clamp-1">{note.origin}</p>
            </div>
          </div>
        )}
      </div>
    );
  };

  const categories: ("Top" | "Middle" | "Base")[] = ["Top", "Middle", "Base"];

  return (
    <div className="mt-24 pt-24 border-t border-wood/10">
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
        <div>
          <h3 className="text-[11px] md:text-[12px] font-bold uppercase tracking-[0.2em] text-wood/30 mb-2">
            03. Perfumery Notes (향기 원료 사전)
          </h3>
          <p className="text-sm text-wood/60 break-keep">
            마음에 드는 <span className="text-wood font-medium">원료를 최대 3개</span>까지 선택해 보세요. 당신의 스타일 사진과 함께 분석하여 가장 닮은 향수를 찾아드립니다.
          </p>
          {selectedNotes.length === 0 && (
            <p className="text-[10px] text-wood/30 mt-2 italic">
              * 선택하지 않으셔도 분석이 가능하지만, 취향이 반영되지 않을 수 있습니다.
            </p>
          )}
        </div>
        
        {/* 상단 컨트롤 바: 선택 수 지표 및 초기화 버튼 */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            {[1, 2, 3].map((num) => (
              <div 
                key={num} 
                className={`w-2.5 h-2.5 rounded-full border transition-colors duration-500 ${
                  selectedNotes.length >= num ? 'bg-wood border-wood' : 'border-wood/20'
                }`} 
              />
            ))}
          </div>
          <button 
            onClick={resetNotes}
            className="flex items-center gap-1.5 text-[10px] uppercase tracking-widest text-wood/40 hover:text-wood transition-colors"
          >
            <RefreshCw size={12} />
            Reset
          </button>
        </div>
      </div>

      {/* 카테고리별 노트 그리드 영역 */}
      <div className="space-y-12">
        {categories.map(category => {
          const notes = scentNotes.filter(n => n.category === category);
          if (notes.length === 0) return null;
          
          return (
            <div key={category}>
              <div className="flex items-center gap-3 mb-6">
                <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-wood/20">{category}</span>
                <div className="h-px bg-wood/5 flex-1" />
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-8 gap-4">
                {notes.map(renderNoteCard)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// EOF: NoteGlossary.tsx
