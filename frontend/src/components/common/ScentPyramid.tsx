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
  return (
    <div className={`relative flex flex-col items-center group ${className}`}>
      <svg className="absolute inset-0 w-full h-full pointer-events-none drop-shadow-sm" viewBox="0 0 100 100">
        <path d="M50 5 L95 90 L5 90 Z" fill="none" stroke="currentColor" strokeWidth="0.2" className="text-wood/20" />
        <line x1="35.2" y1="33" x2="64.8" y2="33" stroke="currentColor" strokeWidth="0.15" className="text-wood/10" />
        <line x1="19.8" y1="62" x2="80.2" y2="62" stroke="currentColor" strokeWidth="0.15" className="text-wood/10" />
      </svg>

      <div className="w-full h-full flex flex-col items-center pt-2 pb-8">
        {/* TOP SLOT */}
        <div 
          onClick={() => !isStatic && onTabChange?.('Top')}
          className={`relative z-10 w-full h-[32%] flex flex-col items-center justify-end pb-4 transition-all duration-700 ${
            !isStatic ? 'cursor-pointer' : ''
          } ${slots.Top ? 'text-wood' : 'text-wood/20'} ${!isStatic && activeTab === 'Top' ? 'scale-105' : 'hover:scale-102'}`}
        >
          <span className="text-[7px] uppercase tracking-[0.3em] mb-1.5 font-bold">Top</span>
          <span className={`text-[11px] md:text-[12px] font-medium tracking-tight truncate max-w-[80px] text-center px-2 transition-colors duration-500 ${slots.Top ? 'text-wood' : 'text-wood/40 italic opacity-50'}`}>
            {slots.Top ? slots.Top.name : "Select"}
          </span>
        </div>

        {/* MIDDLE SLOT */}
        <div 
          onClick={() => !isStatic && onTabChange?.('Middle')}
          className={`relative z-10 w-full h-[32%] flex flex-col items-center justify-center transition-all duration-700 ${
            !isStatic ? 'cursor-pointer' : ''
          } ${slots.Middle ? 'text-wood' : 'text-wood/20'} ${!isStatic && activeTab === 'Middle' ? 'scale-105' : 'hover:scale-102'}`}
        >
          <span className="text-[7px] uppercase tracking-[0.3em] mb-1.5 font-bold">Middle</span>
          <span className={`text-[11px] md:text-[12px] font-medium tracking-tight text-center px-2 transition-colors duration-500 ${slots.Middle ? 'text-wood' : 'text-wood/40 italic opacity-50'}`}>
            {slots.Middle ? slots.Middle.name : "Select"}
          </span>
        </div>

        {/* BASE SLOT */}
        <div 
          onClick={() => !isStatic && onTabChange?.('Base')}
          className={`relative z-10 w-full h-[34%] flex flex-col items-center justify-start pt-6 transition-all duration-700 ${
            !isStatic ? 'cursor-pointer' : ''
          } ${slots.Base ? 'text-wood' : 'text-wood/20'} ${!isStatic && activeTab === 'Base' ? 'scale-105' : 'hover:scale-102'}`}
        >
          <span className="text-[7px] uppercase tracking-[0.3em] mb-1.5 font-bold">Base</span>
          <span className={`text-[11px] md:text-[12px] font-medium tracking-tight text-center px-2 transition-colors duration-500 ${slots.Base ? 'text-wood' : 'text-wood/40 italic opacity-50'}`}>
            {slots.Base ? slots.Base.name : "Select"}
          </span>
        </div>
      </div>
    </div>
  );
}
