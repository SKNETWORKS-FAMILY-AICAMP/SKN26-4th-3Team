# Olfit (올핏) - 나만의 향기 분석 플랫폼

> **"당신의 페르소나를 향기로 완성하다"**
>
> Olfit은 AI 기반의 인터뷰를 통해 사용자의 성향과 취향을 분석하고, 그에 최적화된 향수와 라이프스타일을 제안하는 큐레이션 플랫폼입니다.

---

## 🔗 Live Demo
**[https://olfit-front.vercel.app/](https://olfit-front.vercel.app/)**

---

## 🚀 프로젝트 개요
Olfit은 단순히 향수를 판매하는 것을 넘어, 사용자의 내면(Persona)을 탐구하고 이를 감각적인 경험으로 연결합니다. 세련된 인터페이스와 부드러운 애니메이션을 통해 프리미엄한 브랜드 경험을 제공합니다.

- **목적**: 사용자 맞춤형 향기 분석 및 큐레이션 서비스 제공
- **주요 타겟**: 자신의 취향을 깊게 탐구하고 감각적인 소비를 지향하는 사용자
- **핵심 가치**: 전문성, 개인화, 감각적 경험

## 🛠 Tech Stack
포트폴리오로서 기술적 역량을 보여주기 위해 현대적인 프론트엔드 스택을 활용하였습니다.

### Core
- **Framework**: React 19 (TypeScript)
- **Build Tool**: Vite
- **Routing**: React Router 7

### Styling & UI
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn UI (Radix UI 기반)
- **Icons**: Lucide React
- **Animations**: Tailwind Animate & CSS Transitions

### Utilities
- **State Management**: React Hook Form, Zod (Form Validation)
- **Visualization**: Recharts (데이터 시각화 리포트)
- **Interactions**: Embla Carousel (슬라이드 구현)

---

## ✨ Key Features
1. **AI Interview Section**: 대화형 UI를 통해 사용자의 성향을 파악하는 몰입형 분석 프로세스
2. **Scent Guide**: 우디, 플로럴 등 다양한 향기 패밀리에 대한 전문적인 정보 가이드
3. **Curated Selection**: 분석된 데이터를 바탕으로 한 맞춤형 제품 추천 큐레이션
4. **Insight Report**: 사용자의 취향을 데이터 시각화(Recharts)로 보여주는 개인화 리포트
5. **Safety & Values**: 브랜드가 추구하는 안전성과 철학을 감각적인 애니메이션으로 전달

---

## 🏃 Getting Started

### Prerequisites
- Node.js (v18 이상 권장)
- Yarn (추천) or npm

### Installation
```bash
# 저장소 클론
git clone https://github.com/JJonyeok2/persona_l_front.git

# 프로젝트 폴더로 이동
cd persona_l_front

# 의존성 설치 (Yarn 권장)
yarn install
```

### Development
```bash
# 로컬 개발 서버 실행
yarn dev
```
기본적으로 `http://localhost:5173`에서 실행됩니다.

### Build & Deployment
```bash
# 프로덕션 빌드
yarn build

# 빌드 결과물 미리보기
yarn preview
```

---

## 📂 Project Structure
```text
/
├── docs/             # 프로젝트 문서 및 발표 자료
├── tools/            # 데이터 수집(Crawler) 등 외부 도구
└── src/
    ├── components/
    │   ├── common/   # 공통 UI 컴포넌트
    │   ├── layout/   # Navigation, Footer 등 레이아웃
    │   ├── sections/ # 메인 페이지 섹션 컴포넌트
    │   └── ...       # 도메인별 컴포넌트 (curated, guide, report)
    ├── data/         # 정적 데이터 및 상수 (scent, product, personalData)
    ├── services/     # 비즈니스 로직 (추천 엔진 등)
    ├── hooks/        # 커스텀 훅
    ├── types/        # TypeScript 타입 정의
    └── App.tsx       # 메인 애플리케이션 로직
```

---

## ✒️ Author
- **Name**: 전종혁 (JJonyeok)
- **GitHub**: [@JJonyeok2](https://github.com/JJonyeok2)
