/**
 * @file productData.ts
 * @description 향수 제품의 데이터 인터페이스 구조를 정의하고, 전체 제품 리스트를 통합 관리하는 데이터 파일입니다.
 */

import { personalProducts } from './personalData';

export interface Product {
  id: number;
  name: string;
  brand: string;
  price: string;
  size: string;
  image: string;
  tags: string[];
  notes: string; // 간략한 노트 요약 (호버용)
  family: string;
  featured?: boolean;
  category: "Personal";
  /** 클릭 시 모달에 노출될 상세 정보 */
  details: {
    story: string; // 향수의 탄생 스토리 또는 분위기 설명
    topNotes: string; // 탑 노트 상세
    middleNotes: string; // 미들 노트 상세
    baseNotes: string; // 베이스 노트 상세
    bestFor: string; // 추천 어울리는 순간/룩
  };
}

export const products: Product[] = [
  ...personalProducts
];
// EOF: productData.ts
