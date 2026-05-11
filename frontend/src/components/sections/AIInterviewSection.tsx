/**
 * @file AIInterviewSection.tsx
 * @description 사용자의 스타일(OOTD) 이미지를 분석하여 맞춤형 향기를 추천하기 위한 인터뷰 섹션입니다.
 */

import { useState } from "react";
import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { Sparkles, CheckCircle2 } from "lucide-react";
import ImageUploader from "@/components/common/ImageUploader";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import ErrorFallback from "@/components/common/ErrorFallback";
import { useOlfitStore } from "@/store/useStore";
import type { AnalysisResults } from "@/types";

interface AIInterviewSectionProps {
  onComplete?: (results: AnalysisResults) => void;
  selectedNotes?: string[];
}

export default function AIInterviewSection({ onComplete, selectedNotes = [] }: AIInterviewSectionProps) {
  const { ref, isVisible } = useIntersectionObserver();
  const { isLoading, error, setLoading, setError } = useOlfitStore();
  const [isComplete, setIsComplete] = useState(false);
  const [analysisStatus, setAnalysisStatus] = useState("");
  const [progress, setProgress] = useState(0);
  const [lastProcessedBase64, setLastProcessedBase64] = useState<string | null>(null);
  
  const getSteps = () => [
    { threshold: 10, text: "이미지 픽셀 데이터 추출 중..." },
    { threshold: 30, text: "스타일 실루엣 및 텍스처 분석..." },
    { threshold: 50, text: "색채 심리학 기반 무드 매칭..." },
    { threshold: 70, text: "선택된 노트와 스타일 결합 중..." },
    { threshold: 90, text: "최적의 향기 아우라 생성 완료" },
  ];

  const handleImageProcessed = async (base64: string, remoteUrl: string) => {
    setLastProcessedBase64(base64);
    setLoading(true);
    setError(null);
    setProgress(0);

    const analysisSteps = getSteps();
    const duration = 5000; 
    const interval = 100;
    const step = (interval / duration) * 100;

    // 시각적인 프로그레스 바 업데이트
    const progressTimer = setInterval(() => {
      setProgress((prev) => {
        const next = prev + step;
        const currentStep = analysisSteps.find(s => next <= s.threshold) || analysisSteps[analysisSteps.length - 1];
        setAnalysisStatus(currentStep.text);
        return next >= 95 ? 95 : next; // API 응답 전까지는 95%에서 대기
      });
    }, interval);

    try {
      const { requestAuraAnalysis } = await import("@/services/api");
      const results = await requestAuraAnalysis(base64, selectedNotes);

      clearInterval(progressTimer);
      setProgress(100);
      setAnalysisStatus("최적의 향기 아우라 생성 완료");

      setTimeout(() => {
        setLoading(false);
        setIsComplete(true);
        if (onComplete) {
          onComplete(results);
          console.log("Analysis completed with backend results:", results);
        }
      }, 500);

    } catch (err: any) {
      clearInterval(progressTimer);
      setLoading(false);
      setError(err.message || "분석 중 오류가 발생했습니다.");
    }
  };


  const handleRetry = () => {
    if (lastProcessedBase64) {
      handleImageProcessed(lastProcessedBase64, "retry-mock-url");
    }
  };

  return (
    <section id="interview" className="bg-wood text-cream py-24 md:py-40">
      <div className="max-w-[1440px] mx-auto px-6 md:px-8">
        <div ref={ref} className={`transition-all duration-800 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <div className="text-center mb-16">
            <p className="label-upper text-cream/40 mb-4">AI Visual Analysis</p>
            <h2 className="text-2xl sm:text-4xl md:text-5xl font-light tracking-tight break-keep text-cream" style={{ fontFamily: "'Playfair Display', serif" }}>
              {isComplete ? "분석이 완료되었습니다" : "당신의 스타일을 보여주세요"}
            </h2>
          </div>

          <div className="max-w-2xl mx-auto">
            {error ? (
              <ErrorFallback message={error} onRetry={handleRetry} />
            ) : !isComplete ? (
              <div className="relative">
                <ImageUploader onImageProcessed={handleImageProcessed} isAnalyzing={isLoading} />
                {isLoading && (
                  <div className="mt-12 space-y-6">
                    <div className="h-px bg-cream/10 w-full relative overflow-hidden">
                      <div className="absolute inset-y-0 left-0 bg-cream transition-all duration-300 ease-out" style={{ width: `${progress}%` }} />
                    </div>
                    <div className="flex justify-between items-center">
                      <div className="flex items-center gap-3">
                        <LoadingSpinner className="p-0 gap-2 flex-row" message={analysisStatus} />
                      </div>
                      <span className="text-[11px] font-mono text-cream/40">{Math.round(progress)}%</span>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center py-12 animate-in fade-in zoom-in duration-1000">
                <div className="w-20 h-20 rounded-full bg-cream/10 flex items-center justify-center mb-8 border border-cream/20">
                  <CheckCircle2 className="text-cream w-10 h-10" strokeWidth={1} />
                </div>
                <a href="#report" className="group flex items-center gap-3 bg-cream text-wood px-10 py-4 text-[12px] font-medium uppercase tracking-[0.2em] transition-all duration-300 hover:bg-white active:scale-95">
                  View Insight Report <Sparkles size={16} className="group-hover:rotate-12 transition-transform" />
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
