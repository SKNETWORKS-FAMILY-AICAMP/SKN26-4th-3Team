/**
 * @file recommendationEngine.ts
 * @description 사용자의 인터뷰 분석 결과와 실제 향수 제품 데이터를 지능적으로 매칭하는 핵심 서비스 로직입니다.
 * 이미지 기반 무드 분석 결과와 사용자가 선택한 향기 노트를 다각도로 검토하여 유사도를 계산합니다.
 */

import type { AnalysisResults } from "@/types";
import { personalProducts } from "@/data/personalData";
import type { Product } from "@/data/productData";

/**
 * 인터뷰 결과에 따른 최적의 추천 제품 리스트를 반환합니다.
 * 시각적 무드 가중치와 후각적 노트 매칭 가중치를 결합하여 상위 5개를 추출합니다.
 * 
 * @param results AI 인터뷰 최종 분석 결과 객체
 * @returns {Array} 유사도 및 추천 사유가 포함된 제품 리스트
 */
export function getRecommendedProducts(results: AnalysisResults | null): (Product & { similarity: number, matchReason: string })[] {
  if (!results) return [];

  // 1. 백엔드에서 전달된 추천 결과가 있으면 최우선 사용 및 데이터 정규화
  if (results.recommendations && Array.isArray(results.recommendations)) {
    return results.recommendations.map((rec, idx) => ({
      ...rec,
      // ID가 문자열인 경우 숫자로 해싱하거나 인덱스 활용하여 충돌 방지
      id: typeof rec.id === 'number' ? rec.id : (idx + 1000), 
      brand: rec.brand || "Unknown",
      name: rec.name || "Unknown",
      price: rec.price || "정보 없음",
      size: rec.size || "N/A",
      image: rec.image || "",
      tags: Array.isArray(rec.tags) ? rec.tags : [],
      notes: rec.notes || "",
      family: rec.family || "프레시",
      similarity: rec.similarity ?? 90,
      matchReason: rec.matchReason || "AI가 선정한 당신의 스타일 매칭 향수입니다.",
      details: rec.details || {
        story: "",
        topNotes: "",
        middleNotes: "",
        baseNotes: "",
        bestFor: ""
      }
    })) as any;
  }

  // 2. 백엔드 결과가 없는 경우 로컬 데이터 fallback
  const meta = results.analysisMetadata;
  if (!meta) return [];
  const scoredProducts = personalProducts.map((product) => {
    let score = 0;
    const matchedNotes: string[] = [];
    const matchedKeywords: string[] = [];
    
    // 1. 후각적 매칭: 선택된 노트와 제품 성분 간의 교차 검증 (가중치 2)
    selectedNotes.forEach((userNote) => {
      if (!userNote) return;
      const targetText = `
        ${product.notes.toLowerCase()} 
        ${product.details.topNotes.toLowerCase()} 
        ${product.details.middleNotes.toLowerCase()} 
        ${product.details.baseNotes.toLowerCase()}
      `.replace(/\s+/g, '');
      
      if (targetText.includes(userNote.toLowerCase().replace(/\s+/g, ''))) {
        score += 2;
        matchedNotes.push(userNote);
      }
    });

    // 2. 백엔드 키워드 매칭: 변환된 향수 키워드와 제품 정보 매칭 (가중치 2)
    perfumeKeywords.forEach((keyword) => {
      if (!keyword) return;
      const cleanKeyword = keyword.replace("#", "").toLowerCase();
      const targetText = `${product.notes} ${product.family} ${product.details.story}`.toLowerCase();
      
      if (targetText.includes(cleanKeyword)) {
        score += 2;
        matchedKeywords.push(keyword);
      }
    });

    // 3. 시각적/심리적 매칭 (백엔드 키워드가 없을 때 보조적으로 사용)
    if (perfumeKeywords.length === 0) {
      if (mood.includes("시크") && (product.family === "우디" || product.family === "머스크")) {
        score += 1.5;
      }
      if (mood.includes("로맨틱") && product.family === "플로랄") {
        score += 1.5;
      }
      if (mood.includes("상쾌") && (product.family === "시트러스" || product.family === "프레쉬")) {
        score += 1.5;
      }
    }

    // 데이터 기반 동적 추천 사유(Reason) 생성
    let matchReason = "";
    if (matchedKeywords.length > 0) {
      matchReason = `AI가 분석한 당신의 분위기(${matchedKeywords.join(", ")})가 이 향수의 ${product.family} 계열과 뛰어난 조화를 이룹니다.`;
    } else if (matchedNotes.length > 0) {
      matchReason = `선택하신 #${matchedNotes.join(", #")} 성분이 포함되어 있어 당신이 선호하는 향의 본질을 잘 담고 있습니다.`;
    } else {
      matchReason = `당신의 독특한 스타일 지수를 분석한 결과, 새로운 분위기를 완성해줄 베스트 옵션으로 선정되었습니다.`;
    }

    // 정량적 점수를 백분율(0-100%) 유사도로 변환 및 보정
    const maxPossibleScore = (selectedNotes.length * 2) + (perfumeKeywords.length * 2) || 1.5;
    const rawSimilarity = (score / maxPossibleScore) * 100;
    
    // 데이터 쏠림 방지를 위한 안정적인 난수 보정값 추가 (시각적 다양성 확보)
    const stableRandom = (product.id % 10) / 10;
    const similarity = Math.min(Math.round(rawSimilarity * 0.3 + 65 + stableRandom), 98);
    
    return { ...product, similarity, matchReason };
  });

  // 유사도 내림차순 정렬 후 상위 5개 제품 선별
  return scoredProducts
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 5);
}

// EOF: recommendationEngine.ts
