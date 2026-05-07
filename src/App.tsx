/**
 * @file App.tsx
 * @description 애플리케이션의 전체 레이아웃과 섹션 구성을 정의하는 메인 컴포넌트입니다.
 * 사이트의 전역 테마(배경색, 텍스트 색상)를 설정하고 각 섹션을 순서대로 배치합니다.
 */

import { useState, useEffect } from "react";
import Navigation from "@/sections/Navigation";
import HeroSection from "@/sections/HeroSection";
import PhilosophySection from "@/sections/PhilosophySection";
import ScentGuideSection from "@/sections/ScentGuideSection";
import AIInterviewSection from "@/sections/AIInterviewSection";
import InsightReportSection from "@/sections/InsightReportSection";
import SafetyValuesSection from "@/sections/SafetyValuesSection";
import FooterSection from "@/sections/FooterSection";
import FloatingNavButton from "@/components/common/FloatingNavButton";
import PrivacyConsentModal from "@/components/common/PrivacyConsentModal";

import type { AnalysisResults } from "@/types";

export default function App() {
  // 인터뷰 결과를 저장할 상태
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  
  // 사용자가 선택한 향기 노트들
  const [selectedNotes, setSelectedNotes] = useState<string[]>([]);
  
  // 개인정보 동의 및 세션 상태 관리
  const [hasConsented, setHasConsented] = useState<boolean>(false);

  useEffect(() => {
    // 앱 로드 시 기존 동의 여부 및 세션 확인
    const consented = localStorage.getItem("olfit_consent") === "true";
    const sessionId = localStorage.getItem("olfit_session_id");
    
    if (consented && sessionId) {
      setHasConsented(true);
    }
  }, []);

  const handleAgree = () => {
    // 고유 세션 ID 생성 (UUID v4 유사)
    const newSessionId = crypto.randomUUID();
    
    // 로컬 스토리지 저장
    localStorage.setItem("olfit_consent", "true");
    localStorage.setItem("olfit_session_id", newSessionId);
    
    setHasConsented(true);
  };

  return (
    /**
     * 전체 페이지 컨테이너
     * hasConsented 가 false 일 때 overflow-hidden 을 적용하여 스크롤 차단
     */
    <div className={`min-h-screen bg-cream text-wood font-sans ${!hasConsented ? "overflow-hidden h-screen" : ""}`}>
      {/* 개인정보 동의 모달 (필수) */}
      {!hasConsented && <PrivacyConsentModal onAgree={handleAgree} />}

      {/* 
        메인 콘텐츠 영역 
        동의 전까지 블러 처리 및 상호작용 방지
      */}
      <div className={`transition-all duration-700 ${!hasConsented ? "blur-xl scale-[1.02] pointer-events-none select-none" : "blur-0 scale-100"}`}>
        {/* 상단 네비게이션 바 */}
        <Navigation />
        
        {/* 메인 콘텐츠 영역 */}
        <main>
          {/* 히어로 섹션: 첫 화면 및 인트로 */}
          <HeroSection />
          
          {/* 철학 섹션: 브랜드 가치 및 철학 설명 */}
          <PhilosophySection />
          
          {/* 향기 가이드 섹션: 향수 사용법 및 팁 */}
          <ScentGuideSection onNotesChange={setSelectedNotes} />
          
          {/* AI 인터뷰 섹션: 사용자 취향 분석을 위한 이미지 업로드 및 로직 */}
          <AIInterviewSection 
            onComplete={(results: AnalysisResults) => setAnalysisResults(results)} 
            selectedNotes={selectedNotes}
          />
          
          {/* 분석 리포트 섹션: 인터뷰 결과에 따른 개인화된 분석 결과 */}
          <InsightReportSection results={analysisResults} />
          
          {/* 안전성 섹션: 제품의 원료 및 안전성 강조 */}
          <SafetyValuesSection />
        </main>
        
        {/* 하단 푸터 영역 */}
        <FooterSection />

        {/* 플로팅 내비게이션 버튼 (클릭: 이전 섹션 / 더블클릭: 맨 위로) */}
        <FloatingNavButton />
      </div>
    </div>
  );
}
