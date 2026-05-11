<<<<<<< HEAD
# Frontend

프론트엔드는 Vite, React, TypeScript, Tailwind CSS 기반으로 구성된다. 사용자는 이미지와 선호 노트를 입력하고, 백엔드 분석 결과를 카드, 리포트, 상세 모달에서 확인한다.

## Structure

주요 디렉터리는 다음 역할을 가진다.

- `e2e`: Playwright 기반 브라우저 E2E 테스트
- `src/components/sections`: 페이지 단위 섹션
- `src/components/report`: 분석 리포트와 추천 리스트 UI
- `src/components/curated`: 향수 상세 모달
- `src/components/common`: 공통 UI 컴포넌트
- `src/services`: 백엔드 통신, 추천 정규화, 리포트 캡처
- `src/test`: Vitest 공통 테스트 setup
- `src/store`: Zustand 기반 전역 상태
- `src/data`: 로컬 fallback 상품/노트 데이터
- `src/types`: 분석 결과 등 공유 타입

## Recommendation Adapter

백엔드 추천 결과는 `src/services/recommendationEngine.ts`의 `normalizeBackendRecommendation()`에서 UI용 `Product` 타입으로 변환된다.

이 adapter의 목적은 백엔드 응답 구조가 풍부해져도 기존 카드와 모달 컴포넌트가 같은 타입을 사용할 수 있게 하는 것이다.

현재 매핑 규칙은 다음과 같다.

- `rec.perfume`을 우선 원천 상세 정보로 사용한다.
- `perfume.koreanName`, `perfume.brand`, `perfume.price.raw`, `perfume.volume`을 상품 기본 정보로 매핑한다.
- `rec.imageDetail.base64` 또는 `rec.imageAsset.base64`가 있으면 data URL로 변환한다.
- `/static/...` 이미지 경로는 `VITE_API_URL`을 붙여 브라우저 접근 URL로 변환한다.
- `rec.details.topNotes/middleNotes/baseNotes`를 상세 모달의 Scent Pyramid에 우선 표시한다.
- 상세 노트가 없을 때만 대표 노트 문자열을 Top fallback으로 사용한다.

## Product Modal Contract

`ProductModal`은 `Product.details`의 다음 필드가 채워져 있다고 가정한다.

```ts
details: {
  story: string;
  topNotes: string;
  middleNotes: string;
  baseNotes: string;
  bestFor: string;
}
```

백엔드는 이 필드를 `recommendations[].details`에 내려주고, 프론트엔드는 해당 값을 그대로 `Product.details`로 연결한다. 이 계약 덕분에 향 노트가 모두 Top에 몰리거나 MID/BASE가 빈 행으로 표시되는 문제를 프론트에서 임의 보정하지 않아도 된다.

## Backend Fallback

로컬 fallback 추천 데이터도 여전히 지원한다. 백엔드 추천 배열이 없을 때는 `personalProducts`를 사용하고, 사용자가 선택한 노트와 백엔드 키워드 기반으로 간단한 유사도 점수를 계산한다.

백엔드 추천이 있는 경우에는 로컬 scoring을 사용하지 않고, 백엔드가 내려준 `similarity`와 `matchReason`을 우선한다.

## Verification

프론트엔드 변경 후에는 Corepack Yarn 기준으로 검증한다.

```bash
cd frontend
corepack yarn build
```

단위 테스트는 Vitest를 사용한다.

```bash
cd frontend
corepack yarn test:run
```

브라우저 이벤트와 업로드 흐름은 Playwright E2E로 확인한다. `test:e2e`는 production build 후 `dist`를 테스트 내부 HTTP 서버로 띄워 실행한다.

```bash
cd frontend
corepack yarn test:e2e
```

테스트 결과물은 Git에 포함하지 않는다.

- `frontend/test-results/`
- `frontend/playwright-report/`
=======
Using Node.js 20, Tailwind CSS v3.4.19, and Vite v7.2.4

Tailwind CSS has been set up with the shadcn theme

Setup complete: /mnt/agents/output/app

Components (40+):
  accordion, alert-dialog, alert, aspect-ratio, avatar, badge, breadcrumb,
  button-group, button, calendar, card, carousel, chart, checkbox, collapsible,
  command, context-menu, dialog, drawer, dropdown-menu, empty, field, form,
  hover-card, input-group, input-otp, input, item, kbd, label, menubar,
  navigation-menu, pagination, popover, progress, radio-group, resizable,
  scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner,
  spinner, switch, table, tabs, textarea, toggle-group, toggle, tooltip

Usage:
  import { Button } from '@/components/ui/button'
  import { Card, CardHeader, CardTitle } from '@/components/ui/card'

Structure:
  src/sections/        Page sections
  src/hooks/           Custom hooks
  src/types/           Type definitions
  src/App.css          Styles specific to the Webapp
  src/App.tsx          Root React component
  src/index.css        Global styles
  src/main.tsx         Entry point for rendering the Webapp
  index.html           Entry point for the Webapp
  tailwind.config.js   Configures Tailwind's theme, plugins, etc.
  vite.config.ts       Main build and dev server settings for Vite
  postcss.config.js    Config file for CSS post-processing tools
>>>>>>> 21e8744 (docs(wiki): move frontend notes into mdbook)
