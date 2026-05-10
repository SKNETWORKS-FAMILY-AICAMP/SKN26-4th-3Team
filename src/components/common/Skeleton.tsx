/**
 * @file Skeleton.tsx
 * @description 데이터 로딩 중 실제 콘텐츠의 레이아웃 뼈대를 미리 보여주어 인지 성능을 높이는 컴포넌트입니다.
 */

interface SkeletonProps {
  className?: string;
}

export default function Skeleton({ className = "" }: SkeletonProps) {
  return (
    <div className={`bg-wood/5 animate-pulse rounded-sm ${className}`} />
  );
}

/**
 * 섹션 전체를 위한 프리셋 스켈레톤
 */
export function SectionSkeleton() {
  return (
    <div className="w-full py-24 px-6 md:px-20 space-y-12">
      <Skeleton className="w-24 h-4" />
      <Skeleton className="w-3/4 h-12" />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <Skeleton className="aspect-square w-full" />
        <div className="space-y-6">
          <Skeleton className="w-full h-4" />
          <Skeleton className="w-full h-4" />
          <Skeleton className="w-2/3 h-4" />
        </div>
      </div>
    </div>
  );
}
