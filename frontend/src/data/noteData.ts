/**
 * @file noteData.ts
 * @description 향수의 주요 원료(Notes)에 대한 상세 설명을 담은 데이터베이스입니다.
 * 향조(Note) 선택 UI(탭 + 단일 항목 캐러셀)에 사용됩니다.
 */

export interface ScentNote {
  id: string;
  name: string;
  family: string;
  category: "Top" | "Middle" | "Base";
  description: string;
  representative: string[];
  origin: string;
}

export const topNotesData: ScentNote[] = [
  {
    id: "bergamot",
    name: "베르가못",
    family: "Fresh",
    category: "Top",
    description: "밝고 청량한 시트러스 향입니다. <br /> 향의 첫인상을 맑고 세련되게 열어줍니다.",
    representative: ["베르가못", "레몬", "라임", "자몽", "만다린", "네롤리", "페티그레인"],
    origin: "감귤류 과일의 껍질"
  },
  {
    id: "lemon",
    name: "레몬",
    family: "Fresh",
    category: "Top",
    description: "깨끗하고 산뜻한 시트러스 향입니다. <br /> 향을 가볍고 생기 있게 시작하게 해줍니다.",
    representative: ["레몬", "베르가못", "라임", "자몽", "유자", "만다린", "네롤리"],
    origin: "감귤류 과일의 껍질"
  },
  {
    id: "lime",
    name: "라임",
    family: "Fresh",
    category: "Top",
    description: "톡 쏘는 듯한 청량감이 있는 향입니다. <br /> 더 날카롭고 상쾌한 첫인상을 만듭니다.",
    representative: ["라임", "레몬", "베르가못", "자몽", "그레이프프루트", "만다린", "민트"],
    origin: "감귤류 과일의 껍질"
  },
  {
    id: "grapefruit",
    name: "자몽",
    family: "Fresh",
    category: "Top",
    description: "쌉싸름하고 또렷한 시트러스 향입니다. <br /> 밝지만 더 현대적인 인상을 줍니다.",
    representative: ["자몽", "베르가못", "레몬", "라임", "만다린", "네롤리", "페티그레인"],
    origin: "감귤류 과일의 과육과 껍질"
  },
  {
    id: "mandarin",
    name: "만다린",
    family: "Fresh",
    category: "Top",
    description: "부드럽고 달콤한 감귤 향입니다. <br /> 친근하고 편안한 분위기를 만들어줍니다.",
    representative: ["만다린", "레몬", "베르가못", "라임", "자몽", "네롤리", "오렌지블라썸"],
    origin: "감귤류 과일의 껍질"
  },
  {
    id: "neroli",
    name: "네롤리",
    family: "Fresh",
    category: "Top",
    description: "맑고 우아한 시트러스 플로럴 향입니다. <br /> 깨끗하면서도 고급스러운 느낌을 더합니다.",
    representative: ["네롤리", "베르가못", "오렌지블라썸", "레몬", "만다린", "페티그레인", "자스민"],
    origin: "비터오렌지 꽃"
  },
  {
    id: "petitgrain",
    name: "페티그레인",
    family: "Fresh",
    category: "Top",
    description: "초록빛이 도는 상쾌한 시트러스 향입니다. <br /> 차분한 청량감으로 균형을 잡아줍니다.",
    representative: ["페티그레인", "베르가못", "네롤리", "라벤더", "레몬", "만다린", "그린노트"],
    origin: "비터오렌지 잎과 가지"
  }
];

