/**
 * @file scentData.ts
 * @description 향기의 계열(Family) 및 농도(Concentration)에 대한 교육용 텍스트 데이터입니다.
 * 각 계열의 특징과 대표 성분, 부향률별 지속시간 정보를 포함합니다.
 */

import { Leaf, Mountain, Sparkles, Wind, Cookie } from "lucide-react";

/**
 * 향기 계열에 대한 총괄 설명
 */
export const familyDescription = "향기 계열은 향수의 성격과 분위기를 결정하는 가장 큰 기준입니다. 비슷한 성질을 가진 향료들을 그룹화하여, 당신이 선호하는 향의 지도를 그리는 첫걸음이 됩니다.";

/**
 * 부향률에 대한 총괄 설명
 */
export const concentrationDescription = "부향률은 향수 원액이 차지하는 비율로, 향의 지속성과 확산성을 결정합니다. 당신의 라이프스타일에 맞는 완벽한 농도를 선택해 보세요.";

/**
 * 향기 계열 데이터: Floral, Woody, Amber, Fresh, Gourmand 정보
 */
export const scentFamilies = [
  {
    title: "Floral",
    subtitle: "만개한 정원의 우아함",
    description: "꽃에서 피어나는 부드럽고 화사한 향입니다. <br className=\"hidden sm:inline\" /> 우아하고 편안한 분위기를 만들며, 가장 친숙하고 대중적인 인상을 줍니다.",
    keyNotes: ["장미", "자스민", "피오니", "튜베로즈", "릴리"],
    details: [
      { name: "Rose", desc: "화려하고 풍성한 꽃의 여왕 향기가 <br className=\"hidden sm:inline\" /> 우아하고 고전적인 존재감을 드러냅니다." },
      { name: "Jasmine", desc: "관능적이고 달콤한 밤의 꽃 향기가 <br className=\"hidden sm:inline\" /> 신비롭고 매혹적인 아우라를 더해줍니다." },
    ],
    icon: Leaf,
    color: "bg-cream",
  },
  {
    title: "Woody",
    subtitle: "대지의 깊은 안식",
    description: "나무결에서 느껴지는 따뜻하고 묵직한 향입니다. <br className=\"hidden sm:inline\" /> 차분하고 안정적인 무드를 주며, 세련되고 깊이 있는 인상을 더합니다.",
    keyNotes: ["샌달우드", "시더우드", "베티버", "파출리", "오크우드"],
    details: [
      { name: "Sandalwood", 
        desc: "부드럽고 크리미한 우유빛 나무 향이 <br className=\"hidden sm:inline\" /> 마음을 깊게 가라앉혀 평온을 선사합니다."
      },
      { name: "Cedarwood", 
        desc: "연필심처럼 건조하고 깨끗한 연필 향이 <br className=\"hidden sm:inline\" /> 현대적이고 지적인 세련미를 완성합니다."
      },
    ],
    icon: Mountain,
    color: "bg-wood/5",
  },
  {
<<<<<<< HEAD
    title: "Amber",
    subtitle: "신비로운 밤의 서사",
    description: "따뜻하고 달콤하며 감각적인 향입니다. <br className=\"hidden sm:inline\" /> 풍부하고 포근한 분위기를 만들며, 진하고 매력적인 잔향이 특징입니다.",
    keyNotes: ["바닐라", "벤조인", "라다넘", "인센스", "스파이스"],
    details: [
      { name: "Amber", desc: "황금빛 온기가 느껴지는 달콤한 향이 <br className=\"hidden sm:inline\" /> 포근한 위로와 성숙한 아름다움을 줍니다." },
      { name: "Vanilla", desc: "부드럽고 깊은 크림처럼 달콤한 향이 <br className=\"hidden sm:inline\" /> 심리적 안정감과 깊은 만족감을 선사합니다." },
=======
    title: "Floral",
    subtitle: "만개한 정원의 우아함",
    description: "꽃들의 섬세한 결이 모여 완성되는 풍성한 아름다움입니다. 화사한 생명력과 로맨틱한 무드를 자아내며, 가장 클래식하면서도 매혹적인 분위기를 연출합니다.",
    details: [
      { name: "Rose", desc: "화려하고 풍성한 꽃의 여왕 향기가 우아하고 고전적인 존재감을 드러냅니다." },
      { name: "Jasmine", desc: "관능적이고 달콤한 밤의 꽃 향기가 신비롭고 매혹적인 아우라를 더해줍니다." },
    ],
    icon: Leaf,
    color: "bg-cream",
  },
  {
    title: "Citrus",
    subtitle: "찬란한 햇살의 에너지",
    description: "갓 딴 과일의 껍질에서 터져 나오는 싱그럽고 활기찬 기운입니다. 기분을 즉각적으로 전환하며, 당신의 하루를 밝고 깨끗한 에너지로 가득 채워줍니다.",
    details: [
      { name: "Bergamot", desc: "차분한 감귤 향과 고급스러운 풍미가 세련되고 긍정적인 활력을 부여합니다." },
      { name: "Lemon", desc: "날카롭고 선명한 산미가 느껴지는 향이 지친 감각에 즉각적인 리프레시를 줍니다." },
    ],
    icon: Sun,
    color: "bg-[#FDFCF0]",
  },
  {
    title: "Oriental",
    subtitle: "신비로운 밤의 서사",
    description: "이국적인 향신료와 따스한 수지가 어우러진 깊은 잔향입니다. 포근한 온기와 함께 관능적인 매력을 풍기며, 잊히지 않는 긴 여운을 남깁니다.",
    details: [
      { name: "Amber", desc: "황금빛 온기가 느껴지는 달콤한 향이 포근한 위로와 성숙한 아름다움을 줍니다." },
      { name: "Vanilla", desc: "부드럽고 깊은 크림처럼 달콤한 향이 심리적 안정감과 깊은 만족감을 선사합니다." },
>>>>>>> c5c5017 (feat(frontend): migrate react fragrance experienceAdds the Vite React application, Tailwind styling, Zustand state, API services, report capture flow, reusable UI components, and static imagery for the Olfit fragrance matching experience.)
    ],
    icon: Sparkles,
    color: "bg-[#F9F4F2]",
  },
<<<<<<< HEAD
  {
    title: "Fresh",
    subtitle: "찬란한 햇살의 에너지",
    description: "맑고 산뜻하며 깨끗한 향입니다. <br className=\"hidden sm:inline\" /> 가볍고 상쾌한 인상을 주며, 청량하고 밝은 분위기를 완성합니다.",
    keyNotes: ["레몬", "베르가못", "자몽", "그린", "아쿠아틱"],
    details: [
      { name: "Bergamot", desc: "차분한 감귤 향과 고급스러운 풍미가 <br className=\"hidden sm:inline\" /> 세련되고 긍정적인 활력을 부여합니다." },
      { name: "Marine", desc: "푸른 바다의 소금기 섞인 바람처럼 <br className=\"hidden sm:inline\" /> 시원하고 투명한 해방감을 선사합니다." },
    ],
    icon: Wind,
    color: "bg-[#FDFCF0]",
  },
  {
    title: "Gourmand",
    subtitle: "달콤한 미식의 기억",
    description: "먹을 수 있을 것처럼 달콤하고 부드러운 향입니다. <br className=\"hidden sm:inline\" /> 디저트를 연상시키는 향으로 따뜻하고 유혹적인 느낌을 줍니다.",
    keyNotes: ["바닐라", "카라멜", "초콜릿", "커피", "허니"],
    details: [
      { name: "Praline", desc: "구운 견과류와 설탕의 고소하고 달콤한 풍미가 <br className=\"hidden sm:inline\" /> 거부할 수 없는 중독성을 선사합니다." },
      { name: "Honey", desc: "끈적하고 진한 꿀의 달콤함이 피부 위에 <br className=\"hidden sm:inline\" />녹아들어 관능적인 부드러움을 더합니다." },
    ],
    icon: Cookie,
    color: "bg-wood/[0.03]",
  },
];

/**
 * 향기의 계층(노트) 데이터
 */
export const noteHierarchy = [
  {
    title: "Top Note",
    subtitle: "첫인상의 찰나 (0-30분)",
    description: "향수를 뿌린 직후 느껴지는 첫 향기입니다. <br className=\"hidden sm:inline\" /> 휘발성이 강한 시트러스나 허브 계열이 주로 쓰이며, <br className=\"hidden sm:inline\" /> 전체적인 분위기를 결정하는 결정적인 첫인상을 남깁니다."
  },
  {
    title: "Middle Note",
    subtitle: "향기의 심장 (30분-2시간)",
    description: "하트 노트라고도 불리며, 향수의 본질적인 성격을 드러냅니다. <br className=\"hidden sm:inline\" /> 탑 노트가 사라진 후 서서히 피어나며, 오랜 시간 동안 조화로운 풍성함을 유지합니다."
  },
  {
    title: "Base Note",
    subtitle: "깊은 여운의 잔향 (2시간-끝까지)",
    description: "가장 무거운 분자로 구성되어 피부에 가장 오래 머무는 향기입니다. 우디나 머스크 계열이 주로 쓰이며, <br className=\"hidden sm:inline\" />향수의 깊이감과 마지막 인상을 완성합니다."
  }
=======
>>>>>>> c5c5017 (feat(frontend): migrate react fragrance experienceAdds the Vite React application, Tailwind styling, Zustand state, API services, report capture flow, reusable UI components, and static imagery for the Olfit fragrance matching experience.)
];

/**
 * 향수 등급(부향률) 데이터: Parfum, EDP, EDT, EDC 정보
 */
export const concentrations = [
  { type: "Parfum", koType: "퍼퓸", ratio: "20-30%", duration: "7-8h+", desc: "가장 진하고 깊은 영혼의 향기" },
  { type: "Eau de Parfum", koType: "오 드 퍼퓸", ratio: "15-20%", duration: "5-6h", desc: "풍부한 잔향이 매력적인 데일리 시그니처" },
  { type: "Eau de Toilette", koType: "오 드 뚜왈렛", ratio: "5-15%", duration: "3-4h", desc: "가볍고 산뜻하게 시작하는 하루의 기분" },
  { type: "Eau de Cologne", koType: "오 드 코롱", ratio: "2-4%", duration: "1-2h", desc: "은은하고 투명하게 스치는 향기의 흔적" },
];

// EOF: scentData.ts
