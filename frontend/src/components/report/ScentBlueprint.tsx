import ScentPyramid from "@/components/common/ScentPyramid";
<<<<<<< HEAD
import { ArrowRight } from "lucide-react";
=======
>>>>>>> c5c5017 (feat(frontend): migrate react fragrance experienceAdds the Vite React application, Tailwind styling, Zustand state, API services, report capture flow, reusable UI components, and static imagery for the Olfit fragrance matching experience.)
import type { ScentNote } from "@/data/noteData";

interface ScentBlueprintProps {
  isVisible: boolean;
  slots: {
    Top: ScentNote | null;
    Middle: ScentNote | null;
    Base: ScentNote | null;
  };
  matchPercent: number;
  accentClass: string;
}

export default function ScentBlueprint({ isVisible, slots, matchPercent, accentClass }: ScentBlueprintProps) {
  const hasNoNotes = !slots.Top && !slots.Middle && !slots.Base;

  return (
    <div className={`mb-32 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
      <div className="flex items-center gap-4 mb-12">
        <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-wood/30">My Scent Blueprint</span>
        <h3 className={`text-xl font-light tracking-widest uppercase ${accentClass}`}>Scent Blueprint</h3>
        <div className="h-px bg-wood/10 flex-1" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-24">
        <div className="flex justify-center">
          <ScentPyramid slots={slots} isStatic={true} className="w-72 h-72 md:w-80 md:h-80" />
        </div>
        <div className="flex flex-col justify-center text-center lg:text-left">
          <p className="text-wood/60 uppercase tracking-widest text-[11px] mb-2 font-mono">AI Analysis Result</p>
          <h4 className="text-2xl md:text-3xl font-light text-wood break-keep leading-tight">
            {hasNoNotes ? (
              <>당신의 시각적 아우라와 <br/> 향기 싱크로율이 <span className="font-medium text-gold">{matchPercent}%</span> 입니다</>
            ) : (
              <>AI가 분석한 당신의 무드와 <br/> <span className="font-medium text-gold">{matchPercent}%</span> 일치합니다</>
            )}
          </h4>
          <p className="mt-6 text-[13px] text-wood leading-relaxed max-w-lg mx-auto lg:mx-0 break-keep">
            {hasNoNotes ? (
              "선택하신 향기 정보가 없어, 업로드하신 이미지의 색채와 실루엣 분석 데이터만을 바탕으로 당신에게 가장 잘 어울리는 향기 밸런스를 도출했습니다."
            ) : (
              <>
                선택하신 {
                  [slots.Top?.name, slots.Middle?.name, slots.Base?.name]
                    .filter(Boolean)
                    .join(", ")
                } 노트를 바탕으로 <br /> 당신의 시각적 아우라와 가장 조화로운 향기 밸런스를 찾았습니다.
              </>
            )}
          </p>
          {hasNoNotes && (
            <a 
              href="#guide"
              className="inline-flex items-center gap-2 mt-6 text-[11px] uppercase tracking-widest text-wood/50 hover:text-wood border-b border-wood/20 hover:border-wood/60 pb-0.5 transition-all duration-300 self-start mx-auto lg:mx-0"
            >
              원료를 선택하면 더 정확한 매칭이 가능해요
              <ArrowRight size={11} />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