export const middleNotesData: ScentNote[] = [
  {
    id: "rose",
    name: "장미",
    family: "Floral",
    category: "Middle",
    description: "가장 클래식한 플로럴 향입니다. <br /> 향의 중심을 우아하고 풍부하게 채워줍니다.",
    representative: ["장미", "재스민", "피오니", "오렌지블라썸", "일랑일랑", "아이리스", "제라늄"],
    origin: "장미꽃의 꽃잎"
  },
  {
    id: "jasmine",
    name: "재스민",
    family: "Floral",
    category: "Middle",
    description: "달콤하고 깊은 화이트 플로럴 향입니다. <br /> 향에 관능적인 밀도를 더해줍니다.",
    representative: ["재스민", "장미", "오렌지블라썸", "튜베로즈", "일랑일랑", "아이리스", "네롤리"],
    origin: "재스민 꽃"
  },
  {
    id: "orange-blossom",
    name: "오렌지블라썸",
    family: "Floral",
    category: "Middle",
    description: "달콤하고 맑은 꽃향입니다. <br /> 시트러스와 플로럴 사이를 자연스럽게 이어줍니다.",
    representative: ["오렌지블라썸", "네롤리", "장미", "재스민", "피오니", "일랑일랑", "머그렛"],
    origin: "오렌지 나무의 꽃"
  },
  {
    id: "peony",
    name: "피오니",
    family: "Floral",
    category: "Middle",
    description: "부드럽고 사랑스러운 플로럴 향입니다. <br /> 가볍고 깨끗한 로맨틱함을 줍니다.",
    representative: ["피오니", "장미", "재스민", "오렌지블라썸", "아이리스", "머스크", "로터스"],
    origin: "모란꽃"
  },
  {
    id: "ylang-ylang",
    name: "일랑일랑",
    family: "Floral",
    category: "Middle",
    description: "달콤하고 크리미한 꽃향입니다. <br /> 이국적이고 풍부한 분위기를 더합니다.",
    representative: ["일랑일랑", "장미", "재스민", "오렌지블라썸", "튜베로즈", "아이리스", "바닐라"],
    origin: "일랑일랑 꽃"
  },
  {
    id: "iris",
    name: "아이리스",
    family: "Floral",
    category: "Middle",
    description: "건조하고 파우더리한 향입니다. <br /> 차분하고 정제된 고급스러움을 줍니다.",
    representative: ["아이리스", "장미", "피오니", "바이올렛", "머스크", "시더우드", "앰버"],
    origin: "아이리스 뿌리줄기"
  },
  {
    id: "cardamom",
    name: "카다멈",
    family: "Amber",
    category: "Middle",
    description: "따뜻하고 스파이시한 향입니다. <br /> 향에 긴장감과 세련미를 더해줍니다.",
    representative: ["카다멈", "계피", "클로브", "후추", "장미", "재스민", "시더우드"],
    origin: "생강과 식물의 씨앗"
  }
];

export const baseNotesData: ScentNote[] = [
  {
    id: "sandalwood",
    name: "샌달우드",
    family: "Woody",
    category: "Base",
    description: "부드럽고 크리미한 우디 향입니다. <br /> 향 전체를 따뜻하게 받쳐줍니다.",
    representative: ["샌달우드", "시더우드", "베티버", "파출리", "앰버", "바닐라", "머스크"],
    origin: "나무의 심재"
  },
  {
    id: "cedarwood",
    name: "시더우드",
    family: "Woody",
    category: "Base",
    description: "건조하고 맑은 우디 향입니다. <br /> 향에 단단한 구조감과 세련미를 줍니다.",
    representative: ["시더우드", "샌달우드", "베티버", "파출리", "앰버", "머스크", "인센스"],
    origin: "향나무의 목재"
  },
  {
    id: "vetiver",
    name: "베티버",
    family: "Woody",
    category: "Base",
    description: "흙내음이 느껴지는 묵직한 향입니다. <br /> 잔향에 깊이와 안정감을 더합니다.",
    representative: ["베티버", "시더우드", "샌달우드", "파출리", "앰버", "오크모스", "머스크"],
    origin: "벼과 식물의 뿌리"
  },
  {
    id: "patchouli",
    name: "파출리",
    family: "Woody",
    category: "Base",
    description: "어둡고 흙내음이 강한 향입니다. <br /> 개성 있고 몽환적인 잔향을 남깁니다.",
    representative: ["파출리", "베티버", "시더우드", "샌달우드", "앰버", "바닐라", "인센스"],
    origin: "파출리 잎"
  },
  {
    id: "amber",
    name: "앰버",
    family: "Amber",
    category: "Base",
    description: "따뜻하고 달콤한 잔향을 만드는 향입니다. <br /> 포근하고 감각적인 분위기를 남깁니다.",
    representative: ["앰버", "바닐라", "벤조인", "라다넘", "인센스", "통카빈", "머스크"],
    origin: "레진과 바닐라 계열의 조합"
  },
  {
    id: "vanilla",
    name: "바닐라",
    family: "Gourmand",
    category: "Base",
    description: "달콤하고 부드러운 크리미한 향입니다. <br /> 향을 포근하고 친근하게 만들어줍니다.",
    representative: ["바닐라", "앰버", "통카빈", "벤조인", "머스크", "샌달우드", "카라멜"],
    origin: "바닐라 오키드의 꼬투리"
  },
  {
    id: "musk",
    name: "머스크",
    family: "Amber",
    category: "Base",
    description: "깨끗하고 부드러운 피부 같은 향입니다. <br /> 다른 향을 둥글게 감싸며 마무리해줍니다.",
    representative: ["머스크", "앰버", "샌달우드", "바닐라", "시더우드", "파출리", "아이리스"],
    origin: "과거 사향에서 유래한 향조"
  }
];

export const scentNotes: ScentNote[] = [
  ...topNotesData,
  ...middleNotesData,
  ...baseNotesData
];

// EOF: noteData.ts
