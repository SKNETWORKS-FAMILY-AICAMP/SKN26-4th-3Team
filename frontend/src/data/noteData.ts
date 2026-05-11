/**
 * @file noteData.ts
 * @description 향수의 주요 원료(Notes)에 대한 상세 설명을 담은 데이터베이스입니다.
 * 브랜드명을 배제하고 향기가 주는 이미지와 공간감을 중심으로 추상적이고 감성적으로 묘사합니다.
 */

export interface ScentNote {
  name: string;
  enName: string;
  category: "Top" | "Middle" | "Base";
  description: string;
  origin: string;
}

export const scentNotes: ScentNote[] = [
  // --- TOP NOTES (8): 싱그럽고 즉각적인 첫인상 ---
  {
    name: "베르가못",
    enName: "Bergamot",
    category: "Top",
    description: "이른 아침 정원에 쏟아지는 화사한 햇살처럼, 마음을 환하게 밝혀주는 맑고 깨끗한 시트러스의 정수입니다.",
    origin: "이탈리아산 감귤류 과일"
  },
  {
    name: "네롤리",
    enName: "Neroli",
    category: "Top",
    description: "순백의 꽃잎들이 바람에 흩날리는 듯한 싱그러움. 깨끗하게 정제된 공기와 로맨틱한 설레임을 동시에 전합니다.",
    origin: "비터 오렌지 나무의 꽃"
  },
  {
    name: "알데하이드",
    enName: "Aldehyde",
    category: "Top",
    description: "눈 덮인 들판에서 마주한 차갑고 투명한 공기. 갓 세탁한 하얀 면 시트처럼 눈부시게 깨끗한 느낌을 선사합니다.",
    origin: "합성 향료 원료"
  },
  {
    name: "페어",
    enName: "Pear",
    category: "Top",
    description: "늦여름 과수원에서 불어오는 달콤하고 시원한 바람. 잘 익은 과일의 투명한 과즙이 주는 생동감을 담았습니다.",
    origin: "신선한 서양배 추출물"
  },
  {
    name: "핑크 페퍼",
    enName: "Pink Pepper",
    category: "Top",
    description: "무채색의 공간에 튀는 선명한 색채처럼, 향기의 시작에 리드미컬하고 세련된 에너지를 불어넣습니다.",
    origin: "브라질산 페퍼 트리 열매"
  },
  {
    name: "주니퍼 베리",
    enName: "Juniper Berry",
    category: "Top",
    description: "서늘한 새벽 숲속의 맑은 공기. 차갑고 이지적인 분위기와 함께 정체된 감각을 일깨우는 청량한 선율입니다.",
    origin: "주니퍼 나무의 열매"
  },
  {
    name: "민트",
    enName: "Mint",
    category: "Top",
    description: "고요한 수면에 던져진 작은 파동처럼, 정체된 일상을 깨우는 날카롭고 시원한 숨결을 선사합니다.",
    origin: "박하 식물의 잎"
  },
  {
    name: "카다멈",
    enName: "Cardamom",
    category: "Top",
    description: "낯선 도시의 모래바람처럼 야성적이면서도 부드러운 온기. 묵직하고 세련된 긴장감을 향기의 도입부에 더합니다.",
    origin: "생강과 식물의 씨앗"
  },

  // --- MIDDLE NOTES (8): 향수의 성격과 심장 ---
  {
    name: "로즈",
    enName: "Rose",
    category: "Middle",
    description: "가장 클래식하면서도 현대적인 우아함의 상징. 화려한 꽃잎의 결을 따라 흐르는 깊고 풍부한 기품을 담았습니다.",
    origin: "터키 및 불가리아산 장미"
  },
  {
    name: "자스민",
    enName: "Jasmine",
    category: "Middle",
    description: "밤의 고요를 타고 번지는 신비로운 달콤함. 관능적이면서도 섬세한 꽃향기가 향기에 입체적인 깊이감을 더합니다.",
    origin: "이집트 및 인도산 자스민 꽃"
  },
  {
    name: "무화과",
    enName: "Fig",
    category: "Middle",
    description: "크리미한 과육과 쌉싸름한 잎사귀의 조화. 지적이면서도 평화로운 오후의 정취를 떠올리게 하는 중성적인 향입니다.",
    origin: "무화과 열매와 잎"
  },
  {
    name: "아이리스",
    enName: "Iris",
    category: "Middle",
    description: "파우더리하고 귀족적인 보랏빛 안개. 피부 위에 닿는 벨벳처럼 부드럽고 우아한 잔상을 남깁니다.",
    origin: "붓꽃의 말린 뿌리"
  },
  {
    name: "화이트 티",
    enName: "White Tea",
    category: "Middle",
    description: "마음의 소란을 잠재우는 투명하고 정갈한 찻잎의 향. 고요한 공간에서 즐기는 명상적인 평온함을 선사합니다.",
    origin: "어린 차나무 잎"
  },
  {
    name: "편백",
    enName: "Hinoki",
    category: "Middle",
    description: "비 내린 뒤 숲길에서 느껴지는 깊은 호흡. 나무가 전하는 묵직한 안식과 치유의 무드를 향기에 담았습니다.",
    origin: "일본산 편백나무 추출물"
  },
  {
    name: "라벤더",
    enName: "Lavender",
    category: "Middle",
    description: "보랏빛 들판의 깨끗한 바람. 지친 감각을 부드럽게 감싸 안으며 이성적이고 세련된 휴식을 제안합니다.",
    origin: "라벤더 꽃과 잎"
  },
  {
    name: "블랙커런트",
    enName: "Blackcurrant",
    category: "Middle",
    description: "매혹적인 보랏빛 열매의 생동감. 야생의 울창한 숲에서 마주한 뜻밖의 달콤함과 날카로운 생명력을 표현합니다.",
    origin: "블랙커런트 열매와 싹"
  },

  // --- BASE NOTES (8): 피부에 남는 깊은 여운 ---
  {
    name: "샌달우드",
    enName: "Sandalwood",
    category: "Base",
    description: "오래된 고성의 서재에서 느껴지는 깊은 나무 향. 차분하고 밀도 높은 우유빛 질감이 마음의 중심을 잡아줍니다.",
    origin: "인도산 백단향 나무"
  },
  {
    name: "머스크",
    enName: "Musk",
    category: "Base",
    description: "따뜻한 살결을 스치는 보드라운 린넨의 감촉. 모든 향기를 포근하게 껴안으며 신비로운 안정감으로 마무리합니다.",
    origin: "식물성 및 합성 향료 원료"
  },
  {
    name: "앰버",
    enName: "Amber",
    category: "Base",
    description: "황금빛 보석 안에 갇힌 따스한 온기. 피부 위에 오래도록 머무는 성숙한 관능미와 아늑한 위로를 동시에 전합니다.",
    origin: "나무 수지(Resin)에서 유래"
  },
  {
    name: "베티버",
    enName: "Vetiver",
    category: "Base",
    description: "비 온 뒤 대지의 흙 내음과 쌉싸름한 잔향. 이성적이고 묵직한 존재감을 지닌 대지의 에너지를 담았습니다.",
    origin: "열대 지방 풀의 뿌리"
  },
  {
    name: "바닐라",
    enName: "Vanilla",
    category: "Base",
    description: "차가운 계절을 감싸는 달콤한 외투처럼, 포근하고 아늑한 위로와 함께 고급스러운 매력을 완성합니다.",
    origin: "마다가스카르산 바닐라 빈"
  },
  {
    name: "가죽",
    enName: "Leather",
    category: "Base",
    description: "야성적이고 센슈얼한 카리스마. 거칠면서도 매끄러운 질감이 주는 독보적인 존재감과 강렬한 잔상을 남깁니다.",
    origin: "자작나무 타르 등 복합 향료"
  },
  {
    name: "우드",
    enName: "Oud",
    category: "Base",
    description: "침향나무에서 얻는 가장 진귀한 시간의 흔적. 묵직하고 어두운 나무 향이 전하는 신비롭고 장엄한 울림입니다.",
    origin: "동남아시아의 침향나무"
  },
  {
    name: "인센스",
    enName: "Incense",
    category: "Base",
    description: "신성한 공간에 피어오르는 정적인 연기 향. 시간이 멈춘 듯한 신비로움과 명상적인 고요함을 선사합니다.",
    origin: "유향 및 나무 수지"
  }
];

// EOF: noteData.ts
