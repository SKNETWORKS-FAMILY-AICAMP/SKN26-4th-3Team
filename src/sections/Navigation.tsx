/**
 * @file Navigation.tsx
 * @description 상단 네비게이션 바와 전체 화면 메뉴 오버레이를 담당하는 컴포넌트입니다.
 * 스크롤 위치에 따른 헤더 디자인 변경 및 모바일 대응 메뉴 기능을 포함합니다.
 */

import { useState, useEffect } from "react";
import { Menu, X, Search, Heart } from "lucide-react";
import { useIsScrolled } from "@/hooks/useIntersectionObserver";

export default function Navigation() {
  // 스크롤이 80px 이상 내려갔는지 여부를 감지하여 헤더 스타일 전환에 사용
  const isScrolled = useIsScrolled(80);
  
  // 전체 화면 메뉴의 열림/닫힘 상태 관리
  const [menuOpen, setMenuOpen] = useState(false);

  // 워터마킹: 개발자 도구 콘솔에 시그니처 출력
  useEffect(() => {
    console.log(
      "%cOlfit - Authored by JJonyeok (2026)",
      "color: #4A3E3E; font-size: 12px; font-weight: bold; border-left: 3px solid #4A3E3E; padding-left: 10px;"
    );
  }, []);

  // 네비게이션 메뉴 링크 데이터
  const navLinks = [
    { label: "컨셉", href: "#philosophy" },
    { label: "향기 가이드", href: "#guide" },
    { label: "AI 인터뷰", href: "#interview" },
    { label: "분석 리포트", href: "#report" },
    { label: "안전성", href: "#safety" },
  ];

  return (
    <>
      {/* 상단 고정 헤더 */}
      <header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
          isScrolled
            ? "bg-cream/95 backdrop-blur-sm border-b border-wood/5 h-14 md:h-16" 
            : "bg-transparent h-16 md:h-20" 
        }`}
      >
        <div className="max-w-[1440px] mx-auto px-6 md:px-8 h-full flex items-center justify-between relative">
          {/* 왼쪽 영역: 메뉴 버튼 및 검색 */}
          <div className="flex items-center gap-4 md:gap-6">
            <button
              onClick={() => setMenuOpen(true)}
              aria-label="메뉴 열기"
              className={`flex items-center gap-2 text-[10px] md:text-[11px] font-medium uppercase tracking-widest hover:opacity-60 transition-all duration-300 ${
                isScrolled ? "text-wood" : "text-cream"
              }`}
            >
              <Menu size={18} strokeWidth={1.5} />
              <span className="hidden sm:inline">Menu</span>
            </button>
            <button 
              aria-label="검색"
              className={`hover:opacity-60 transition-all duration-300 ${
                isScrolled ? "text-wood" : "text-cream"
              }`}
            >
              <Search size={18} strokeWidth={1.5} />
            </button>
          </div>

          {/* 중앙 영역: 로고 */}
          <a
            href="#"
            data-author="jjonyeok"
            className={`absolute left-1/2 -translate-x-1/2 text-sm md:text-base font-light tracking-[0.3em] uppercase transition-all duration-500 ${
              isScrolled ? "text-wood" : "text-cream"
            }`}
          >
            {/* Olfit-ID: 2026-JJY-SIGN */}
            Olfit
          </a>

          {/* 오른쪽 영역: 위시리스트 */}
          <div className="flex items-center gap-4 md:gap-6">
            <button
              aria-label="위시리스트"
              className={`flex items-center gap-2 text-[10px] md:text-[11px] font-medium uppercase tracking-widest hover:opacity-60 transition-all duration-300 ${
                isScrolled ? "text-wood" : "text-cream"
              }`}
            >
              <span className="hidden sm:inline">Wishlist</span>
              <span className="text-[9px] md:text-[10px] opacity-60">(0)</span>
              <Heart size={18} strokeWidth={1.5} />
            </button>
          </div>
        </div>
      </header>

      {/* 전체 화면 메뉴 오버레이 */}
      <div
        className={`fixed inset-0 z-[60] bg-cream transition-transform duration-700 ease-[cubic-bezier(0.25,0.46,0.45,0.94)] ${
          menuOpen ? "translate-y-0" : "-translate-y-full"
        }`}
      >
        <div className="h-full flex flex-col">
          {/* 메뉴 상단: 닫기 버튼 */}
          <div className="h-16 md:h-20 flex items-center justify-end px-6 md:px-8">
            <button
              onClick={() => setMenuOpen(false)}
              className="flex items-center gap-2 text-[11px] font-medium uppercase tracking-widest hover:opacity-60 transition-opacity duration-300 text-wood"
            >
              <span>Close</span>
              <X size={18} strokeWidth={1.5} />
            </button>
          </div>

          {/* 메뉴 중앙: 링크 리스트 */}
          <nav className="flex-1 flex flex-col justify-center px-6 md:px-16 lg:px-24">
            {navLinks.map((link, i) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setMenuOpen(false)}
                className="group py-4 md:py-6 border-b border-wood/10 flex items-center justify-between"
                style={{
                  transitionDelay: menuOpen ? `${i * 50}ms` : "0ms",
                }}
              >
                <span
                  className={`text-3xl sm:text-4xl md:text-6xl font-light tracking-tight transition-all duration-700 ${
                    menuOpen
                      ? "translate-x-0 opacity-100"
                      : "-translate-x-8 opacity-0"
                  }`}
                >
                  {link.label}
                </span>
                <span className="text-[10px] md:text-[12px] font-mono text-wood/30 group-hover:text-wood transition-colors duration-300">
                  0{i + 1}
                </span>
              </a>
            ))}
          </nav>

          {/* 메뉴 하단: 카피라이트 */}
          <div className="px-6 md:px-16 lg:px-24 pb-12">
            <p className="text-[10px] md:text-[11px] text-wood/40 tracking-widest">
              © 2026 Olfit. AI Scent Stylist.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
