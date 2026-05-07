/**
 * @file Navigation.tsx
 * @description 상단 네비게이션 바 컴포넌트입니다.
 * 메뉴 항목을 헤더에 직접 노출하여 직관적이고 안정적인 탐색을 제공합니다.
 */

import { useIsScrolled } from "@/hooks/useIntersectionObserver";

export default function Navigation() {
  const isScrolled = useIsScrolled(80);

  const navLinks = [
    { label: "컨셉", href: "#philosophy" },
    { label: "향기 가이드", href: "#guide" },
    { label: "AI 인터뷰", href: "#interview" },
    { label: "분석 리포트", href: "#report" },
    { label: "안전성", href: "#safety" },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        isScrolled
          ? "bg-cream/95 backdrop-blur-sm border-b border-wood/5 h-14 md:h-16"
          : "bg-transparent h-16 md:h-20"
      }`}
    >
      <div className="max-w-[1440px] mx-auto px-6 md:px-8 h-full flex items-center justify-between gap-4">
        {/* 왼쪽 영역: 로고 */}
        <div className="flex-shrink-0">
          <a
            href="#"
            className={`text-base md:text-lg font-light tracking-[0.3em] uppercase transition-all duration-500 ${
              isScrolled ? "text-wood" : "text-cream"
            }`}
          >
            Olfit
          </a>
        </div>

        {/* 중앙 영역: 네비게이션 링크 */}
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

        {/* 오른쪽 영역: 모바일 대응 또는 여백 */}
        <div className="md:hidden flex overflow-x-auto no-scrollbar gap-5 max-w-[200px]">
          {navLinks.slice(0, 3).map((link) => (
            <a
              key={link.href}
              href={link.href}
              className={`text-[9px] font-medium uppercase tracking-widest whitespace-nowrap ${
                isScrolled ? "text-wood/70" : "text-cream/70"
              }`}
            >
              {link.label}
            </a>
          ))}
        </div>
        
        {/* 데스크탑 우측 여백 비율용 (좌측 로고와 균형) */}
        <div className="hidden md:block w-[60px]"></div>
      </div>
    </header>
  );
}