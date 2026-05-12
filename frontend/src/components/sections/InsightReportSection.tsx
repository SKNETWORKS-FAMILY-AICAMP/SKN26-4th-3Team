/**
 * @file InsightReportSection.tsx
 * @description AI 인터뷰 결과를 바탕으로 사용자의 향기 아우라를 분석하여 시각화해 주는 섹션입니다.
 */

import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import RadarChart from "@/components/common/RadarChart";
import { radarData } from "@/data/reportData";
import { scentNotes } from "@/data/noteData";
import { getRecommendedProducts } from "@/services/recommendationEngine";
import { captureReportBlob, shareOrDownloadImage } from "@/services/reportCapture";
import { useRef, useMemo, useState } from "react";

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

const fallbackRadarAdjustments = [0.06, 0.03, 0.08, 0.05, 0.02];

export default function InsightReportSection({ results, onProductClick }: InsightReportSectionProps) {
  const { ref: refHeader, isVisible: visHeader } = useIntersectionObserver();
  const { ref: refRadar, isVisible: visRadar } = useIntersectionObserver();
  const { ref: refSteps, isVisible: visSteps } = useIntersectionObserver();
  const { ref: refPyramid, isVisible: visPyramid } = useIntersectionObserver();
  const reportRef = useRef<HTMLDivElement>(null);
  const isCapturingRef = useRef(false);

  const [sortBy, setSortBy] = useState<"recommended" | "price">("recommended");
  const [isSaving, setIsSaving] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  const baseRecommendations = useMemo(() => getRecommendedProducts(results), [results]);

  const slots = useMemo(() => {
    const selected = results?.analysisMetadata?.selectedNotes || [];
    return {
      Top: scentNotes.find(n => n.category === "Top" && selected.includes(n.name)) || null,
      Middle: scentNotes.find(n => n.category === "Middle" && selected.includes(n.name)) || null,
      Base: scentNotes.find(n => n.category === "Base" && selected.includes(n.name)) || null,
    };
  }, [results]);

  const matchPercent = baseRecommendations.length > 0 ? baseRecommendations[0].similarity : 0;

  const recommendations = useMemo(() => {
    const sorted = [...baseRecommendations];
    if (sortBy === "price") {
      return sorted.sort((a, b) => {
        const priceA = parseInt(a.price.replace(/[^0-9]/g, "")) || 0;
        const priceB = parseInt(b.price.replace(/[^0-9]/g, "")) || 0;
        return priceA - priceB;
      });
    }
    return sorted;
  }, [baseRecommendations, sortBy]);

  const dynamicLogicSteps = [
    `업로드된 이미지에서 추출된 ${results?.personalMood || "#현대적 #시크"} 무드 분석`,
    results?.analysisMetadata?.selectedNotes && results.analysisMetadata.selectedNotes.filter(Boolean).length > 0
      ? `사용자가 선택한 원료(${results.analysisMetadata.selectedNotes.filter(Boolean).join(", ")})와의 조화 계산`
      : "이미지의 색채 심리학적 데이터 기반 향기 맵 생성",
    `최적의 향기 아우라 매칭: ${recommendations[0]?.name || "분석 중"}`,
    "시각적 무드와 후각적 취향의 완벽한 밸런스 완성",
  ];

  const currentRadarData = useMemo(() => {
    if (!results) return radarData;
    const scores = results.analysisMetadata?.radarScores;

    return [
      { axis: "플로랄", value: scores?.["플로랄"] ?? 0.2 },
      { axis: "우디", value: scores?.["우디"] ?? 0.5 },
      { axis: "앰버", value: scores?.["앰버"] ?? 0.3 },
      { axis: "프레시", value: scores?.["프레시"] ?? 0.4 },
      { axis: "구르망", value: scores?.["구르망"] ?? 0.2 },
    ].map((d, index) => ({
      ...d,
      description: radarData.find(rd => rd.axis === d.axis)?.description,
      value: scores ? d.value : Math.max(0.1, Math.min(0.95, d.value + fallbackRadarAdjustments[index]))
    }));
  }, [results]);

  const theme = { bg: "bg-cream", accent: "text-wood", border: "border-wood/10" };

  const handleShareResults = async () => {
    if (isCapturingRef.current) return;
    isCapturingRef.current = true;
    setIsSaving(true);
    try {
      const blob = await captureReportBlob(reportRef.current);
      if (!blob) throw new Error("Blob creation failed");
      const result = await shareOrDownloadImage(blob);
      if (result === "copied") {
        setFeedback("이미지 복사 완료!");
        setTimeout(() => setFeedback(null), 2000);
      } else if (result === "downloaded") {
        setFeedback("이미지 저장 완료!");
        setTimeout(() => setFeedback(null), 2000);
      }
    } catch (err) {
      console.error("Report processing error:", err);
    } finally {
      isCapturingRef.current = false;
      setIsSaving(false);
    }
  };

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
                isSaving={isSaving} 
                feedback={feedback} 
                onShare={handleShareResults} 
              />
            </div>

            <div ref={reportRef} id="report-content" className="p-4 md:p-8 rounded-lg bg-[#FDFCF0]">
              <div ref={refPyramid}>
                <ScentBlueprint 
                  isVisible={visPyramid || !!results} 
                  slots={slots} 
                  matchPercent={matchPercent} 
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
                    <RadarChart data={currentRadarData} forceDraw={true} />
                  </div>
                  <div ref={refSteps}>
                    <AuraAnalysisSteps 
                      isVisible={visSteps || !!results} 
                      logicSteps={dynamicLogicSteps} 
                      borderClass={theme.border} 
                    />
                  </div>
                </div>

                <RecommendationList 
                  recommendations={recommendations} 
                  onProductClick={onProductClick} 
                  slots={slots} 
                  sortBy={sortBy} 
                  onSortChange={setSortBy} 
                />
              </div>
            </div>
          </>
        )}
      </div>
    </section>
  );
}
