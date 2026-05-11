/**
 * @file ConcentrationList.tsx
 * @description 향수의 부향률(Concentration) 정보를 체계적으로 리스트업하여 사용자에게 정보를 제공하는 컴포넌트입니다.
 * 농도별 향수 타입, 비율, 지속시간 및 특징을 시각화합니다.
 */

interface Concentration {
  type: string;
  koType: string;
  ratio: string;
  duration: string;
  desc: string;
}

interface ConcentrationListProps {
  /** 표시할 농도 정보 데이터 리스트 */
  concentrations: Concentration[];
}

export default function ConcentrationList({ concentrations }: ConcentrationListProps) {
  return (
    <div className="flex flex-col h-full">
      <h3 className="text-[11px] md:text-[12px] font-bold uppercase tracking-[0.2em] text-wood/30 mb-8 md:mb-10">
        01. Concentration (부향률)
      </h3>
      <div className="flex-1 bg-white/40 backdrop-blur-sm p-6 sm:p-8 md:p-12 rounded-sm border border-wood/5 flex flex-col justify-center">
        <div className="space-y-8 md:space-y-10">
          {concentrations.map((c) => (
            <div key={c.type} className="group border-b border-wood/10 pb-5 last:border-0 last:pb-0">
              <div className="flex justify-between items-end mb-2 md:mb-3 text-wood">
                <div className="flex items-baseline gap-2 md:gap-3">
                  <h4 className="text-lg md:text-xl font-medium">{c.type}</h4>
                  <span className="text-[11px] md:text-[12px] text-wood/50 font-normal">{c.koType}</span>
                </div>
                <span className="text-[10px] md:text-[12px] font-mono text-wood/40">{c.ratio} / {c.duration}</span>
              </div>
              <p className="text-[14px] md:text-[15px] text-wood/60 group-hover:text-wood transition-colors duration-300 break-keep">
                {c.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
      <p className="text-[9px] md:text-[10px] text-wood/30 mt-6 text-center italic uppercase tracking-widest">Guide to Concentration & Longevity</p>
    </div>
  );
}

// EOF: ConcentrationList.tsx
