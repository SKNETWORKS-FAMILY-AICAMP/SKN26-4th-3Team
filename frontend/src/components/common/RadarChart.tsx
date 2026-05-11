/**
 * @file RadarChart.tsx
 * @description 사용자의 취향 분석 결과를 시각화하기 위한 방사형(레이더) 차트 컴포넌트입니다.
 * SVG를 사용하여 구현되었으며, 인터랙티브한 호버 효과와 부드러운 애니메이션을 제공합니다.
 */

import { useEffect, useState } from "react";
import { useIntersectionObserver } from "@/hooks/useIntersectionObserver";
import { radarData } from "@/data/reportData";

interface RadarChartProps {
  /** 
   * 인터뷰 결과 데이터 리스트 
   * axis: 축 이름 (예: '시트러스', '우디')
   * value: 0~1 사이의 가중치 수치
   * description: 호버 시 노출될 상세 설명
   */
  data?: { axis: string; value: number; description?: string }[];
  /** 분석 완료 직후 애니메이션을 강제로 트리거할지 여부 */
  forceDraw?: boolean;
}

export default function RadarChart({ data, forceDraw }: RadarChartProps) {
  const { ref, isVisible } = useIntersectionObserver();
  const [drawn, setDrawn] = useState(false);
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  // 데이터가 제공되지 않은 경우 기본 스켈레톤/더미 데이터 사용
  const chartData = data || radarData;

  /**
   * 뷰포트에 진입하거나 강제 드로우 요청 시 애니메이션 시작
   */
  useEffect(() => {
    if (isVisible || forceDraw) {
      const timer = setTimeout(() => setDrawn(true), 300);
      return () => clearTimeout(timer);
    }
  }, [isVisible, forceDraw]);

  // 차트 렌더링을 위한 기하학적 상수
  const size = 300; // SVG 내부 좌표계 크기
  const center = size / 2;
  const radius = 100; // 최대 반지름
  const angleStep = (Math.PI * 2) / chartData.length;

  /**
   * 데이터 인덱스와 수치를 기반으로 SVG 좌표를 계산합니다.
   */
  const getPoint = (i: number, value: number) => {
    const angle = i * angleStep - Math.PI / 2;
    return {
      x: center + radius * value * Math.cos(angle),
      y: center + radius * value * Math.sin(angle),
    };
  };

  // 폴리곤 경로 생성
  const polygonPoints = chartData
    .map((d, i) => {
      const p = getPoint(i, d.value);
      return `${p.x},${p.y}`;
    })
    .join(" ");

  return (
    <div ref={ref} className="relative w-full max-w-[320px] mx-auto aspect-square flex items-center justify-center">
      <svg viewBox={`0 0 ${size} ${size}`} className="w-full h-full overflow-visible">
        {/* 배경 그리드: 방사형 가이드 원 */}
        {[0.2, 0.4, 0.6, 0.8, 1].map((r) => (
          <circle
            key={r}
            cx={center}
            cy={center}
            r={radius * r}
            fill="none"
            stroke="rgba(107, 68, 35, 0.08)"
            strokeWidth={1}
          />
        ))}
        {/* 배경 그리드: 중심에서 뻗어나가는 축 라인 */}
        {chartData.map((_, i) => {
          const p = getPoint(i, 1);
          return (
            <line
              key={i}
              x1={center}
              y1={center}
              x2={p.x}
              y2={p.y}
              stroke="rgba(107, 68, 35, 0.08)"
              strokeWidth={1}
            />
          );
        })}
        {/* 데이터 영역: 투명한 색상이 채워진 폴리곤 */}
        <polygon
          points={polygonPoints}
          fill="rgba(107, 68, 35, 0.06)"
          stroke="#6B4423"
          strokeWidth={1.5}
          className={`transition-all duration-1000 ${drawn ? "opacity-100" : "opacity-0"}`}
          style={{ transitionTimingFunction: "cubic-bezier(0.25, 0.46, 0.45, 0.94)" }}
        />
        {/* 데이터 꼭짓점: 호버 가능한 서클 포인트 */}
        {chartData.map((d, i) => {
          const p = getPoint(i, d.value);
          return (
            <circle
              key={`point-${i}`}
              cx={p.x}
              cy={p.y}
              r={hoveredIndex === i ? 5 : 3}
              fill="#6B4423"
              className={`transition-all duration-500 cursor-help ${drawn ? "opacity-100" : "opacity-0"}`}
              style={{ transitionDelay: drawn ? "0ms" : `${600 + i * 100}ms` }}
              onMouseEnter={() => setHoveredIndex(i)}
              onMouseLeave={() => setHoveredIndex(null)}
            />
          );
        })}
        {/* 축 텍스트: 향기 계열 명칭 */}
        {chartData.map((d, i) => {
          const p = getPoint(i, 1.25);
          return (
            <text
              key={`label-${i}`}
              x={p.x}
              y={p.y}
              textAnchor="middle"
              dominantBaseline="middle"
              className={`text-[12px] md:text-[11px] font-medium uppercase tracking-[0.15em] cursor-help transition-colors duration-300 ${
                hoveredIndex === i ? "fill-wood" : "fill-wood/60"
              }`}
              style={{ fontFamily: "'Playfair Display', serif" }}
              onMouseEnter={() => setHoveredIndex(i)}
              onMouseLeave={() => setHoveredIndex(null)}
            >
              {d.axis}
            </text>
          );
        })}
      </svg>

      {/* 툴팁: 마우스 호버 시 해당 항목의 상세 분석 결과 표시 */}
      {hoveredIndex !== null && chartData[hoveredIndex].description && (
        <div 
          className="absolute z-10 bg-white/95 backdrop-blur-sm border border-wood/20 px-3 py-2 rounded-lg shadow-xl pointer-events-none animate-in fade-in zoom-in duration-200"
          style={{
            top: `${(getPoint(hoveredIndex, 1.45).y / size) * 100}%`,
            left: `${(getPoint(hoveredIndex, 1.45).x / size) * 100}%`,
            transform: 'translate(-50%, -50%)',
            width: 'max-content',
            maxWidth: '180px'
          }}
        >
          <p className="text-[10px] text-wood/80 leading-relaxed text-center break-keep">
            {chartData[hoveredIndex].description}
          </p>
          {/* 말풍선 꼬리 장식 */}
          <div 
            className={`absolute w-2 h-2 bg-white border-wood/20 rotate-45 ${
              hoveredIndex === 0 || hoveredIndex === 1 || hoveredIndex === 4 
                ? "bottom-[-5px] border-b border-r" 
                : "top-[-5px] border-t border-l"
            }`}
            style={{
              left: '50%',
              marginLeft: '-4px',
            }}
          />
        </div>
      )}
    </div>
  );
}

// EOF: RadarChart.tsx
