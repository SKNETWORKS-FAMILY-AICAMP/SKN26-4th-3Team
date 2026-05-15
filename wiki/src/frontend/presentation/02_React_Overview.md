# 02. React + Vite Architecture

이 파트는 Olfit 프론트엔드가 어떤 구조로 화면을 만들고 데이터를 흘려보내는지 설명합니다. 핵심 메시지는 “React 컴포넌트로 화면을 나누고, Vite로 빠르게 개발하며, Zustand와 API 서비스로 상태 흐름을 단순하게 유지했다”입니다.

## React 기초 개념

React는 사용자 인터페이스를 컴포넌트 단위로 만드는 JavaScript 라이브러리입니다. 하나의 큰 HTML 파일을 직접 조작하는 대신, 화면을 독립적인 조각으로 나누고 데이터 상태에 따라 다시 렌더링합니다.

Olfit 화면도 다음처럼 역할별 컴포넌트로 나뉩니다.

- `HeroSection`: 첫 화면
- `ScentGuideSection`: 향기 노트 선택
- `AIInterviewSection`: 이미지 업로드와 AI 분석 요청
- `InsightReportSection`: 분석 결과 리포트
- `ProductModal`: 추천 향수 상세 정보

## React가 기존 DOM 조작과 다른 점

| 구분 | 직접 DOM 조작 | React 방식 |
| --- | --- | --- |
| 화면 변경 | 개발자가 DOM 요소를 직접 찾아 수정 | 상태가 바뀌면 React가 필요한 UI를 다시 계산 |
| 구조화 | 페이지가 커질수록 이벤트와 DOM 조작이 섞임 | 컴포넌트 단위로 역할 분리 |
| 데이터 전달 | 전역 변수나 직접 이벤트 연결이 늘어남 | props와 상태 관리 도구로 데이터 흐름 제어 |
| 재사용성 | 같은 UI를 복사하기 쉬움 | 같은 컴포넌트를 여러 위치에서 재사용 |

## Vite를 선택한 이유

Vite는 React 프로젝트의 개발 서버와 번들링을 담당하는 도구입니다. Olfit은 서버 사이드 렌더링보다 빠른 개발, 정적 번들 배포, 단일 페이지 사용자 경험이 중요했기 때문에 Vite 기반 CSR 구조가 적합했습니다.

프로젝트 설정은 `frontend/vite.config.ts`에서 확인할 수 있습니다.

```ts
export default defineConfig({
  base: './',
  plugins: [inspectAttr(), react()],
  server: {
    port: 3000,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

여기서 `@` alias를 `src`로 매핑해 `@/components/...`, `@/services/...`처럼 긴 상대 경로를 줄였습니다.

## 앱 조립 구조

최상위 파일은 `frontend/src/App.tsx`입니다. 이 파일은 전체 섹션을 조립하고, 개인정보 동의 여부, 분석 결과, 선택된 상품 모달 상태를 연결합니다.

Olfit은 주요 섹션을 `lazy()`로 불러옵니다.

```tsx
const AIInterviewSection = lazy(() => import("@/components/sections/AIInterviewSection"));
```

각 섹션은 `Suspense`와 `ErrorBoundary`로 감쌉니다.

- `Suspense`: lazy component가 준비될 때까지 렌더링 경계를 잡는다. 현재 구현은 별도 Skeleton 컴포넌트 없이 `fallback={null}`을 사용한다.
- `ErrorBoundary`: 특정 섹션에서 오류가 나도 전체 앱이 하얀 화면으로 멈추지 않게 한다.

이 구조의 장점은 초기 로딩 부담을 줄이고, 장애 범위를 섹션 단위로 제한한다는 점입니다.

## 상태 관리: Zustand

Olfit은 `frontend/src/store/useStore.ts`에서 Zustand 기반 전역 상태를 관리합니다.

주요 상태는 다음과 같습니다.

| 상태 | 역할 |
| --- | --- |
| `hasConsented` | 개인정보 동의 여부 |
| `selectedNotes` | 사용자가 선택한 향기 노트 |
| `analysisResults` | 백엔드 분석 결과 |
| `selectedProduct` | 현재 열린 상품 상세 모달 데이터 |
| `isLoading`, `error` | API 요청 상태 |
| `restartToken` | 재분석 시 섹션을 초기화하기 위한 키 |

개인정보 동의 여부와 세션 ID는 `localStorage`와 연결됩니다. 사용자가 동의하면 `App.tsx`에서 익명 세션 ID를 만들고 저장합니다.

```ts
const newSessionId = crypto.randomUUID();
localStorage.setItem("olfit_consent", "true");
localStorage.setItem("olfit_session_id", newSessionId);
```

이 값은 인증 수단이 아니라 분석 요청을 묶기 위한 익명 식별자입니다.

## 데이터 흐름

Olfit의 핵심 사용자 흐름은 다음 순서로 진행됩니다.

1. 사용자가 개인정보 수집에 동의한다.
2. `ScentGuideSection`에서 선호 향기 노트를 선택한다.
3. `AIInterviewSection`에서 OOTD 이미지를 업로드하고 분석을 시작한다.
4. `requestAuraAnalysis()`가 `/api/analyze/`로 이미지와 선택 노트를 보낸다.
5. 백엔드 결과가 `analysisResults`로 저장된다.
6. `InsightReportSection`이 결과를 기반으로 레이더 차트, 향기 설계도, 추천 리스트를 렌더링한다.
7. 사용자가 상품을 누르면 `ProductModal`이 열린다.

## 발표할 때 강조할 점

React는 “컴포넌트로 화면을 나누는 도구”이고, Vite는 “개발과 빌드를 빠르게 하는 도구”입니다. Olfit은 이 둘을 조합해 랜딩 페이지처럼 자연스럽게 스크롤되는 단일 페이지 앱을 만들고, Zustand로 전역 상태를 단순하게 연결했습니다.

## Q&A 방어 포인트

Q. Next.js를 쓰지 않은 이유는?

A. 이번 프론트엔드는 검색 엔진 노출보다 이미지 업로드, 분석, 리포트 인터랙션이 중심입니다. 서버 렌더링보다 빠른 개발 서버, 가벼운 번들, 클라이언트 상태 흐름이 중요했기 때문에 Vite + React가 적합했습니다.

Q. 전역 상태를 Redux 대신 Zustand로 쓴 이유는?

A. 상태 범위가 동의 여부, 선택 노트, 분석 결과, 모달 정도로 명확합니다. Zustand는 boilerplate가 적고 훅처럼 사용할 수 있어 프로젝트 규모에 맞게 단순하게 유지할 수 있었습니다.
