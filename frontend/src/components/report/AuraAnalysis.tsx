import RadarChart from "@/components/common/RadarChart";

interface AuraAnalysisProps {
  isRadarVisible: boolean;
  isStepsVisible: boolean;
  radarData: any[];
  logicSteps: string[];
  borderClass: string;
}

export default function AuraAnalysis({ 
  isRadarVisible, 
  isStepsVisible, 
  radarData, 
  logicSteps, 
  borderClass 
}: AuraAnalysisProps) {
  
  const renderText = (text: string) => {
    return text.split("<br/>").map((line, i) => (
      <span key={i}>
        {line}
        {i < text.split("<br/>").length - 1 && <br />}
      </span>
    ));
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-24">
      <div className={`transition-all duration-800 delay-100 ${isRadarVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
        <RadarChart data={radarData} forceDraw={true} />
      </div>

      <div className={`transition-all duration-800 delay-200 ${isStepsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
        <div className="space-y-0 mb-12">
          {logicSteps.map((step, i) => (
            <div key={i} className={`group py-5 border-b ${borderClass} flex items-start gap-4 hover:bg-wood/[0.01] transition-colors duration-300`}>
              <span className="text-[11px] font-medium text-wood/30 mt-0.5 font-mono">0{i + 1}</span>
              <p className="text-[15px] leading-relaxed text-wood/70 group-hover:text-wood break-keep">
                {renderText(step)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
