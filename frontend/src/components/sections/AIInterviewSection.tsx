/**
 * @file AIInterviewSection.tsx
 * @description 사용자의 스타일(OOTD) 이미지를 분석하여 맞춤형 향기를 추천하기 위한 인터뷰 섹션입니다.
 */

import { useState, useRef } from "react";
import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { Sparkles, CheckCircle2 } from "lucide-react";
import ImageUploader from "@/components/common/ImageUploader";
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
  
  /**
   * 🛡️ SYNC LOCK: React의 비동기적 상태 업데이트 시차(Latency)를 극복하기 위한 동기식 잠금 레퍼런스입니다.
   * StrictMode 등에서 발생하는 컴포넌트 이중 호출이나, 매우 짧은 간격의 중복 클릭을 물리적으로 차단합니다.
   */
  const processingRef = useRef(false);
  
  const getSteps = () => [
    { threshold: 10, text: "이미지 픽셀 데이터 추출 중..." },
    { threshold: 30, text: "스타일 실루엣 및 텍스처 분석..." },
    { threshold: 50, text: "색채 심리학 기반 무드 매칭..." },
    { threshold: 70, text: "선택된 노트와 스타일 결합 중..." },
    { threshold: 90, text: "최적의 향기 아우라 생성 완료" },
  ];

  const getFinalizingSteps = () => [
    "아우라 분석 결과를 정리하는 중...",
    "추천 향수 데이터를 불러오는 중...",
    "제품 이미지와 상세 정보를 준비하는 중...",
    "리포트 화면을 구성하는 중...",
  ];

  const handleImageProcessed = (base64: string) => {
    /** 
     * [STEP 1] Entry Gate - 물리적 잠금 확인 
     * 이미 프로세스가 진행 중(processingRef)이거나 완료(isComplete)된 경우, 
     * React 상태(isLoading) 반영 여부와 관계없이 즉시 모든 추가 실행을 취소합니다.
     */
    if (processingRef.current || isComplete) return; 
    
    // 즉시 잠금 활성화
    processingRef.current = true;
    setLastProcessedBase64(base64);
    setLoading(true);
    setError(null);
    setProgress(0);
    
    const analysisSteps = getSteps();
    const duration = 5000; // 분석 시뮬레이션 총 소요 시간 (5초)
    const interval = 100;  // 업데이트 주기 (0.1초)
    const stepSize = (interval / duration) * 100;
    
    /**
     * 🛠️ REFACTOR: React 상태와 독립된 로컬 변수로 진행률을 관리합니다.
     * setState 콜백 내부의 사이드 이펙트(API 호출 등)를 외부로 끌어내어 이중 호출을 방지합니다.
     */
    let internalProgress = 0;

    const timer = setInterval(() => {
      internalProgress += stepSize;
      
      // UI 표시를 위한 진행률 및 문구 업데이트
      const currentStep = analysisSteps.find(s => internalProgress <= s.threshold) || analysisSteps[analysisSteps.length - 1];
      setAnalysisStatus(currentStep.text);
      setProgress(Math.min(internalProgress, 100));

      // [STEP 2] Exit Condition - 분석 시뮬레이션 종료 시점에만 1회 호출
      if (internalProgress >= 100) {
        clearInterval(timer);
        setProgress(100);

        const finalizingSteps = getFinalizingSteps();
        let finalizingIndex = 0;
        setAnalysisStatus(finalizingSteps[finalizingIndex]);
        const finalizingTimer = window.setInterval(() => {
          finalizingIndex = (finalizingIndex + 1) % finalizingSteps.length;
          setAnalysisStatus(finalizingSteps[finalizingIndex]);
        }, 1600);
        
        /**
         * 🚀 [CRITICAL FIX]: API 요청은 반드시 setState 콜백 외부에서 실행되어야 합니다.
         * React의 상태 일괄 업데이트(Batching)나 Concurrent 렌더링에 의한 중복 호출을 원천 봉쇄합니다.
         */
        requestAuraAnalysis(base64, selectedNotes)
          .then((realResults) => {
            clearInterval(finalizingTimer);
            setLoading(false);
            setIsComplete(true);
            // 성공 시 락 유지 (중복 전송 방지)
            if (onComplete) {
              onComplete(realResults);
            }
          })
          .catch((err) => {
            clearInterval(finalizingTimer);
            // 에러 발생 시에만 재시도를 위해 락 해제
            setLoading(false);
            processingRef.current = false; 
            setError(err.message || "분석 중 오류가 발생했습니다.");
          });
      }
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
                    
                    <div className="text-cream/70">
                      <p className="text-[11px] uppercase tracking-[0.2em] font-medium">
                        {analysisStatus}
                      </p>
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
