/**
 * @file OlfitLogo.tsx
 * @description Olfit 브랜드의 SVG 로고 컴포넌트입니다.
 * 벡터 포맷을 사용하여 어떠한 해상도에서도 선명하게 렌더링되며, 프로젝트 전역에서 브랜딩 요소로 사용됩니다.
 */

interface OlfitLogoProps {
  /** 추가적인 CSS 클래스 */
  className?: string;
  /** 로고의 너비 (기본값: "auto") */
  width?: number | string;
  /** 로고의 높이 (기본값: "1.2em") */
  height?: number | string;
  /** 로고 텍스트 및 라인의 색상 (기본값: "currentColor") */
  color?: string;
  /** 하단 데코레이션 라인 표시 여부 */
  showLine?: boolean;
}

export default function OlfitLogo({ 
  className, 
  width = "auto", 
  height = "1.2em", 
  color = "currentColor",
  showLine = true
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
        y="50%"
        dominantBaseline="middle"
        textAnchor="middle"
        fill={color}
        style={{ 
          fontFamily: "'Playfair Display', serif", 
          fontWeight: 300, 
          fontSize: "26px", 
          letterSpacing: "0.28em",
          textTransform: "uppercase"
        }}
      >
        Olfit
      </text>
      {/* 단순 텍스트를 넘어선 로고 느낌을 위한 데코레이션 라인 */}
      {showLine && (
        <path 
          d="M25 32 H95" 
          stroke={color} 
          strokeWidth="0.5" 
          strokeOpacity="0.3" 
        />
      )}
    </svg>
  );
}

// EOF: OlfitLogo.tsx
