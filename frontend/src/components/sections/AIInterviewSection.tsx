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
import { requestAuraAnalysis } from "@/services/api";
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

  const handleImageProcessed = (base64: string) => {
    if (isLoading) return; // 🚨 FIX: POST 중복 요청 방지
    
    setLastProcessedBase64(base64);
    setLoading(true);
    setError(null);
    setProgress(0);
    
    const analysisSteps = getSteps();
    const duration = 5000; // 시뮬레이션 5초
    const interval = 100;
    const step = (interval / duration) * 100;

    const timer = setInterval(async () => {
      setProgress((prev) => {
        const next = prev + step;
        const currentStep = analysisSteps.find(s => next <= s.threshold) || analysisSteps[analysisSteps.length - 1];
        setAnalysisStatus(currentStep.text);

        if (next >= 100) {
          clearInterval(timer);
          
          // 실제 백엔드 분석 요청
          requestAuraAnalysis(base64, selectedNotes)
            .then((realResults) => {
              setLoading(false);
              setIsComplete(true);
              if (onComplete) {
                onComplete(realResults);
              }
            })
            .catch((err) => {
              setLoading(false);
              setError(err.message || "분석 중 오류가 발생했습니다.");
            });
            
          return 100;
        }
        return next;
      });
    }, interval);
  };

  const handleRetry = (e?: React.MouseEvent) => {
    if (e) {
      e.preventDefault(); // 🚨 FIX: POST 중복 요청 방지
      e.stopPropagation(); // 🚨 FIX: POST 중복 요청 방지
    }
    // 🛠️ REFACTOR (UX 안정성): 재시도 시 사용자에게 시각적 피드백 제공
    setError(null);
    if (lastProcessedBase64) {
      handleImageProcessed(lastProcessedBase64);
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
              // 🛠️ REFACTOR (UX 안정성): ErrorFallback에 구체적인 가이드 메시지 전달
              <ErrorFallback 
                message={`${error} \n서버 연결이 원활하지 않을 수 있습니다. 잠시 후 다시 시도해 주세요.`} 
                onRetry={handleRetry} 
              />
            ) : !isComplete ? (
              <div className="relative">
                <ImageUploader onImageProcessed={handleImageProcessed} isAnalyzing={isLoading} />
                {isLoading && (
                  <div className="mt-12 space-y-10 animate-in fade-in duration-700">
                    {/* 🛠️ REFACTOR (UX 안정성): 투박한 프로그레스 바 대신 우아한 스켈레톤 UI와 진행 상태 결합 */}
                    <div className="space-y-4">
                      <div className="flex justify-between items-end mb-2">
                        <span className="text-[11px] uppercase tracking-[0.3em] text-cream/30 font-bold">Analysis in progress</span>
                        <span className="text-[10px] font-mono text-cream/60">{Math.round(progress)}%</span>
                      </div>
                      <div className="h-[2px] bg-cream/5 w-full relative overflow-hidden">
                        <div 
                          className="absolute inset-y-0 left-0 bg-cream/40 transition-all duration-300 ease-out shadow-[0_0_8px_rgba(253,252,240,0.3)]" 
                          style={{ width: `${progress}%` }} 
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 gap-6">
                      <div className="p-8 border border-cream/5 bg-white/[0.02] rounded-sm backdrop-blur-sm relative overflow-hidden">
                        <div className="flex items-center gap-4">
                          <LoadingSpinner className="p-0 gap-3 flex-row" message={analysisStatus} />
                        </div>
                        {/* 🛠️ REFACTOR (UX 안정성): 로딩 중 컨텐츠의 뼈대를 보여주는 스켈레톤 펄스 효과 */}
                        <div className="mt-8 space-y-3 opacity-20">
                          <div className="h-3 bg-cream/40 rounded-full w-3/4 animate-pulse" />
                          <div className="h-3 bg-cream/40 rounded-full w-1/2 animate-pulse" />
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center py-12 animate-in fade-in zoom-in duration-1000">
                <div className="w-20 h-20 rounded-full bg-cream/10 flex items-center justify-center mb-8 border border-cream/20">
                  <CheckCircle2 className="text-cream w-10 h-10" strokeWidth={1} />
                </div>
                <a 
                  href="#report" 
                  onClick={(e) => { e.stopPropagation(); }} // 🚨 FIX: POST 중복 요청 방지
                  className="group flex items-center gap-3 bg-cream text-wood px-10 py-4 text-[12px] font-medium uppercase tracking-[0.2em] transition-all duration-300 hover:bg-white active:scale-95"
                >
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
