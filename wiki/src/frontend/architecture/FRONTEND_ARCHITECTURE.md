# Frontend Architecture Document

이 문서는 Olfit 웹 애플리케이션 프런트엔드(`frontend/src`)의 전체 아키텍처, 상태 관리, 데이터 흐름 및 UI 시스템을 설명합니다.

---

## 1. 주요 컴포넌트 역할 (Main Component Roles)

전체 애플리케이션은 기능 단위의 컴포넌트로 분리되어 있으며, 특히 `src/components` 하위에 역할별로 분류되어 있습니다.

- **`App.tsx` (Root/God Component)**
  - 애플리케이션의 최상단 컨테이너로, 전체 레이아웃 구성 및 라우팅(싱글 페이지 스크롤) 역할을 담당합니다.
  - 전역 상태(`useOlfitStore`)를 구독하고 개인정보 동의 여부(`hasConsented`)에 따른 렌더링을 제어합니다.
  - 성능 최적화를 위해 주요 섹션 컴포넌트들을 `lazy`와 `Suspense`로 지연 로딩하며, 각각을 `ErrorBoundary`로 감싸 장애 격리를 수행합니다.
- **`components/sections/` (Page Sections)**
  - **`HeroSection`**: 랜딩 페이지 첫 화면 비주얼.
  - **`PhilosophySection`**: 브랜드 철학 소개.
  - **`ScentGuideSection`**: 향기 노트 및 가이드를 제공하며, 사용자의 향기 취향(`selectedNotes`)을 수집.
  - **`AIInterviewSection`**: 이미지 업로드 및 AI 아우라 분석 요청을 처리(`ImageUploader` 포함).
  - **`InsightReportSection`**: 분석 결과(`AnalysisResults`)를 바탕으로 리포트 렌더링.
  - **`SafetyValuesSection`**: 제품 안전성 및 품질 보증 가치 소개.
- **`components/common/` (Shared UI & Utils)**
  - 재사용 가능한 범용 UI 컴포넌트 모음 (`RadarChart`, `ImageUploader`, `PrivacyConsentModal`, `LoadingSpinner`, `Skeleton` 등).
- **`components/report/` & `components/guide/`**
  - 특정 도메인(리포트 분석, 향기 가이드)에 특화된 하위 컴포넌트들. (`AuraAnalysis`, `ProductCarousel`, `ScentNoteCarousel` 등)

---

## 2. 상태 흐름 (State Flow)

프런트엔드의 전역 상태는 **Zustand**(`src/store/useStore.ts`)를 통해 단일 스토어로 관리됩니다.

- **`useOlfitStore` 주요 상태**:
  - `hasConsented`: 사용자의 개인정보 취급 방침 동의 여부 (초기값은 `localStorage`에서 확인).
  - `selectedNotes`: 사용자가 `ScentGuideSection`에서 선택한 선호 향기 목록.
  - `analysisResults`: `AIInterviewSection`에서 백엔드 API 호출 후 반환된 AI 분석 리포트 데이터.
  - `selectedProduct`: 리포트 결과 중 사용자가 클릭한 특정 상품 정보(모달 오픈 용도).
  - `isLoading`, `error`: API 요청의 전역 로딩 및 에러 상태.
- **상태 전파 (Prop Drilling vs Subscribe)**:
  - 현재 `App.tsx`가 스토어의 데이터와 액션을 가져와 각 섹션(`ScentGuideSection`, `AIInterviewSection`)에 Prop으로 내려주는 구조를 띠고 있습니다. (이는 리팩토링 단계에서 Selector 패턴으로 최적화될 예정입니다.)

---

## 3. 페이지 구조 (Page Structure)

- **Single Page Scroll Layout**
  - 라우터 패키지(`react-router`)가 존재하지만, 메인 플로우는 별도의 URL 이동 없이 단일 페이지 내에서 스크롤을 통해 각 섹션을 탐색하는 랜딩 페이지 형식입니다.
