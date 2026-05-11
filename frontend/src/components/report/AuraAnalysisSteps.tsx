interface AuraAnalysisStepsProps {
  isVisible: boolean;
  logicSteps: string[];
  borderClass: string;
}

export default function AuraAnalysisSteps({ 
  isVisible, 
  logicSteps, 
  borderClass 
}: AuraAnalysisStepsProps) {
  
  const renderText = (text: string) => {
    return text.split("<br/>").map((line, i) => (
      <span key={i}>
        {line}
        {i < text.split("<br/>").length - 1 && <br />}
      </span>
    ));
  };

  return (
    <div className={`transition-all duration-800 delay-200 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
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
  );
}
