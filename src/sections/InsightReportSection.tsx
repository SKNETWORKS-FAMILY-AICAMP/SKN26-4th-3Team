/**
 * @file InsightReportSection.tsx
 * @description AI 인터뷰 결과를 바탕으로 사용자의 향기 아우라를 분석하여 시각화해 주는 섹션입니다.
 * 비주얼 분석 결과와 추천 제품 리스트를 포함합니다.
 */

import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import RadarChart from "@/components/common/RadarChart";
import ProductCarousel from "@/components/report/ProductCarousel";
import { radarData } from "@/data/reportData";
import { getRecommendedProducts } from "@/data/recommendationEngine";
import { Download } from "lucide-react";
import html2canvas from "html2canvas";
import { useRef, useMemo, useState } from "react";
import type { AnalysisResults } from "@/types";
import type { Product } from "@/data/productData";

interface InsightReportSectionProps {
  results: AnalysisResults | null;
  onProductClick: (product: Product) => void;
}

export default function InsightReportSection({ results, onProductClick }: InsightReportSectionProps) {
  const { ref: ref1, isVisible: vis1 } = useIntersectionObserver();
  const { ref: ref2, isVisible: vis2 } = useIntersectionObserver();
  const { ref: ref3, isVisible: vis3 } = useIntersectionObserver();
  const reportRef = useRef<HTMLDivElement>(null);

  // 정렬 상태 추가
  const [sortBy, setSortBy] = useState<"recommended" | "price">("recommended");
  const [isSaving, setIsSaving] = useState(false);

  // 다이내믹 데이터 계산
  const baseRecommendations = useMemo(() => getRecommendedProducts(results), [results]);

  // 정렬된 추천 리스트 계산
  const recommendations = useMemo(() => {
    const sorted = [...baseRecommendations];
    if (sortBy === "price") {
      return sorted.sort((a, b) => {
        const priceA = parseInt(a.price.replace(/[^0-9]/g, "")) || 0;
        const priceB = parseInt(b.price.replace(/[^0-9]/g, "")) || 0;
        return priceA - priceB;
      });
    }
    // 기본은 이미 similarity 순으로 정렬되어 있음
    return sorted;
  }, [baseRecommendations, sortBy]);

  // 사용자의 선택에 따른 가변적인 로직 생성
  const dynamicLogicSteps = [
    `업로드된 이미지에서 추출된 #현대적 #시크 무드 분석`,
    `사용자가 선택한 원료(${results?.analysisMetadata?.selectedNotes.join(", ") || "선택 없음"})와의 조화 계산`,
    `최적의 향기 아우라 매칭: ${recommendations[0]?.name || "분석 중"}`,
    "시각적 무드와 후각적 취향의 완벽한 밸런스 완성",
  ];

  // 인터뷰 결과에 따른 레이더 차트 데이터 동적 계산
  const getDynamicRadarData = () => {
    if (!results) return radarData;
    const baseData = [
      { axis: "플로랄", value: 0.2 },
      { axis: "우디", value: 0.5 },
      { axis: "오리엔탈", value: 0.3 },
      { axis: "프레시", value: 0.4 },
      { axis: "구르망", value: 0.2 },
    ];
    return baseData.map(d => ({
      ...d,
      value: Math.max(0.1, Math.min(0.95, d.value + (Math.random() * 0.1)))
    }));
  };

  const currentRadarData = getDynamicRadarData();

  // 결과에 따른 다이내믹 테마 결정
  const getThemeColors = () => ({ bg: "bg-cream", accent: "text-wood", border: "border-wood/10" });
  const theme = getThemeColors();

  // 리포트 이미지 저장 함수
  const saveReportAsImage = async () => {
    if (!reportRef.current || isSaving) return;
    
    setIsSaving(true);
    
    // UI 업데이트와 애니메이션 안정을 위해 짧은 지연시간 부여
    await new Promise(resolve => setTimeout(resolve, 600));

    try {
      const canvas = await html2canvas(reportRef.current, {
        backgroundColor: "#FDFCF0",
        scale: 2,
        useCORS: true,
        logging: false,
        onclone: (clonedDoc) => {
          // 캡처 시점에만 특정 스타일을 강제로 고정하거나 조정할 수 있음
          const el = clonedDoc.getElementById("report-content");
          if (el) el.style.filter = "none";
        }
      });
      const image = canvas.toDataURL("image/png");
      const link = document.createElement("a");
      link.href = image;
      link.download = `Olfit_Report.png`;
      link.click();
    } catch (err) {
      console.error("이미지 저장 실패:", err);
    } finally {
      setIsSaving(false);
    }
  };

  const renderText = (text: string) => {
    return text.split("<br/>").map((line, i) => (
      <span key={i}>
        {line}
        {i < text.split("<br/>").length - 1 && <br />}
      </span>
    ));
  };

  return (
    <section id="report" className={`${theme.bg} py-24 md:py-40 transition-colors duration-1000`}>
      <div className="max-w-[1440px] mx-auto px-6 md:px-8">
        {!results && (
          <div className="max-w-2xl mx-auto text-center py-20 border border-wood/10 rounded-sm">
            <p className="text-wood/40 uppercase tracking-widest text-[11px] mb-4">Awaiting Analysis</p>
            <h2 className="text-xl sm:text-2xl font-light mb-8 break-keep px-4 text-wood">
              AI 비주얼 분석을 완료하면 <span className="hidden sm:inline"><br/></span> 당신만의 아우라 리포트가 생성됩니다.
            </h2>
          </div>
        )}

        {results && (
          <>
            <div ref={ref1} className={`flex flex-col items-center mb-20 transition-all duration-800 ${vis1 || results ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
              <p className="label-upper text-wood/40 mb-4">Diagnosis Report</p>
              <h2 className="text-3xl sm:text-4xl md:text-5xl font-light tracking-tight break-keep text-wood mb-10 text-center">
                당신의 비주얼 아우라 진단
              </h2>
              
              <button 
                onClick={saveReportAsImage}
                disabled={isSaving}
                className={`flex items-center gap-2 px-6 py-2.5 border border-wood/20 rounded-full text-[10px] sm:text-[11px] uppercase tracking-widest transition-all duration-300 ${
                  isSaving ? "bg-wood/10 text-wood/40 cursor-not-allowed" : "hover:bg-wood hover:text-cream"
                }`}
              >
                {isSaving ? (
                  <>
                    <div className="w-3 h-3 border-2 border-wood/20 border-t-wood rounded-full animate-spin" />
                    Preparing Image...
                  </>
                ) : (
                  <>
                    <Download size={14} />
                    Save Report as Image
                  </>
                )}
              </button>
            </div>

            <div ref={reportRef} id="report-content" className="p-4 md:p-8 rounded-lg">
              {/* 01. Aura Analysis */}
              <div className="mb-32 animate-in fade-in duration-1000">
                <div className="flex items-center gap-4 mb-12">
                  <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-wood/30">Visual Analysis</span>
                  <h3 className={`text-xl font-light tracking-widest uppercase ${theme.accent}`}>Personal Aura</h3>
                  <div className="h-px bg-wood/10 flex-1" />
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-24">
                  <div ref={ref2} className={`transition-all duration-800 delay-100 ${vis2 || results ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
                    <RadarChart data={currentRadarData} forceDraw={!!results} />
                  </div>

                  <div ref={ref3} className={`transition-all duration-800 delay-200 ${vis3 || results ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
                    <div className="space-y-0 mb-12">
                      {dynamicLogicSteps.map((step, i) => (
                        <div key={i} className={`group py-5 border-b ${theme.border} flex items-start gap-4 hover:bg-wood/[0.01] transition-colors duration-300`}>
                          <span className="text-[11px] font-medium text-wood/30 mt-0.5 font-mono">0{i + 1}</span>
                          <p className="text-[15px] leading-relaxed text-wood/70 group-hover:text-wood break-keep">{renderText(step)}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-32 pt-24 border-t border-wood/10">
                  <div className="flex flex-col items-center mb-16 gap-8">
                    <div className="flex items-center gap-2 p-1 bg-wood/5 rounded-full border border-wood/10">
                      <button
                        onClick={() => setSortBy("recommended")}
                        className={`px-6 py-2 rounded-full text-[10px] font-medium uppercase tracking-widest transition-all ${
                          sortBy === "recommended" ? "bg-wood text-cream shadow-md" : "text-wood/40 hover:text-wood"
                        }`}
                      >
                        추천순
                      </button>
                      <button
                        onClick={() => setSortBy("price")}
                        className={`px-6 py-2 rounded-full text-[10px] font-medium uppercase tracking-widest transition-all ${
                          sortBy === "price" ? "bg-wood text-cream shadow-md" : "text-wood/40 hover:text-wood"
                        }`}
                      >
                        가격순
                      </button>
                    </div>

                    <div className="text-center">
                      <p className="text-[10px] font-bold uppercase tracking-[0.3em] text-wood/30 mb-2">Matching Selection</p>
                      <h3 className="text-2xl font-light tracking-tight text-wood">당신의 스타일을 닮은 향기</h3>
                    </div>
                  </div>

                  <ProductCarousel 
                    products={recommendations} 
                    onProductClick={onProductClick} 
                  />
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </section>
  );
}
