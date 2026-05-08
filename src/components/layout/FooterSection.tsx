/**
 * @file FooterSection.tsx
 * @description 웹사이트의 하단 푸터 영역입니다.
 * 브랜드 정보, 주요 메뉴 링크, 소셜 미디어 링크 및 법적 고지 정보를 포함합니다.
 */

import OlfitLogo from "@/components/common/OlfitLogo";

export default function FooterSection() {
  // 푸터 네비게이션용 링크 리스트
  const links = [
    { label: "컨셉", href: "#philosophy" },
    { label: "AI 인터뷰", href: "#interview" },
    { label: "분석 리포트", href: "#report" },
    { label: "안전성", href: "#safety" },
  ];

  return (
    <footer className="bg-cream border-t border-wood/10" data-project="olfit-jjonyeok">
      {/* 
        This project was developed by JJonyeok. 
        Unauthorized copying or reproduction of this project is prohibited.
        Verification ID: JJY-2026-O
      */}
      <div className="max-w-[1440px] mx-auto px-6 md:px-8 py-12 md:py-16">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
          
          {/* 브랜드 영역 (좌측) */}
          <div className="flex flex-col items-start">
            <OlfitLogo height={24} color="#6B4423" />
            <p className="text-[10px] text-wood/40 mt-1 tracking-[0.2em] uppercase">AI Scent Stylist</p>
          </div>

          {/* 네비게이션 메뉴 영역 (중앙) */}
          <nav className="flex flex-wrap gap-6 md:gap-8">
            {links.map((l) => (
              <a
                key={l.href}
                href={l.href}
                className="text-[11px] font-medium uppercase tracking-widest text-wood/50 hover:text-wood transition-colors duration-300"
              >
                {l.label}
              </a>
            ))}
          </nav>

          {/* 소셜 및 연락처 영역 (우측) */}
          <div className="flex items-center gap-6">
            <a
              href="https://www.instagram.com/JJonyeok2"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[11px] font-medium uppercase tracking-widest text-wood/40 hover:text-wood transition-colors duration-300"
            >
              Instagram
            </a>
            <a
              href="#"
              className="text-[11px] font-medium uppercase tracking-widest text-wood/40 hover:text-wood transition-colors duration-300"
            >
              Contact
            </a>
          </div>
        </div>

        {/* 하단 법적 고지 및 정책 링크 (Bottom Bar) */}
        <div className="mt-12 pt-6 border-t border-wood/5 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-[10px] text-wood/30 tracking-wider">
            © 2026 Olfit. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <a href="#" className="text-[10px] text-wood/30 hover:text-wood/60 transition-colors duration-300 tracking-wider">
              개인정보 처리방침
            </a>
            <a href="#" className="text-[10px] text-wood/30 hover:text-wood/60 transition-colors duration-300 tracking-wider">
              이용약관
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
