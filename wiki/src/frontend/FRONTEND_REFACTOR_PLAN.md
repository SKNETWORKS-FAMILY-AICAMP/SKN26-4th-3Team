# Frontend Refactor Plan: Olfit Web Application

이 문서는 Olfit 프런트엔드 코드베이스의 현재 구조를 분석하고, 유지보수성, 성능, 그리고 타입 안정성을 향상시키기 위한 리팩토링 전략을 제안합니다.

---

## 1. 현재 구조 문제점 (Structural Issues)

### 1.1 "God Component" 경향
- `App.tsx`가 레이아웃 배치, 전역 상태 구독, 비즈니스 로직(개인정보 동의 핸들러 등)을 모두 포함하고 있어 파일이 비대해지고 책임이 과중됨.

### 1.2 평면적인 폴더 구조
- `src/components` 아래에 기능별 폴더가 있으나, 특정 도메인(예: Aura Analysis)에 종속된 훅, 서비스, 타입이 전역 폴더(`src/hooks`, `src/services`, `src/types`)에 흩어져 있어 응집도가 낮음.

### 1.3 중복되는 선언적 래퍼
- `App.tsx` 내에서 모든 섹션마다 `Suspense`와 `ErrorBoundary`를 반복적으로 감싸고 있어 가독성이 떨어짐.

---

## 2. 성능 문제 가능성 (Performance Bottlenecks)

### 2.1 Zustand Store 구독 최적화 부족
- `App.tsx` 및 주요 컴포넌트에서 `const { ... } = useOlfitStore();` 방식을 사용하여 스토어 전체를 구독함. 이는 스토어의 무관한 값이 변경되어도 컴포넌트 전체가 리렌더링되는 원인이 됨.
- **해결책**: Selector 패턴(`useOlfitStore(state => state.analysisResults)`) 도입 필요.

### 2.2 잦은 LocalStorage 접근
- `useStore.ts` 및 `App.tsx`에서 직접 `localStorage`에 접근함. 이는 동기적인 I/O 작업으로, 빈번한 상태 변화 시 미세한 성능 저하를 유발할 수 있으며 SSR(Server Side Rendering) 환경으로 확장 시 에러 유발 가능성이 있음.

---

## 3. React Anti-patterns

### 3.1 불필요한 Prop Drilling
- `App.tsx`에서 Zustand 스토어의 액션(`setSelectedNotes`, `setAnalysisResults`)을 직접 꺼내어 자식 컴포넌트에 전달함. 자식 컴포넌트에서 직접 스토어를 구독하거나, 더 좁은 범위의 context를 사용하는 것이 적절함.

### 3.2 컴포넌트 내 비즈니스 로직 결합
- `handleAgree`와 같은 로직이 UI 컴포넌트인 `App.tsx`에 존재함. 이러한 로직은 커스텀 훅(`useAuth` 등)이나 스토어 액션으로 이동해야 함.

### 3.3 혼재된 데이터 소스
- `RadarChart.tsx`와 같이 UI 컴포넌트가 `src/data`의 정적 데이터를 직접 import하면서 동시에 props로 데이터를 전달받는 구조는 데이터 흐름을 추적하기 어렵게 만듬.

---

## 4. 타입 안정성 문제 (Type Safety)

### 4.1 거대한 단일 타입 파일
- `src/types/index.ts` 하나에 모든 도메인 타입이 정의되어 있어 협업 시 충돌 가능성이 높고 관리가 어려움.

### 4.2 과도한 선택적 필드 (Optional Fields)
- `AnalysisResults` 인터페이스의 대부분이 `?`로 정의되어 있어, 실제 사용 시 `null` 체크나 비확정 타입 처리가 번거로움. 명확한 Union Type으로 상태를 분리(Loading | Success | Error)하는 것이 권장됨.

---

## 5. 개선 우선순위 (Prioritization)

1.  **High**: Zustand Selector 패턴 적용 (성능 최적화 및 불필요한 리렌더링 방지).
2.  **High**: 비즈니스 로직 분리 (App.tsx 정화 및 커스텀 훅 추출).
3.  **Medium**: Feature-based 구조 도입 (응집도 향상).
4.  **Medium**: 타입 정의 세분화 및 Domain-specific 타입 분리.
5.  **Low**: 공통 레이아웃 래퍼(Suspense/ErrorBoundary) 통합.

---

## 6. 리팩토링 단계 (Refactoring Steps)

### Step 1: 상태 관리 최적화
- `useOlfitStore`를 기능별로 쪼개거나(Slices), 사용하는 컴포넌트에서 개별 셀렉터를 사용하도록 수정.
- `localStorage` 접근 로직을 별도의 유틸리티로 추상화.

### Step 2: 디렉토리 구조 재편 (Feature-based)
```bash
src/
  features/
    auth/           # 개인정보 동의 및 세션 관리
    aura-analysis/  # AI 인터뷰 및 리포트 로직
    scent-guide/    # 향기 가이드 관련
  shared/
    components/     # 공통 UI (Button, Modal 등)
    hooks/
    utils/
```

### Step 3: API 레이어 강화
- `axios` 인터셉터 외에도 서비스별 클래스/함수를 정의하여 컴포넌트에서는 `useQuery` 패턴(또는 유사한 추상화)을 사용하여 데이터 패칭 로직을 숨김.

### Step 4: UI/UX 패턴 통일
- 섹션 로딩 및 에러 처리를 위한 `SectionWrapper` 고차 컴포넌트(HOC) 또는 래퍼 컴포넌트를 만들어 `App.tsx` 코드를 간결하게 유지.

---
**작성일**: 2026-05-13
**작성자**: Gemini CLI Agent
