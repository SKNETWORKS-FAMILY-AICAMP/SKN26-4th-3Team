/**
 * @file OlfitLogo.tsx
 * @description Olfit 브랜드의 SVG 로고 컴포넌트입니다.
 * 벡터 포맷을 사용하여 어떠한 해상도에서도 선명하게 렌더링됩니다.
 */

import React from 'react';

interface OlfitLogoProps {
  className?: string;
  width?: number | string;
  height?: number | string;
  color?: string;
}

export default function OlfitLogo({ 
  className, 
  width = "auto", 
  height = "1.2em", 
  color = "currentColor" 
}: OlfitLogoProps) {
  return (
    <svg 
      width={width} 
      height={height} 
      viewBox="0 0 120 40" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <text
        x="50%"
        y="55%"
        dominantBaseline="middle"
        textAnchor="middle"
        fill={color}
        style={{ 
          fontFamily: "serif", 
          fontWeight: 300, 
          fontSize: "24px", 
          letterSpacing: "0.25em",
          textTransform: "uppercase"
        }}
      >
        Olfit
      </text>
      {/* 단순 텍스트를 넘어선 로고 느낌을 위한 데코레이션 라인 */}
      <path 
        d="M20 32 H100" 
        stroke={color} 
        strokeWidth="0.5" 
        strokeOpacity="0.3" 
      />
    </svg>
  );
}
