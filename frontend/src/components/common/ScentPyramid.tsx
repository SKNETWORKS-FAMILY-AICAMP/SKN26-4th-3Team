import type { ScentNote } from "@/data/noteData";

interface ScentPyramidProps {
  slots: {
    Top: ScentNote | null;
    Middle: ScentNote | null;
    Base: ScentNote | null;
  };
  activeTab?: "Top" | "Middle" | "Base";
  onTabChange?: (tab: "Top" | "Middle" | "Base") => void;
  className?: string;
  isStatic?: boolean;
}

export default function ScentPyramid({ 
  slots, 
  activeTab, 
  onTabChange, 
  className = "", 
  isStatic = false 
}: ScentPyramidProps) {
  const slotTextClass = (isSelected: boolean) =>
    `text-[11px] md:text-[12px] tracking-tight text-center px-2 transition-all duration-300 ${
      isSelected
        ? "text-wood font-medium group-hover/slot:font-semibold"
        : "text-wood/60 italic font-normal group-hover/slot:text-wood group-hover/slot:font-semibold"
    }`;

  return (
    <div className={`relative flex flex-col items-center group ${className}`}>
      <svg className="absolute inset-0 w-full h-full pointer-events-none drop-shadow-sm" viewBox="0 0 100 100">
        <path d="M50 5 L95 90 L5 90 Z" fill="none" stroke="currentColor" strokeWidth="0.2" className="text-wood/35" />
        <line x1="35.2" y1="33" x2="64.8" y2="33" stroke="currentColor" strokeWidth="0.15" className="text-wood/25" />
        <line x1="19.8" y1="62" x2="80.2" y2="62" stroke="currentColor" strokeWidth="0.15" className="text-wood/25" />
      </svg>

      <div className="w-full h-full flex flex-col items-center pt-2 pb-8">
        {/* TOP SLOT */}
        <div 
          onClick={() => !isStatic && onTabChange?.('Top')}
          className={`group/slot relative z-10 w-full h-[32%] flex flex-col items-center justify-end pb-4 transition-all duration-700 ${
            !isStatic ? 'cursor-pointer' : ''
          } text-wood ${!isStatic && activeTab === 'Top' ? 'scale-105' : 'hover:scale-102'}`}
        >
          <span className="text-[7px] uppercase tracking-[0.3em] mb-1.5 font-bold">Top</span>
          <span className={`${slotTextClass(!!slots.Top)} truncate max-w-[80px]`}>
            {slots.Top ? slots.Top.name : "Select"}
          </span>
        </div>

        {/* MIDDLE SLOT */}
        <div 
          onClick={() => !isStatic && onTabChange?.('Middle')}
          className={`group/slot relative z-10 w-full h-[32%] flex flex-col items-center justify-center transition-all duration-700 ${
            !isStatic ? 'cursor-pointer' : ''
          } text-wood ${!isStatic && activeTab === 'Middle' ? 'scale-105' : 'hover:scale-102'}`}
        >
          <span className="text-[7px] uppercase tracking-[0.3em] mb-1.5 font-bold">Middle</span>
          <span className={slotTextClass(!!slots.Middle)}>
            {slots.Middle ? slots.Middle.name : "Select"}
          </span>
        </div>

        {/* BASE SLOT */}
        <div 
          onClick={() => !isStatic && onTabChange?.('Base')}
          className={`group/slot relative z-10 w-full h-[34%] flex flex-col items-center justify-start pt-6 transition-all duration-700 ${
            !isStatic ? 'cursor-pointer' : ''
          } text-wood ${!isStatic && activeTab === 'Base' ? 'scale-105' : 'hover:scale-102'}`}
        >
          <span className="text-[7px] uppercase tracking-[0.3em] mb-1.5 font-bold">Base</span>
          <span className={slotTextClass(!!slots.Base)}>
            {slots.Base ? slots.Base.name : "Select"}
          </span>
        </div>
      </div>
    </div>
  );
}
