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

export default function InsightReportSection({ results, onProductClick }: InsightReportSectionProps) {
  const { ref: refHeader, isVisible: visHeader } = useIntersectionObserver();
  const { ref: refRadar, isVisible: visRadar } = useIntersectionObserver();
  const { ref: refSteps, isVisible: visSteps } = useIntersectionObserver();
  const { ref: refPyramid, isVisible: visPyramid } = useIntersectionObserver();
  const reportRef = useRef<HTMLDivElement>(null);

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
        // 백엔드에서 제공하는 수치형 원화 가격(price_krw) 사용
        const priceA = (a as any).price_krw || 0;
        const priceB = (b as any).price_krw || 0;
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
      { axis: "오리엔탈", value: scores?.["오리엔탈"] ?? 0.3 },
      { axis: "프레시", value: scores?.["프레시"] ?? 0.4 },
      { axis: "구르망", value: scores?.["구르망"] ?? 0.2 },
    ].map(d => ({
      ...d,
      description: radarData.find(rd => rd.axis === d.axis)?.description,
      // API 데이터가 있으면 그대로 쓰고, 없으면 랜덤 보정값 사용
      value: scores ? d.value : Math.max(0.1, Math.min(0.95, d.value + (Math.random() * 0.1)))
    }));
  }, [results]);

  const theme = { bg: "bg-cream", accent: "text-wood", border: "border-wood/10" };

  const handleShareResults = async () => {
    if (isSaving) return;
    setIsSaving(true);
    setFeedback(null); // 기존 피드백 초기화

    try {
      // 1. 렌더링 안정화를 위해 아주 짧은 지연
      await new Promise(resolve => setTimeout(resolve, 300));
      
      // 2. 리포트 캡처 (공유창이 뜨기 전에 완전히 완료해야 함)
      const blob = await captureReportBlob(reportRef.current);
      if (!blob) throw new Error("Blob creation failed");
      
      // 3. 캡처가 완료된 후 아주 짧은 지연 뒤에 공유 창 호출
      await new Promise(resolve => setTimeout(resolve, 200));
      const result = await shareOrDownloadImage(blob);
      
      // 4. 결과 피드백 처리
      if (result === "copied") {
        setFeedback("이미지 복사 완료!");
      } else if (result === "downloaded") {
        setFeedback("리포트 저장 완료!");
      } else if (result === "shared") {
        setFeedback("공유 완료!");
      }
      
      if (result !== "failed") {
        setTimeout(() => setFeedback(null), 3000);
      }
    } catch (err) {
      console.error("Report processing error:", err);
      setFeedback("캡처 중 오류 발생");
      setTimeout(() => setFeedback(null), 3000);
    } finally {
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
                isVisible={true} // 결과가 있으면 무조건 보이도록 강제 (디버깅 및 UX 개선)
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
