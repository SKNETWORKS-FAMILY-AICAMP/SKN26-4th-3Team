# 💠 Olfit Frontend Technical Wiki

이 문서는 Olfit 프로젝트의 프론트엔드 구현 기술, 비즈니스 로직 및 아키텍처를 상세히 기록합니다. 일반적인 이론이나 백엔드 인프라 내용은 배제하고, 실제 코드 기반의 구현 디테일에 집중합니다.

---

## 🏗️ 1. Architecture & Core Implementation

### 1-1. 섹션 기반 지연 로딩 (Section-based Lazy Loading)
`App.tsx`에서 모든 메인 섹션을 `lazy()`로 선언하여 초기 번들 크기를 최소화하고, 각 섹션을 `Suspense`와 `ErrorBoundary`로 래핑하여 특정 섹션의 오류가 전체 앱에 영향을 주지 않도록 설계되었습니다.

```tsx
// App.tsx 구현 예시
const AIInterviewSection = lazy(() => import("@/components/sections/AIInterviewSection"));

<Suspense fallback={<SectionSkeleton />}>
  <ErrorBoundary fallbackMessage="인터뷰 섹션 오류">
    <AIInterviewSection />
  </ErrorBoundary>
</Suspense>
```

### 1-2. 상태 관리 및 영속성 (State Management with Zustand)
`src/store/useStore.ts`에서 전역 상태를 관리합니다. 특히 개인정보 동의(`hasConsented`)와 세션 ID는 `localStorage`와 연동되어 새로고침 후에도 상태가 유지됩니다.

*   **주요 상태**: `analysisResults` (AI 분석값), `selectedNotes` (사용자 선택 취향), `selectedProduct` (모달 상세 정보).
*   **특이사항**: 클라이언트 사이드에서 즉시 실행되는 IIFE를 통해 초기 상태를 결정합니다.

---

## 🧠 2. Core Business Logic (Services)

### 2-1. 지능형 추천 엔진 (`recommendationEngine.ts`)
백엔드에서 전달받은 AI 키워드와 사용자가 프론트엔드 UI에서 선택한 향기 노트를 결합하여 최적의 제품을 산출합니다.

*   **가중치 산정 로직**:
    1.  **후각 매칭 (Weight: 2)**: 사용자 선택 노트와 제품 성분 데이터 매칭.
    2.  **키워드 매칭 (Weight: 2)**: AI가 추출한 감성 키워드와 제품 스토리/계열 매칭.
    3.  **보조 매칭 (Weight: 1.5)**: 키워드 부재 시 분위기(시크, 로맨틱 등) 기반 자동 추천.
*   **유사도 보정 알고리즘**:
    *   정량적 점수를 백분율로 변환 후, `stableRandom` (제품 ID 기반의 고정 난수)을 더해 시각적으로 다채로운 유사도 수치(예: 94%, 87%)를 생성하여 사용자 신뢰도를 높임.

### 2-2. 리포트 캡처 및 공유 (`reportCapture.ts`)
`html2canvas` 라이브러리를 사용하여 사용자의 분석 결과 리포트를 이미지 파일로 변환합니다. DOM 요소의 스타일(Tailwind CSS 포함)을 캔버스로 래스터화하여 다운로드 기능을 제공합니다.

---

## 📂 3. Directory & File Roles

### `src/components/`
*   **`sections/`**: 서비스의 주요 단계를 담당하는 대형 컴포넌트.
    *   `AIInterviewSection.tsx`: 이미지 업로드 및 인터뷰 단계 제어.
    *   `InsightReportSection.tsx`: 결과 데이터 시각화 및 추천 리스트 렌더링.
*   **`report/`**: 결과 리포트 전용 UI 컴포넌트군.
    *   `ScentBlueprint.tsx`: 사용자 맞춤형 향기 설계도 구현.
    *   `AuraAnalysis.tsx`: Recharts를 이용한 취향 레이더 차트.
*   **`common/`**: 디자인 시스템 기반의 공통 요소 (Skeleton, Loading, Error).

### `src/services/`
*   `api.ts`: Axios 인스턴스 설정 및 백엔드 엔드포인트 통신 정의.
*   `uploadService.ts`: 이미지 바이너리 데이터 처리 및 서버 전송 로직.

### `src/data/`
*   `productData.ts` / `scentData.ts`: 서비스에 사용되는 제품 정보 및 향기 사전 등의 정적 데이터. UI 로직과 콘텐츠 데이터를 분리하여 유지보수성 확보.

---

## 🎨 4. UI/UX Implementation Details

*   **유동적인 레이아웃**: Tailwind CSS의 `transition`과 `blur` 유틸리티를 활용하여 개인정보 미동의 시 화면을 흐리게 처리하고 상호작용을 차단하는 인터랙티브 가드 구현.
*   **시각화 라이브러리 (Recharts)**: 사용자의 향기 스펙트럼을 다각형 차트로 표현하여 정성적인 취향을 정량적으로 시각화.
*   **에셋 최적화**: `public/` 디렉토리의 이미지들을 활용한 일관된 톤앤매너 유지.

---
*Last Updated: 2026-05-11*
