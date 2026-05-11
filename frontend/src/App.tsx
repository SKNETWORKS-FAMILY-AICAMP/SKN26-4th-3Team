/**
 * @file App.tsx
 * @description 애플리케이션의 전체 레이아웃과 상태 관리를 담당하는 메인 컴포넌트입니다.
 * 개인정보 동의 프로세스, AI 분석 결과 브릿징, 그리고 각 섹션의 배치를 제어합니다.
 */

import { useOlfitStore } from "@/store/useStore";
import { lazy, Suspense } from "react";
import Navigation from "@/components/layout/Navigation";
import { SectionSkeleton } from "@/components/common/Skeleton";
import ErrorBoundary from "@/components/common/ErrorBoundary";
import FooterSection from "@/components/layout/FooterSection";
import FloatingNavButton from "@/components/common/FloatingNavButton";
import PrivacyConsentModal from "@/components/common/PrivacyConsentModal";
import ProductModal from "@/components/curated/ProductModal";

import type { AnalysisResults } from "@/types";

// 지연 로딩을 위한 섹션 컴포넌트 정의
const HeroSection = lazy(() => import("@/components/sections/HeroSection"));
const PhilosophySection = lazy(() => import("@/components/sections/PhilosophySection"));
const ScentGuideSection = lazy(() => import("@/components/sections/ScentGuideSection"));
const AIInterviewSection = lazy(() => import("@/components/sections/AIInterviewSection"));
const InsightReportSection = lazy(() => import("@/components/sections/InsightReportSection"));
const SafetyValuesSection = lazy(() => import("@/components/sections/SafetyValuesSection"));

export default function App() {
  const { 
    analysisResults, 
    selectedNotes, 
    hasConsented, 
    selectedProduct,
    setAnalysisResults,
    setSelectedNotes,
    setHasConsented,
    setSelectedProduct
  } = useOlfitStore();

  /**
   * 사용자가 개인정보 수집에 동의했을 때 실행되는 핸들러
   */
  const handleAgree = () => {
    // 고유 익명 세션 ID 생성
    const newSessionId = crypto.randomUUID();
    
    // 영속성 유지를 위한 로컬 스토리지 저장
    localStorage.setItem("olfit_consent", "true");
    localStorage.setItem("olfit_session_id", newSessionId);
    
    setHasConsented(true);
  };

  return (
    /**
     * 최상위 컨테이너
     * 미동의 시 스크롤을 원천 차단하여 필수 단계를 강조함
     */
    <div className={`min-h-screen bg-cream text-wood font-sans ${!hasConsented ? "overflow-hidden h-screen" : ""}`}>
      {/* 00. 개인정보 동의 모달 (레이어 최상단) */}
      {!hasConsented && <PrivacyConsentModal onAgree={handleAgree} />}

      {/* 01. 글로벌 네비게이션 헤더 */}
      <Navigation />

      {/* 
        02. 메인 서비스 레이어 
        미동의 시 블러 및 상호작용 방지 효과 적용
      */}
      <div className={`transition-all duration-700 ${!hasConsented ? "blur-xl scale-[1.02] pointer-events-none select-none" : "blur-0"}`}>
        <main>
          {/* 섹션별 독립적 Suspense/ErrorBoundary 배치로 인지 성능 및 안정성 극대화 */}
          <Suspense fallback={<SectionSkeleton />}>
            <ErrorBoundary fallbackMessage="Hero 섹션을 불러오지 못했습니다.">
              <HeroSection />
            </ErrorBoundary>
          </Suspense>

          <Suspense fallback={<SectionSkeleton />}>
            <ErrorBoundary fallbackMessage="철학 섹션을 불러오지 못했습니다.">
              <PhilosophySection />
            </ErrorBoundary>
          </Suspense>

          <Suspense fallback={<SectionSkeleton />}>
            <ErrorBoundary fallbackMessage="가이드 섹션을 불러오지 못했습니다.">
              <ScentGuideSection onNotesChange={setSelectedNotes} />
            </ErrorBoundary>
          </Suspense>
          
          <Suspense fallback={<SectionSkeleton />}>
            <ErrorBoundary fallbackMessage="인터뷰 섹션을 불러오지 못했습니다.">
              <AIInterviewSection 
                onComplete={(results: AnalysisResults) => setAnalysisResults(results)} 
                selectedNotes={selectedNotes}
              />
            </ErrorBoundary>
          </Suspense>
          
          <Suspense fallback={<SectionSkeleton />}>
            <ErrorBoundary fallbackMessage="리포트 섹션을 불러오지 못했습니다.">
              <InsightReportSection 
                results={analysisResults} 
                onProductClick={setSelectedProduct}
              />
            </ErrorBoundary>
          </Suspense>
          
          <Suspense fallback={<SectionSkeleton />}>
            <ErrorBoundary fallbackMessage="안전 가치 섹션을 불러오지 못했습니다.">
              <SafetyValuesSection />
            </ErrorBoundary>
          </Suspense>
        </main>
        
        {/* 글로벌 푸터 */}
        <FooterSection />

        {/* 퀵 내비게이션 플로팅 버튼 */}
        <FloatingNavButton />
      </div>

      {/* 
        03. 개별 제품 상세 레이어 (Portal-like 배치)
        메인 콘텐츠의 블러 필터 영향을 피하기 위해 외부에 독립적으로 배치
      */}
      {selectedProduct && (
        <ProductModal 
          product={selectedProduct} 
          onClose={() => setSelectedProduct(null)} 
        />
      )}
    </div>
  );
}

// EOF: App.tsx
