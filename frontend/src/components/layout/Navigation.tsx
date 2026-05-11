/**
 * @file Navigation.tsx
 * @description 상단 네비게이션 바 컴포넌트입니다.
 * 스크롤 상태에 따른 스타일 변화와 모바일 전용 전체화면 메뉴 기능을 제공합니다.
 */

import { useState, useEffect } from "react";
import { useIsScrolled } from "@/hooks/useIntersectionObserver";
import OlfitLogo from "@/components/common/OlfitLogo";
import { Menu, X } from "lucide-react";

export default function Navigation() {
  /** 일정 거리(80px) 이상 스크롤 여부 */
  const isScrolled = useIsScrolled(80);
  /** 모바일 메뉴 오픈 상태 */
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  /**
   * 모바일 메뉴가 열려있을 때 배경 페이지 스크롤 방지
   */
  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
  }, [isMenuOpen]);

  // 네비게이션 링크 항목
  const navLinks = [
    { label: "컨셉", href: "#philosophy" },
    { label: "향기 가이드", href: "#guide" },
    { label: "AI 인터뷰", href: "#interview" },
    { label: "분석 리포트", href: "#report" },
    { label: "안전성", href: "#safety" },
  ];

  /** 모바일 메뉴 닫기 */
  const closeMenu = () => setIsMenuOpen(false);

  return (
    <>
      <header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
          isScrolled || isMenuOpen
            ? "bg-cream/95 backdrop-blur-sm border-b border-wood/5 h-14 md:h-16"
            : "bg-transparent h-16 md:h-20"
        }`}
      >
        <div className="max-w-[1440px] mx-auto px-6 md:px-8 h-full flex items-center justify-between gap-4">
          {/* 로고 영역 */}
          <div className="flex-shrink-0 z-50">
            <a
              href="#"
              onClick={closeMenu}
              className={`transition-all duration-500 flex items-center ${
                isScrolled || isMenuOpen ? "text-wood" : "text-cream"
              }`}
            >
              <OlfitLogo height={isScrolled ? 24 : 28} showLine={false} />
            </a>
          </div>

          {/* 데스크탑 메뉴 영역 */}
          <nav className="hidden md:flex items-center gap-8 lg:gap-12">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className={`text-[10px] lg:text-[11px] font-medium uppercase tracking-[0.2em] transition-all duration-300 hover:opacity-100 ${
                  isScrolled ? "text-wood/60 hover:text-wood" : "text-cream/60 hover:text-cream"
                }`}
              >
                {link.label}
              </a>
            ))}
          </nav>

          {/* 모바일 메뉴 토글 버튼 */}
          <div className="md:hidden flex items-center z-50">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className={`p-2 transition-colors duration-300 ${
                isScrolled || isMenuOpen ? "text-wood" : "text-cream"
              }`}
              aria-label="Toggle Menu"
            >
              {isMenuOpen ? <X size={24} strokeWidth={1.5} /> : <Menu size={24} strokeWidth={1.5} />}
            </button>
          </div>

          {/* 레이아웃 균형을 위한 더미 공간 */}
          <div className="hidden md:block w-[60px]"></div>
        </div>
      </header>

      {/* 모바일 전체화면 오버레이 메뉴 */}
      <div 
        className={`fixed inset-0 z-40 bg-cream transition-transform duration-500 ease-in-out md:hidden ${
          isMenuOpen ? "translate-y-0" : "-translate-y-full"
        }`}
      >
        <div className="flex flex-col items-center justify-center h-full gap-10 px-6">
          {navLinks.map((link, i) => (
            <a
              key={link.href}
              href={link.href}
              onClick={closeMenu}
              className={`text-2xl font-light uppercase tracking-[0.3em] text-wood transition-all duration-500 delay-${i * 100} ${
                isMenuOpen ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
              }`}
            >
              {link.label}
            </a>
          ))}

          <div className={`mt-10 pt-10 border-t border-wood/10 w-full text-center transition-all duration-700 delay-500 ${
            isMenuOpen ? "opacity-100" : "opacity-0"
          }`}>
            <p className="text-[10px] uppercase tracking-[0.4em] text-wood/30">Your Style Translated into Scent</p>
          </div>
        </div>
      </div>
    </>
  );
}

// EOF: Navigation.tsx