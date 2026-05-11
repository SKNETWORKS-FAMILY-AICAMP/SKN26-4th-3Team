/**
 * @file FloatingNavButton.tsx
 * @description 페이지 탐색을 돕는 플로팅 버튼 컴포넌트입니다.
 * 단일 클릭 시 이전 섹션으로, 더블 클릭 시 최상단으로 이동하는 하이브리드 기능을 제공합니다.
 */

import { useState, useEffect, useRef } from "react";
import { ArrowUp } from "lucide-react";

export default function FloatingNavButton() {
  const [isVisible, setIsVisible] = useState(false);
  const [isAtFooter, setIsAtFooter] = useState(false);
  const clickTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  /**
   * 스크롤 위치 감지 및 UI 상태 업데이트
   */
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;

      // 1. 일정 거리(300px) 이상 스크롤 시 버튼 노출
      setIsVisible(scrollY > 300);

      // 2. 푸터 영역 도달 시 버튼 위치를 위로 밀어올림 (레이아웃 겹침 방지)
      const distanceFromBottom = documentHeight - (scrollY + windowHeight);
      setIsAtFooter(distanceFromBottom < 120);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  /**
   * 이전 섹션(현재 위치보다 위쪽의 가장 가까운 <section>)으로 스무스 스크롤
   */
  const scrollToPreviousSection = () => {
    const sections = Array.from(document.querySelectorAll("main > section"));
    const currentScroll = window.scrollY;
    
    const prevSection = [...sections]
      .reverse()
      .find((section) => {
        const rect = section.getBoundingClientRect();
        const absoluteTop = rect.top + window.scrollY;
        // 현재 위치보다 최소 100px 위에 있는 섹션을 타겟팅
        return absoluteTop < currentScroll - 100;
      });

    if (prevSection) {
      prevSection.scrollIntoView({ behavior: "smooth" });
    } else {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  /**
   * 페이지 최상단으로 즉시 스무스 스크롤
   */
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  /**
   * 클릭 이벤트 처리 (단일/더블 클릭 분기)
   */
  const handleClick = () => {
    if (clickTimeoutRef.current) {
      // 250ms 내 재발생 시 더블 클릭으로 간주
      clearTimeout(clickTimeoutRef.current);
      clickTimeoutRef.current = null;
      scrollToTop();
    } else {
      // 단일 클릭 타이머 설정
      clickTimeoutRef.current = setTimeout(() => {
        scrollToPreviousSection();
        clickTimeoutRef.current = null;
      }, 250);
    }
  };

  return (
    <button
      onClick={handleClick}
      className={`fixed right-6 sm:right-8 z-40 w-12 h-12 rounded-full bg-wood text-cream shadow-editorial flex items-center justify-center transition-all duration-500 hover:scale-110 active:scale-95 group ${
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10 pointer-events-none"
      } ${
        isAtFooter ? "bottom-16 sm:bottom-20" : "bottom-8 sm:bottom-10"
      }`}
      aria-label="Navigate upwards"
    >
      <div className="relative">
        <ArrowUp 
          size={20} 
          strokeWidth={2.5} 
          className="transition-transform duration-300 group-hover:-translate-y-1"
        />
      </div>
      
      {/* 사용자 가이드 툴팁 */}
      <div className="absolute right-full mr-4 px-3 py-1.5 bg-wood text-cream text-[10px] whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none rounded tracking-wider">
        CLICK: PREV / DBL CLICK: TOP
      </div>
    </button>
  );
}

// EOF: FloatingNavButton.tsx
