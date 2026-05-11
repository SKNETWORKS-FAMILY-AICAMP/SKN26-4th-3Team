/**
 * @file useIntersectionObserver.ts
 * @description 요소의 가시성 및 브라우저 스크롤 상태를 감지하는 유틸리티성 커스텀 훅 모음입니다.
 * 뷰포트 진입 기반 애니메이션, 동적 네비게이션 스타일 변화 등에 활용됩니다.
 */

import { useEffect, useRef, useState } from "react";

/**
 * 특정 요소가 뷰포트에 진입했는지 감지합니다.
 * 등장 시 한 번만 상태를 업데이트하고 관찰을 종료하는 일회성 애니메이션 트리거에 최적화되어 있습니다.
 * 
 * @param options IntersectionObserver 초기화 옵션 (threshold 등)
 * @returns { ref, isVisible } 감지할 요소에 할당할 ref와 가시성 boolean 값
 */
export function useIntersectionObserver(options?: IntersectionObserverInit) {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          // 단발성 애니메이션을 위해 한 번 진입하면 관찰 종료
          observer.unobserve(el);
        }
      },
      { threshold: 0.15, ...options }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [options]);

  return { ref, isVisible };
}

/**
 * 윈도우 스크롤 Y축 위치를 실시간으로 추적합니다.
 * 
 * @returns {number} 현재 윈도우의 scrollY 값
 */
export function useScrollPosition() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return scrollY;
}

/**
 * 스크롤 위치가 지정한 임계값(Threshold)을 초과했는지 여부를 감지합니다.
 * 실시간 좌표 대신 boolean만 관리하여 불필요한 리렌더링을 최소화합니다.
 * 
 * @param threshold 감지 기준 높이 (단위: px)
 * @returns {boolean} 임계값 초과 여부
 */
export function useIsScrolled(threshold: number) {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const scrolled = window.scrollY > threshold;
      if (scrolled !== isScrolled) {
        setIsScrolled(scrolled);
      }
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll(); // 초기 로드 시점 체크
    return () => window.removeEventListener("scroll", handleScroll);
  }, [isScrolled, threshold]);

  return isScrolled;
}

// EOF: useIntersectionObserver.ts
