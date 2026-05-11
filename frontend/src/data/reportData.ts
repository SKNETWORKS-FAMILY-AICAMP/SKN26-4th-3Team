/**
 * @file reportData.ts
 * @description 진단 리포트 섹션에서 시각화 및 정보 제공을 위해 사용되는 정적 데이터 정의 파일입니다.
 * 유사 페르소나 정보와 레이더 차트의 기본 축 명칭 및 설명을 포함합니다.
 */

/**
 * 유사한 스타일의 페르소나 데이터
 */
export const auras = [
  { 
    name: "어반 미니멀리스트", 
    match: 94, 
    image: "/persona_1.jpg" 
  },
  { 
    name: "아방가르드 크리에이터", 
    match: 87, 
    image: "/persona_2.jpg" 
  },
  { 
    name: "내추럴 컨템플레이터", 
    match: 81, 
    image: "/persona_3.jpg" 
  },
];

/**
 * 방사형 차트용 초기 데이터 (향기 노트별 분석 수치)
 */
export const radarData = [
  { 
    axis: "플로랄", 
    value: 0.3,
    description: "꽃들의 섬세한 결이 모여 완성되는 풍성한 아름다움"
  },
  { 
    axis: "우디", 
    value: 0.75,
    description: "나무의 결에서 느껴지는 따뜻하고 묵직한 힘"
  },
  { 
    axis: "오리엔탈", 
    value: 0.45,
    description: "이국적인 향신료와 따스한 수지가 어우러진 깊은 잔향"
  },
  { 
    axis: "프레시", 
    value: 0.6,
    description: "갓 딴 과일의 싱그러움과 맑은 공기의 청량함"
  },
  { 
    axis: "구르망", 
    value: 0.2,
    description: "바닐라, 초콜릿처럼 달콤하고 포근한 미식의 향기"
  },
];

// EOF: reportData.ts
