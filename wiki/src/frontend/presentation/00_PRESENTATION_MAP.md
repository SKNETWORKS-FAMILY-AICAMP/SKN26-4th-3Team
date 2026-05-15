# Frontend Presentation Map

이 문서는 조원별 발표 자료 제작을 위해 프론트엔드 내용을 파트별로 나눈 안내서입니다. 각 파트는 독립 발표가 가능하도록 구성하되, 전체 흐름은 하나의 사용자 여정으로 이어지게 설계했습니다.

## 발표 전체 흐름

1. 기술 스택을 왜 선택했는지 설명한다.
2. JavaScript/CSS와 TypeScript/Tailwind CSS의 차이를 기초 개념부터 비교한다.
3. React + Vite 구조 안에서 화면, 상태, API, 리포트가 어떻게 연결되는지 설명한다.
4. 이미지 업로드, 분석 요청, 추천 결과, 리포트 저장 같은 핵심 구현을 코드 기준으로 설명한다.
5. UI 디테일, 안정성 처리, 테스트 포인트를 발표 방어 자료로 정리한다.

## 추천 파트 분배

| 파트 | 담당 주제 | 참고 문서 | 발표 핵심 |
| --- | --- | --- | --- |
| 1 | TypeScript 선택 이유 | `01_JS_vs_TS.md` | 타입으로 API 계약과 UI 데이터 구조를 개발 단계에서 검증한다. |
| 2 | React + Vite 구조 | `02_React_Overview.md` | 컴포넌트 분리, lazy loading, Zustand 상태 흐름으로 SPA를 구성한다. |
| 3 | Tailwind CSS 선택 이유 | `03_CSS_and_Tailwind.md` | 유틸리티 클래스와 디자인 토큰으로 스타일 충돌을 줄이고 반응형 UI를 빠르게 만든다. |
| 4 | 핵심 기능 구현 | `04_Core_UI_and_Presentation_Guide.md` | 이미지 처리, API 요청, 추천 결과, 리포트 캡처가 어떤 흐름으로 동작하는지 설명한다. |
| 5 | UI 디테일과 Q&A | `05_ShadcnUI_and_TailwindCSS.md` | 브랜드 톤, 접근성 기반 UI 전략, 중복 요청 방지, 테스트 방어 포인트를 정리한다. |
| 6 | 질문 대응 전체 리스트 | `06_FRONTEND_QA_RESPONSE_LIST.md` | 기술 선택부터 한계와 개선 방향까지 예상 질문에 짧게 답한다. |
| 7 | 최신 UI 변경 요약 | `07_LATEST_UI_REFINEMENT_SUMMARY.md` | GitHub/발표용 최신 변경 요약을 정확한 표현으로 제공한다. |

## 발표용 한 문장 요약

Olfit 프론트엔드는 `TypeScript + React + Vite + Tailwind CSS`를 기반으로, 사용자의 이미지와 향기 취향을 안전하게 입력받고 백엔드 분석 결과를 리포트와 추천 UI로 시각화하는 단일 페이지 애플리케이션입니다.

## 코드 기준 확인 파일

| 범위 | 주요 파일 |
| --- | --- |
| 앱 조립과 섹션 lazy loading | `frontend/src/App.tsx` |
| 전역 상태 | `frontend/src/store/useStore.ts` |
| 공유 타입 | `frontend/src/types/index.ts` |
| API 통신 | `frontend/src/services/api.ts` |
| 이미지 업로드와 전처리 | `frontend/src/components/common/ImageUploader.tsx` |
| AI 분석 섹션 | `frontend/src/components/sections/AIInterviewSection.tsx` |
| 추천 및 리포트 파생 데이터 | `frontend/src/hooks/useInsightReport.ts` |
| 추천 fallback 로직 | `frontend/src/services/recommendationEngine.ts` |
| 리포트 이미지 저장 | `frontend/src/services/reportCapture.ts` |
| Tailwind 설정과 전역 스타일 | `frontend/tailwind.config.js`, `frontend/src/index.css` |
| 질문 대응 전체 리스트 | `wiki/src/frontend/presentation/06_FRONTEND_QA_RESPONSE_LIST.md` |
| 최신 UI 변경 요약 | `wiki/src/frontend/presentation/07_LATEST_UI_REFINEMENT_SUMMARY.md` |

## 주의할 표현

- 현재 코드는 AOS 라이브러리가 아니라 `IntersectionObserver` 기반 커스텀 훅으로 스크롤 진입 애니메이션을 처리한다.
- `components.json`과 Radix UI 의존성은 shadcn 스타일의 UI 구성을 위한 기반이지만, 현재 화면 대부분은 프로젝트 소유의 커스텀 컴포넌트로 구현되어 있다.
- 이미지 업로드의 클라우드 URL 반환은 현재 시뮬레이션이다. 실제 분석 요청은 `base64` 이미지를 백엔드로 전송하는 구조다.
- `X-Session-ID`는 프론트에서 생성한 익명 세션 식별자이므로 인증 수단이 아니라 요청 추적용 값으로 설명해야 한다.
