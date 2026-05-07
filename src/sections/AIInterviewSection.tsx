/**
 * @file AIInterviewSection.tsx
 * @description 사용자의 취향을 분석하기 위한 AI 채팅 인터뷰 섹션입니다.
 */

import { useState, useRef, useEffect } from "react";
import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { Sparkles, Camera, Loader2, CheckCircle2 } from "lucide-react";
import ImageUploader from "@/components/common/ImageUploader";
import type { AnalysisResults } from "@/types";

interface AIInterviewSectionProps {
  onComplete?: (results: AnalysisResults) => void;
  selectedNotes?: string[]; // NoteGlossary 에서 선택된 노트들
}

export default function AIInterviewSection({ onComplete, selectedNotes = [] }: AIInterviewSectionProps) {
  const { ref, isVisible } = useIntersectionObserver();
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [analysisStatus, setAnalysisStatus] = useState("");
  const [progress, setProgress] = useState(0);
  
  // 분석 단계 시나리오 (30초 동안 순차적 노출)
  const steps = [
    { threshold: 10, text: "이미지 픽셀 데이터 추출 중..." },
    { threshold: 30, text: "스타일 실루엣 및 텍스처 분석..." },
    { threshold: 50, text: "색채 심리학 기반 무드 매칭..." },
    { threshold: 70, text: "선택하신 향기 노트와 스타일 결합 중..." },
    { threshold: 90, text: "최적의 향기 아우라 생성 완료" },
  ];

  /**
   * 이미지 처리 핸들러 (30초 시뮬레이션)
   */
  const handleImageProcessed = (base64: string) => {
    setIsAnalyzing(true);
    setProgress(0);
    
    // 30초 동안 프로그레스 바 및 상태 업데이트
    const duration = 30000; // 30 seconds
    const interval = 100;
    const step = (interval / duration) * 100;

    const timer = setInterval(() => {
      setProgress((prev) => {
        const next = prev + step;
        
        // 현재 퍼센트에 맞는 텍스트 업데이트
        const currentStep = steps.find(s => next <= s.threshold) || steps[steps.length - 1];
        setAnalysisStatus(currentStep.text);

        if (next >= 100) {
          clearInterval(timer);
          setIsAnalyzing(false);
          setIsComplete(true);
          
          if (onComplete) {
            onComplete({ 
              type: "personal", 
              personalMood: "이미지 분석 기반 무드", 
              fashionStyle: "이미지 분석 기반 스타일",
              // 선택된 이미지와 노트를 기반으로 한 분석 결과임을 명시
              analysisMetadata: {
                base64Image: base64,
                selectedNotes: selectedNotes
              }
            });
          }
          return 100;
        }
        return next;
      });
    }, interval);
  };

  return (
    <section id="interview" className="bg-wood text-cream py-24 md:py-40">
      <div className="max-w-[1440px] mx-auto px-6 md:px-8">
        <div ref={ref} className={`transition-all duration-800 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <div className="text-center mb-16">
            <p className="label-upper text-cream/40 mb-4">AI Visual Analysis</p>
            <h2 className="text-2xl sm:text-4xl md:text-5xl font-light tracking-tight break-keep text-cream">
              {isComplete ? "분석이 완료되었습니다" : "당신의 스타일을 보여주세요"}
            </h2>
            <p className="mt-6 text-cream/40 text-[13px] max-w-xl mx-auto break-keep">
              업로드하신 사진과 선택하신 원료를 기반으로 Olfit AI가 <br className="hidden sm:inline" /> 
              당신만의 고유한 향기 아우라를 정교하게 분석합니다.
            </p>
          </div>

          <div className="max-w-2xl mx-auto">
            {!isComplete ? (
              <div className="relative">
                <ImageUploader onImageProcessed={handleImageProcessed} isAnalyzing={isAnalyzing} />
                
                {isAnalyzing && (
                  <div className="mt-12 space-y-6">
                    <div className="h-px bg-cream/10 w-full relative overflow-hidden">
                      <div 
                        className="absolute inset-y-0 left-0 bg-cream transition-all duration-300 ease-out"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                    <div className="flex justify-between items-center">
                      <p className="text-[11px] uppercase tracking-[0.2em] text-cream/60 flex items-center gap-2">
                        <Loader2 size={12} className="animate-spin" />
                        {analysisStatus}
                      </p>
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
                <p className="text-lg font-light mb-10 text-center break-keep">
                  스타일 분석과 향기 노트의 매칭이 성공적으로 끝났습니다.<br />
                  이제 당신을 위한 단 하나의 리포트를 확인해 보세요.
                </p>
                <a
                  href="#report"
                  className="group flex items-center gap-3 bg-cream text-wood px-10 py-4 text-[12px] font-medium uppercase tracking-[0.2em] transition-all duration-300 hover:bg-white active:scale-95"
                >
                  View Insight Report
                  <Sparkles size={16} className="group-hover:rotate-12 transition-transform" />
                </a>
                <button 
                  onClick={() => setIsComplete(false)}
                  className="mt-8 text-[10px] uppercase tracking-widest text-cream/30 hover:text-cream transition-colors"
                >
                  다른 사진으로 다시 분석하기
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
