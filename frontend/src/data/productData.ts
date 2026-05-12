/**
 * @file productData.ts
 * @description 향수 제품의 데이터 인터페이스 구조를 정의하고, 전체 제품 리스트를 통합 관리하는 데이터 파일입니다.
 */

import type { Product } from '@/types';
import { personalProducts } from './personalData';

export type { Product };

export const products: Product[] = [
  ...personalProducts
];
// EOF: productData.ts
