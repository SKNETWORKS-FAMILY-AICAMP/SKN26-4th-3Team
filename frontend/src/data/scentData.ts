/**
 * @file scentData.ts
 * @description 향기의 계열(Family) 및 농도(Concentration)에 대한 교육용 텍스트 데이터입니다.
 * 각 계열의 특징과 대표 성분, 부향률별 지속시간 정보를 포함합니다.
 */

import { Leaf, Mountain, Sun, Sparkles } from "lucide-react";

/**
 * 향기 계열 데이터: Woody, Floral, Citrus, Oriental 정보
 */
export const scentFamilies = [
  {
    title: "Woody",
    subtitle: "대지의 깊은 안식",
    description: "나무의 결에서 느껴지는 따뜻하고 묵직한 힘입니다. 숲속을 걷는 듯한 차분함과 지적인 신뢰감을 동시에 전달하며, 당신의 분위기에 안정적인 무게감을 더해줍니다.",
    details: [
      { name: "Sandalwood", 
        desc: "부드럽고 크리미한 우유빛 나무 향이 마음을 깊게 가라앉혀 평온을 선사합니다."
      },
      { name: "Cedarwood", 
        desc: "연필심처럼 건조하고 깨끗한 연필 향이 현대적이고 지적인 세련미를 완성합니다."
      },
    ],
    icon: Mountain,
    color: "bg-wood/5",
  },
  {
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
    ],
    icon: Sparkles,
    color: "bg-[#F9F4F2]",
  },
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
