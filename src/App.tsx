/**
 * @file App.tsx
 * @description 애플리케이션의 전체 레이아웃과 상태 관리를 담당하는 메인 컴포넌트입니다.
 * 개인정보 동의 프로세스, AI 분석 결과 브릿징, 그리고 각 섹션의 배치를 제어합니다.
 */

import { useOlfitStore } from "@/store/useStore";
import Navigation from "@/components/layout/Navigation";
import HeroSection from "@/components/sections/HeroSection";
import PhilosophySection from "@/components/sections/PhilosophySection";
import ScentGuideSection from "@/components/sections/ScentGuideSection";
import AIInterviewSection from "@/components/sections/AIInterviewSection";
import InsightReportSection from "@/components/sections/InsightReportSection";
import SafetyValuesSection from "@/components/sections/SafetyValuesSection";
import FooterSection from "@/components/layout/FooterSection";
import FloatingNavButton from "@/components/common/FloatingNavButton";
import PrivacyConsentModal from "@/components/common/PrivacyConsentModal";
import ProductModal from "@/components/curated/ProductModal";

import type { AnalysisResults } from "@/types";

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
          {/* 섹션별 순차 배치 */}
          <HeroSection />
          <PhilosophySection />
          <ScentGuideSection onNotesChange={setSelectedNotes} />
          
          <AIInterviewSection 
            onComplete={(results: AnalysisResults) => setAnalysisResults(results)} 
            selectedNotes={selectedNotes}
          />
          
          <InsightReportSection 
            results={analysisResults} 
            onProductClick={setSelectedProduct}
          />
          
          <SafetyValuesSection />
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
