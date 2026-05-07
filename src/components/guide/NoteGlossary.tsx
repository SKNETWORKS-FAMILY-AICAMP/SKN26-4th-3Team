/**
 * @file NoteGlossary.tsx
 * @description 향수의 주요 원료들에 대한 설명을 카드 형태로 보여주는 컴포넌트입니다.
 * 사용자가 선호하는 원료를 선택하면 부모 컴포넌트로 전달합니다.
 */

import { useState } from "react";
import { scentNotes } from "@/data/noteData";
import { Check, RefreshCw } from "lucide-react";
import type { ScentNote } from "@/data/noteData";

interface NoteGlossaryProps {
  onNotesChange?: (notes: string[]) => void;
}

export default function NoteGlossary({ onNotesChange }: NoteGlossaryProps) {
  const [hoveredNote, setHoveredNote] = useState<string | null>(null);
  const [selectedNotes, setSelectedNotes] = useState<ScentNote[]>([]);

  const toggleNote = (note: ScentNote) => {
    let newNotes;
    if (selectedNotes.find((n) => n.enName === note.enName)) {
      newNotes = selectedNotes.filter((n) => n.enName !== note.enName);
    } else if (selectedNotes.length < 3) {
      newNotes = [...selectedNotes, note];
    } else {
      return;
    }
    
    setSelectedNotes(newNotes);
    if (onNotesChange) {
      onNotesChange(newNotes.map(n => n.name));
    }
  };

  const resetNotes = () => {
    setSelectedNotes([]);
    if (onNotesChange) onNotesChange([]);
  };

  return (
    <div className="mt-24 pt-24 border-t border-wood/10">
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
        <div>
          <h3 className="text-[11px] md:text-[12px] font-bold uppercase tracking-[0.2em] text-wood/30 mb-2">
            03. Perfumery Notes (향기 원료 사전)
          </h3>
          <p className="text-sm text-wood/60 break-keep">
            마음에 드는 <span className="text-wood font-medium">3가지 원료</span>를 선택해 보세요. 당신의 스타일 사진과 함께 분석하여 가장 닮은 향수를 찾아드립니다.
          </p>
        </div>
        
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

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7 gap-4">
        {scentNotes.map((note: ScentNote) => {
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
              {/* 선택 표시 */}
              {isSelected && (
                <div className="absolute top-3 right-3 text-cream animate-in zoom-in duration-300">
                  <Check size={14} strokeWidth={3} />
                </div>
              )}

              {/* 기본 노출: 원료 이름 */}
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

              {/* 호버 시 노출: 상세 설명 (선택되지 않았을 때만) */}
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
        })}
      </div>
    </div>
  );
}
