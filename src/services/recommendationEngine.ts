/**
 * @file recommendationEngine.ts
 * @description 사용자의 AI 인터뷰 분석 결과를 실제 제품 데이터와 매칭하는 로직입니다.
 * 이미지 분석 메타데이터와 사용자가 선택한 향기 노트를 기반으로 유사도를 계산합니다.
 */

import type { AnalysisResults } from "@/types";
import { personalProducts } from "@/data/personalData";
import type { Product } from "@/data/productData";

/**
 * 인터뷰 결과에 따른 추천 제품들을 반환합니다.
 * (이미지 분석 무드 + 선택된 노트를 결합하여 유사도 높은 5개 제품 추출)
 */
export function getRecommendedProducts(results: AnalysisResults | null): (Product & { similarity: number, matchReason: string })[] {
  if (!results) return [];

  const selectedNotes = results.analysisMetadata?.selectedNotes || [];
  const mood = results.personalMood || "";
  
  // 제품별 유사도 점수 계산
  const scoredProducts = personalProducts.map((product) => {
    let score = 0;
    const matchedNotes: string[] = [];
    let moodMatch = false;
    
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
        matchedNotes.push(userNote);
      }
    });

    // 2. 패밀리 매칭 (기본 가중치 1.5)
    if (mood.includes("시크") && (product.family === "우디" || product.family === "머스크")) {
      score += 1.5;
      moodMatch = true;
    }
    if (mood.includes("로맨틱") && product.family === "플로랄") {
      score += 1.5;
      moodMatch = true;
    }
    if (mood.includes("상쾌") && (product.family === "시트러스" || product.family === "프레쉬")) {
      score += 1.5;
      moodMatch = true;
    }

    // 추천 사유 생성
    let matchReason = "";
    if (matchedNotes.length > 0 && moodMatch) {
      matchReason = `선택하신 #${matchedNotes[0]} 노트와 이미지의 시크한 무드가 이 제품의 ${product.family} 계열과 완벽한 조화를 이룹니다.`;
    } else if (matchedNotes.length > 0) {
      matchReason = `선택하신 #${matchedNotes.join(", #")} 성분이 포함되어 있어 당신이 선호하는 향의 본질을 잘 담고 있습니다.`;
    } else if (moodMatch) {
      matchReason = `이미지에서 느껴지는 현대적인 아우라가 이 향수의 ${product.family} 무드와 높은 싱크로율을 보입니다.`;
    } else {
      matchReason = `당신의 독특한 스타일 지수를 분석한 결과, 새로운 분위기를 완성해줄 베스트 옵션으로 선정되었습니다.`;
    }

    // 점수를 0-100 사이의 유사도 퍼센트로 변환
    const maxPossibleScore = (selectedNotes.length * 2) + 1.5;
    const rawSimilarity = maxPossibleScore > 0 ? (score / maxPossibleScore) * 100 : 70;
    const stableRandom = (product.id % 10) / 10;
    const similarity = Math.min(Math.round(rawSimilarity * 0.3 + 65 + stableRandom), 98);
    
    return { ...product, similarity, matchReason };
  });

  // 유사도 순으로 정렬하여 상위 5개 반환
  return scoredProducts
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 5);
}
