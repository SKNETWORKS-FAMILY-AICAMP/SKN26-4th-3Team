import { Share2, Check } from "lucide-react";

interface ReportHeaderProps {
  isVisible: boolean;
  isSaving: boolean;
  feedback: string | null;
  onShare: () => void;
}

export default function ReportHeader({ isVisible, isSaving, feedback, onShare }: ReportHeaderProps) {
  return (
    <div className={`flex flex-col items-center mb-20 transition-all duration-800 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
      <p className="label-upper text-wood/40 mb-4">Diagnosis Report</p>
      <h2 className="text-3xl sm:text-4xl md:text-5xl font-light tracking-tight break-keep text-wood mb-10 text-center">
        당신의 비주얼 아우라 진단
      </h2>
      
      <div className="flex justify-center">
        <button 
          onClick={onShare}
          disabled={isSaving}
          className={`group flex items-center gap-3 px-8 py-3.5 border rounded-full text-[11px] sm:text-[12px] uppercase tracking-[0.2em] transition-all duration-300 ${
            isSaving 
              ? "bg-wood/5 text-wood/30 border-wood/10 cursor-not-allowed" 
              : feedback 
                ? "bg-green-50 text-green-600 border-green-200" 
                : "bg-wood text-cream border-wood hover:bg-wood/90 hover:shadow-lg active:scale-95"
          }`}
        >
          {isSaving ? (
            <>
              <div className="w-3 h-3 border-2 border-wood/20 border-t-wood rounded-full animate-spin" />
              <span className="hidden sm:inline">고화질 리포트 정밀 생성 중...</span>
              <span className="sm:hidden">생성 중...</span>
            </>
          ) : feedback ? (
            <>
              <Check size={16} />
              {feedback}
            </>
          ) : (
            <>
              <Share2 size={16} className="group-hover:rotate-12 transition-transform" />
              Share & Save Report
            </>
          )}
        </button>
      </div>
    </div>
  );
}
