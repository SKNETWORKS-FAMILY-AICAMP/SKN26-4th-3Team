/**
 * @file useInsightReport.ts
 * @description InsightReportSection의 비즈니스 로직과 상태 관리를 담당하는 커스텀 훅입니다.
 */

import { useState, useMemo, useRef } from "react";
import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { scentNotes } from "@/data/noteData";
import { radarData } from "@/data/reportData";
import { getRecommendedProducts } from "@/services/recommendationEngine";
import { captureReportBlob, shareOrDownloadImage } from "@/services/reportCapture";
import type { AnalysisResults } from "@/types";

const fallbackRadarAdjustments = [0.06, 0.03, 0.08, 0.05, 0.02];

export function useInsightReport(results: AnalysisResults | null) {
  // 🛠️ REFACTOR (유지보수성): 교차 관찰자 상태 분리
  const { ref: refHeader, isVisible: visHeader } = useIntersectionObserver();
  const { ref: refRadar, isVisible: visRadar } = useIntersectionObserver();
  const { ref: refSteps, isVisible: visSteps } = useIntersectionObserver();
  const { ref: refPyramid, isVisible: visPyramid } = useIntersectionObserver();
  
  const reportRef = useRef<HTMLDivElement>(null);
  const isCapturingRef = useRef(false);

  const [sortBy, setSortBy] = useState<"recommended" | "price">("recommended");
  const [isSaving, setIsSaving] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  // 🛠️ REFACTOR (유지보수성): 추천 제품 매칭 로직 분리
  const baseRecommendations = useMemo(() => {
    if (results?.recommendations && results.recommendations.length > 0) {
      return results.recommendations;
    }
    return getRecommendedProducts(results);
  }, [results]);

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

  const dynamicLogicSteps = useMemo(() => [
    `업로드된 이미지에서 추출된 ${results?.personalMood || "#현대적 #시크"} 무드 분석`,
    results?.analysisMetadata?.selectedNotes && results.analysisMetadata.selectedNotes.filter(Boolean).length > 0
      ? `사용자가 선택한 원료(${results.analysisMetadata.selectedNotes.filter(Boolean).join(", ")})와의 조화 계산`
      : "이미지의 색채 심리학적 데이터 기반 향기 맵 생성",
    `최적의 향기 아우라 매칭: ${recommendations[0]?.name || "분석 중"}`,
    "시각적 무드와 후각적 취향의 완벽한 밸런스 완성",
  ], [results, recommendations]);

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

  const handleShareResults = async (e?: React.MouseEvent) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
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

  return {
    observers: { refHeader, visHeader, refRadar, visRadar, refSteps, visSteps, refPyramid, visPyramid },
    reportRef,
    state: { sortBy, isSaving, feedback },
    derived: { recommendations, slots, matchPercent, dynamicLogicSteps, currentRadarData },
    actions: { setSortBy, handleShareResults }
  };
}
