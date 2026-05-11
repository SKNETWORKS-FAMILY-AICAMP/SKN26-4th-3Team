/**
 * @file InsightReportSection.tsx
 * @description AI 인터뷰 결과를 바탕으로 사용자의 향기 아우라를 분석하여 시각화해 주는 섹션입니다.
 */

import RadarChart from "@/components/common/RadarChart";
import { useInsightReport } from "@/hooks/useInsightReport"; // 🛠️ REFACTOR (유지보수성): 커스텀 훅 도입

// 분리된 모듈 임포트
import ReportHeader from "@/components/report/ReportHeader";
import ScentBlueprint from "@/components/report/ScentBlueprint";
import AuraAnalysisSteps from "@/components/report/AuraAnalysisSteps";
import RecommendationList from "@/components/report/RecommendationList";

import type { AnalysisResults } from "@/types";
import type { Product } from "@/data/productData";

interface InsightReportSectionProps {
  results: AnalysisResults | null;
  onProductClick: (product: Product) => void;
}

export default function InsightReportSection({ results, onProductClick }: InsightReportSectionProps) {
  // 🛠️ REFACTOR (유지보수성): 모든 비즈니스 로직과 상태를 useInsightReport 훅으로 위임
  const {
    refs: { refHeader, refRadar, refSteps, refPyramid },
    visibility: { visHeader, visRadar, visSteps, visPyramid },
    reportRef,
    state,
    derived,
    actions
  } = useInsightReport(results);

  const theme = { bg: "bg-cream", accent: "text-wood", border: "border-wood/10" };

  return (
    <section id="report" className={`${theme.bg} py-24 md:py-40 transition-colors duration-1000`}>
      <div className="max-w-[1440px] mx-auto px-6 md:px-8">
        {!results ? (
          <div className="max-w-2xl mx-auto text-center py-20 border border-wood/10 rounded-sm">
            <p className="text-wood/40 uppercase tracking-widest text-[11px] mb-4">Awaiting Analysis</p>
            <h2 className="text-xl sm:text-2xl font-light mb-8 break-keep px-4 text-wood">
              AI 비주얼 분석을 완료하면 <span className="hidden sm:inline"><br/></span> 당신만의 아우라 리포트가 생성됩니다.
            </h2>
          </div>
        ) : (
          <>
            <div ref={refHeader}>
              <ReportHeader 
                isVisible={visHeader || !!results} 
                isSaving={state.isSaving} 
                feedback={state.feedback} 
                onShare={actions.handleShareResults} 
              />
            </div>

            <div ref={reportRef} id="report-content" data-capture-target="true" className="p-4 md:p-8 rounded-lg bg-[#FDFCF0]">
              <div ref={refPyramid}>
                <ScentBlueprint 
                  isVisible={visPyramid || !!results} 
                  slots={derived.slots} 
                  matchPercent={derived.matchPercent} 
                  accentClass={theme.accent} 
                />
              </div>

              <div className="mb-32 animate-in fade-in duration-1000">
                <div className="flex items-center gap-4 mb-12">
                  <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-wood/30">Visual Analysis</span>
                  <h3 className={`text-xl font-light tracking-widest uppercase ${theme.accent}`}>Personal Aura</h3>
                  <div className="h-px bg-wood/10 flex-1" />
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-24 mb-12">
                  <div ref={refRadar} className={`transition-all duration-800 delay-100 ${(visRadar || !!results) ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
                    <RadarChart data={derived.currentRadarData} forceDraw={true} />
                  </div>
                  <div ref={refSteps}>
                    <AuraAnalysisSteps 
                      isVisible={visSteps || !!results} 
                      logicSteps={derived.dynamicLogicSteps} 
                      borderClass={theme.border} 
                    />
                  </div>
                </div>

                <RecommendationList 
                  recommendations={derived.recommendations} 
                  onProductClick={onProductClick} 
                  slots={derived.slots} 
                  sortBy={state.sortBy} 
                  onSortChange={actions.setSortBy} 
                />
              </div>
            </div>
          </>
        )}
      </div>
    </section>
  );
}
