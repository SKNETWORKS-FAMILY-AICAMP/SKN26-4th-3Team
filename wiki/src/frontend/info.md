# Frontend

프론트엔드는 Vite, React, TypeScript, Tailwind CSS 기반으로 구성된다. 사용자는 이미지와 선호 노트를 입력하고, 백엔드 분석 결과를 리포트, 추천 리스트, 상세 모달에서 확인한다.

## Structure

주요 디렉터리는 다음 역할을 가진다.

- `e2e`: Playwright 기반 브라우저 E2E 테스트
- `src/components/sections`: 페이지 단위 섹션
- `src/components/report`: 분석 리포트와 추천 리스트 UI
- `src/components/curated`: 향수 상세 모달
- `src/components/common`: 공통 UI 컴포넌트
- `src/services`: 백엔드 통신, 추천 fallback, 리포트 캡처, 업로드 처리
- `src/hooks`: 리포트 파생 데이터, 스크롤 감지 등 커스텀 훅
- `src/store`: Zustand 기반 전역 상태
- `src/data`: 로컬 fallback 상품/노트 데이터
- `src/types`: 분석 결과와 상품 등 공유 타입

## Main Flow

1. `App.tsx`가 개인정보 동의 모달과 전체 섹션을 조립한다.
2. `ScentGuideSection`에서 선택한 향기 노트가 Zustand store의 `selectedNotes`로 저장된다.
3. `AIInterviewSection`에서 `ImageUploader`를 통해 이미지를 검증, 리사이징, base64 변환한다.
4. `services/api.ts`의 `requestAuraAnalysis()`가 `/api/analyze/`로 이미지와 선택 노트를 전송한다.
5. 응답 결과는 `analysisResults`로 저장되고 `InsightReportSection`이 리포트를 렌더링한다.
6. 추천 상품 클릭 시 `ProductModal`이 상세 스토리와 노트 피라미드를 보여준다.

## Type and API Contract

공유 타입은 `src/types/index.ts`에 모은다.

- `Product`: 상품 카드, 추천 리스트, 상세 모달에서 공통으로 사용하는 상품 타입
- `AnalysisResults`: 백엔드 분석 결과와 리포트 UI가 공유하는 결과 타입
- `analysisMetadata`: 원본 이미지, 선택 노트, 레이더 점수 등 분석 메타데이터

프론트엔드는 백엔드가 `recommendations`를 내려주면 이를 우선 사용한다. 추천 배열이 없을 때만 `src/services/recommendationEngine.ts`의 로컬 fallback 추천을 사용한다.

## Report and Recommendation

`src/hooks/useInsightReport.ts`는 리포트 화면에서 필요한 파생 데이터를 계산한다.

- 추천 목록 정렬: 추천순 또는 `price_krw` 기반 가격순
- 향기 슬롯: 사용자가 선택한 Top/Middle/Base 노트 매핑
- 레이더 차트 데이터: 백엔드 `radarScores` 우선, 없으면 fallback 값 사용
- 공유 기능: `reportCapture.ts`를 호출해 리포트 DOM을 PNG로 저장

## UI System

스타일은 Tailwind CSS를 중심으로 구성한다.

- 브랜드 색상과 animation은 `tailwind.config.js`에서 확장한다.
- CSS 변수, 공통 유틸리티, 스크롤바, 텍스트 렌더링은 `src/index.css`에서 관리한다.
- Radix UI와 shadcn-style 설정은 접근성 있는 UI primitive를 확장하기 위한 기반이며, 현재 화면 대부분은 프로젝트 소유 커스텀 컴포넌트로 구현되어 있다.

## Verification

프론트엔드 변경 후에는 Corepack Yarn 기준으로 검증한다.

```bash
cd frontend
yarn build
```

단위 테스트는 Vitest를 사용한다.

```bash
cd frontend
yarn test:run
```

브라우저 이벤트와 업로드 흐름은 Playwright E2E로 확인한다. `test:e2e`는 production build 후 Playwright를 실행한다.

```bash
cd frontend
yarn test:e2e
```

테스트 결과물은 Git에 포함하지 않는다.

- `frontend/test-results/`
- `frontend/playwright-report/`