- **차단형 상호작용 (Gatekeeping)**
  - 초기 접속 시 개인정보 동의(`PrivacyConsentModal`)를 받기 전까지는 백그라운드를 블러 처리하고(`blur-xl`) 스크롤을 차단(`overflow-hidden`)하여 사용자 행동을 제한합니다.

---

## 4. UI 시스템 (UI System)

- **Styling**: `Tailwind CSS`를 사용하여 유틸리티 클래스 기반의 스타일링을 적용합니다.
- **UI Primitives**: `@radix-ui/react-*` 패키지들을 활용하여 접근성이 보장된 모달, 팝오버, 아코디언 등의 기본 UI 뼈대를 구성합니다 (shadcn/ui 패턴과 유사).
- **Animations & Interactivity**:
  - CSS Transition(`transition-all duration-700` 등)과 커스텀 훅 `useIntersectionObserver`를 사용하여 스크롤 시 화면에 컴포넌트가 나타날 때 애니메이션(Fade-in, Translate)을 적용합니다.
  - 데이터 시각화를 위해 SVG 기반의 `RadarChart`를 직접 구현하거나 `recharts`를 활용합니다.
- **Icons**: `lucide-react`를 표준 아이콘 라이브러리로 사용합니다.

---

## 5. 데이터 흐름 (Data Flow)

데이터는 정적(Static) 데이터와 동적(Dynamic) 데이터로 구분됩니다.

- **Static Data (`src/data/*.ts`)**
  - 향기 노트 정보(`noteData.ts`), 제품 매핑 정보(`productData.ts`), 리포트 시각화 레이아웃(`reportData.ts`) 등 변하지 않는 데이터는 별도의 파일로 분리되어 있습니다.
- **Dynamic Data (API 통신)**
  1. **사용자 입력**: 사용자가 선호 노트 선택(`selectedNotes`) 및 이미지(`base64Image`) 업로드.
  2. **API 요청**: `AIInterviewSection`에서 `services/api.ts`의 `requestAuraAnalysis()` 호출.
  3. **인터셉터 처리**: `axios` 인터셉터가 자동으로 `localStorage`의 `olfit_session_id`를 헤더에 주입하고, 에러 발생 시 Zustand 스토어의 `setError`를 호출하여 글로벌 에러를 처리합니다.
  4. **상태 업데이트**: API 성공 시 반환된 데이터(`AnalysisResults`)를 `useOlfitStore`에 저장.
  5. **리렌더링**: `App.tsx`의 `InsightReportSection`이 변경된 상태를 감지하여 렌더링.

---

## 6. 의존성 관계 (Dependency Relationships)

핵심 모듈 간의 의존성(의존 방향)은 다음과 같습니다.

```text
src/App.tsx
 ├──> src/store/useStore.ts (상태 구독 및 액션 호출)
 ├──> src/components/sections/* (레이아웃 조립)
 │     ├──> src/components/guide/ (향기 가이드 컴포넌트군)
 │     ├──> src/components/report/ (리포트 시각화 컴포넌트군)
 │     └──> src/services/api.ts (AI 분석 API 요청)
 └──> src/types/index.ts (공통 인터페이스 공유)

src/services/api.ts
 ├──> axios (HTTP 클라이언트)
 └──> src/store/useStore.ts (에러 및 로딩 상태 전파)

src/components/common/
 ├──> src/hooks/useIntersectionObserver.ts (애니메이션 뷰포트 감지)
 └──> src/data/* (기본 더미 데이터 폴백 용도)
```

- **절대 경로**: `tsconfig.json` 및 `vite.config.ts` 설정에 의해 `@/*` 를 `src/*` 에 매핑하여 깔끔한 의존성 참조를 유지하고 있습니다.
- **순환 참조 방지**: Zustand 스토어가 API 서비스 등을 직접 참조하지 않고, API 로직에서 스토어의 상태 갱신 함수(`getState()`)를 호출하는 단방향 흐름을 지향하고 있습니다.
