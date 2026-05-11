/**
 * @file FooterSection.tsx
 * @description 웹사이트의 하단 푸터 영역입니다.
 * 브랜드 정보, 주요 메뉴 링크, 소셜 미디어 연결 및 개인정보 처리방침 등의 법적 고지 정보를 포함합니다.
 */

import React, { useState } from "react";
import { createPortal } from "react-dom";
import OlfitLogo from "@/components/common/OlfitLogo";
import { X } from "lucide-react";

export default function FooterSection() {
  /** 모달에 표시될 컨텐츠 상태 */
  const [modalContent, setModalContent] = useState<{ title: string; body: React.ReactNode } | null>(null);

  // 푸터 네비게이션용 링크 리스트
  const links = [
    { label: "컨셉", href: "#philosophy" },
    { label: "AI 인터뷰", href: "#interview" },
    { label: "분석 리포트", href: "#report" },
    { label: "안전성", href: "#safety" },
  ];

  /**
   * 문의처 정보 모달 열기
   */
  const openContact = (e: React.MouseEvent) => {
    e.preventDefault();
    setModalContent({
      title: "Contact Us",
      body: (
        <div className="space-y-4 text-[13px] text-wood/70 leading-relaxed">
          <p>Olfit 서비스에 대한 문의사항이나 제휴 제안은 아래 채널을 통해 연락주세요.</p>
          <div className="pt-4 space-y-2 border-t border-wood/5">
            <p className="flex justify-between"><span>Email</span> <span className="text-wood font-medium">contact@olfit.com</span></p>
            <p className="flex justify-between"><span>Instagram</span> <span className="text-wood font-medium">@olfit_official</span></p>
            <p className="flex justify-between"><span>CS Center</span> <span className="text-wood font-medium">1544-XXXX (평일 10:00 - 18:00)</span></p>
          </div>
          <p className="text-[11px] text-wood/40 mt-4 italic">* 통상 24시간 이내에 답변을 드립니다.</p>
        </div>
      )
    });
  };

  /**
   * 개인정보 처리방침 모달 열기
   */
  const openPrivacy = (e: React.MouseEvent) => {
    e.preventDefault();
    setModalContent({
      title: "Privacy Policy",
      body: (
        <div className="space-y-4 text-[12px] text-wood/70 leading-relaxed max-h-[40vh] overflow-y-auto pr-2 scrollbar-thin">
          <p className="font-medium text-wood text-[13px]">1. 수집하는 개인정보 항목</p>
          <p>Olfit은 AI 분석을 위해 업로드된 이미지, 선호 노트 정보, 그리고 서비스 이용 기록을 수집합니다.</p>
          <p className="font-medium text-wood text-[13px]">2. 개인정보의 이용 목적</p>
          <p>수집된 정보는 오직 개인화된 향기 추천 리포트 생성 및 서비스 품질 개선을 위한 통계적 분석 용도로만 사용됩니다.</p>
          <p className="font-medium text-wood text-[13px]">3. 정보의 보유 및 파기</p>
          <p>분석에 사용된 이미지는 리포트 생성 즉시 암호화 처리되며, 일정 기간 경과 후 안전하게 파기됩니다.</p>
          <p className="pt-4 border-t border-wood/5 text-[10px] text-wood/40">상세한 내용은 정식 서비스 배포 시 관련 법령에 따라 업데이트될 예정입니다.</p>
        </div>
      )
    });
  };

  /**
   * 이용약관 모달 열기
   */
  const openTerms = (e: React.MouseEvent) => {
    e.preventDefault();
    setModalContent({
      title: "Terms of Service",
      body: (
        <div className="space-y-4 text-[12px] text-wood/70 leading-relaxed max-h-[40vh] overflow-y-auto pr-2 scrollbar-thin">
          <p className="font-medium text-wood text-[13px]">1. 서비스의 목적</p>
          <p>Olfit은 AI 기술을 활용하여 사용자에게 최적화된 향기 제품을 추천하고 가이드를 제공하는 큐레이션 서비스입니다.</p>
          <p className="font-medium text-wood text-[13px]">2. 분석 결과의 소유권</p>
          <p>생성된 향기 아우라 리포트 및 이미지는 사용자의 개인적 용도로만 사용 가능하며, 상업적 목적으로의 무단 배포를 금합니다.</p>
          <p className="font-medium text-wood text-[13px]">3. 면책 조항</p>
          <p>추천 결과는 AI의 주관적 분석에 근거하며, 실제 제품의 향기 체감은 개인마다 다를 수 있음을 고지합니다.</p>
          <p className="pt-4 border-t border-wood/5 text-[10px] text-wood/40">본 약관은 추후 서비스 운영 정책에 따라 변경될 수 있습니다.</p>
        </div>
      )
    });
  };

  return (
    <footer className="bg-cream border-t border-wood/10" data-project="olfit-jjonyeok">
      <div className="max-w-[1440px] mx-auto px-6 md:px-8 py-12 md:py-16">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8">

          {/* 브랜드 영역 (좌측) */}
          <div className="flex flex-col items-start">
            <OlfitLogo height={24} color="#6B4423" showLine={false} />
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
            <button
              onClick={openContact}
              className="text-[11px] font-medium uppercase tracking-widest text-wood/40 hover:text-wood transition-colors duration-300"
            >
              Contact
            </button>
          </div>
        </div>

        {/* 하단 법적 고지 및 정책 링크 (Bottom Bar) */}
        <div className="mt-12 pt-6 border-t border-wood/5 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-[10px] text-wood/30 tracking-wider">
            © 2026 Olfit. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <button 
              onClick={openPrivacy}
              className="text-[10px] text-wood/30 hover:text-wood/60 transition-colors duration-300 tracking-wider"
            >
              개인정보 처리방침
            </button>
            <button 
              onClick={openTerms}
              className="text-[10px] text-wood/30 hover:text-wood/60 transition-colors duration-300 tracking-wider"
            >
              이용약관
            </button>
          </div>
        </div>
      </div>

      {/* 푸터 전용 미니 모달 오버레이 - React Portal 적용 */}
      {modalContent && createPortal(
        <div 
          className="fixed inset-0 z-[10000] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
          onClick={() => setModalContent(null)}
          style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh' }}
        >
          <div 
            className="relative bg-white border border-wood/20 p-8 md:p-12 w-full max-w-lg shadow-2xl rounded-sm"
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              onClick={() => setModalContent(null)}
              className="absolute top-4 right-4 p-2 text-wood/40 hover:text-wood transition-colors"
              aria-label="Close"
            >
              <X size={24} />
            </button>

            <h3 className="text-xl md:text-2xl font-light tracking-tight text-wood mb-6 uppercase" style={{ fontFamily: "'Playfair Display', serif" }}>
              {modalContent.title}
            </h3>

            <div className="text-wood">
              {modalContent.body}
            </div>

            <button
              onClick={() => setModalContent(null)}
              className="w-full mt-8 py-4 bg-wood text-cream text-[11px] uppercase tracking-[0.2em] font-medium hover:bg-wood/90 transition-all active:scale-[0.98]"
            >
              Close
            </button>
          </div>
        </div>,
        document.body
      )}
    </footer>
  );
}

// EOF: FooterSection.tsx

