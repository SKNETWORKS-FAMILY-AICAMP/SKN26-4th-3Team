/**
 * @file recommendationEngine.ts
 * @description 사용자의 AI 인터뷰 분석 결과를 실제 제품 데이터와 매칭하는 로직입니다.
 * 이미지 분석 메타데이터와 사용자가 선택한 향기 노트를 기반으로 유사도를 계산합니다.
 */

import type { AnalysisResults } from "@/types";
import { personalProducts } from "../../crawler/personalData";
import type { Product } from "./productData";

/**
 * 인터뷰 결과에 따른 추천 제품들을 반환합니다.
 * (이미지 분석 무드 + 선택된 노트를 결합하여 유사도 높은 5개 제품 추출)
 */
export function getRecommendedProducts(results: AnalysisResults | null): (Product & { similarity: number })[] {
  if (!results) return [];

  const selectedNotes = results.analysisMetadata?.selectedNotes || [];
  
  // 제품별 유사도 점수 계산
  const scoredProducts = personalProducts.map((product) => {
    let score = 0;
    
    // 1. 선택된 노트와 제품 노트 간의 매칭 (가중치 2)
    selectedNotes.forEach((userNote) => {
      const targetText = `
        ${product.notes.toLowerCase()} 
        ${product.details.topNotes.toLowerCase()} 
        ${product.details.middleNotes.toLowerCase()} 
        ${product.details.baseNotes.toLowerCase()}
      `;
      if (targetText.includes(userNote.toLowerCase())) {
        score += 2;
      }
    });

    // 2. 패밀리 매칭 (기본 가중치 1)
    // 분석된 무드에 따른 추천 패밀리 (간소화된 로직)
    const mood = results.personalMood || "";
    if (mood.includes("시크") && (product.family === "우디" || product.family === "머스크")) score += 1.5;
    if (mood.includes("로맨틱") && product.family === "플로랄") score += 1.5;

    // 점수를 0-100 사이의 유사도 퍼센트로 변환 (최대 점수 8점 가정)
    const similarity = Math.min(Math.round((score / 8) * 100), 99);
    
    return { ...product, similarity: similarity > 0 ? similarity : Math.floor(Math.random() * 20) + 60 }; // 최소 60% 보정
  });

  // 유사도 순으로 정렬하여 상위 5개 반환
  return scoredProducts
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 5);
}

/**
 * 레이어링 추천을 위해 메인 향수와 서브 향수를 결정합니다.
 */
export function getLayeringRecommendation(results: AnalysisResults | null): { main: Product; accent: Product; outcome: string; description: string } | null {
  if (!results || results.type !== "personal") return null;

  const recommended = getRecommendedProducts(results);
  if (recommended.length < 2) {
    const main = recommended[0] || personalProducts[0];
    const accent = personalProducts[1];
    return {
      main,
      accent,
      outcome: "새벽의 숲과 시트러스",
      description: "우디한 베이스가 중심을 잡아주며 시트러스의 생동감이 더해집니다."
    };
  }

  const main = recommended[0];
  const accent = recommended[1];

  return {
    main,
    accent,
    outcome: "당신만을 위한 시그니처 레이어링",
    description: "이미지에서 추출된 분위기와 선택하신 노트가 완벽한 조화를 이룹니다."
  };
}
