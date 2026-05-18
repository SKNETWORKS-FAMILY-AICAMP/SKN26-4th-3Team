# 05. UI Details, Radix/Shadcn Strategy, and Q&A

이 파트는 화면 완성도와 발표 방어 포인트를 정리합니다. 핵심 메시지는 “프론트엔드는 기능만 붙인 것이 아니라, 브랜드 경험, 안정성, 접근성, 테스트 가능성까지 고려했다”입니다.

## UI 시스템 방향

Olfit UI는 향수 추천 서비스에 맞게 에디토리얼하고 차분한 톤으로 구성했습니다.

주요 스타일 방향:

- `cream`, `wood`, `gold`를 중심으로 한 고정 브랜드 팔레트
- 얇은 border와 낮은 opacity로 가벼운 레이어 표현
- `rounded-sm` 중심의 절제된 모서리
- 큰 이미지, 여백, serif 계열 디스플레이 타이포그래피
- hover overlay, backdrop blur, loading overlay, progress 상태로 부드러운 전환

구현 위치:

- `frontend/tailwind.config.js`: 브랜드 색상, 폰트, 애니메이션, shadow 확장
- `frontend/src/index.css`: CSS 변수, 공통 컴포넌트 클래스, 전역 스크롤바, 텍스트 렌더링
- `frontend/src/components/common`: 공통 UI
- `frontend/src/components/report`: 리포트 전용 UI

## shadcn/Radix 전략

`frontend/components.json`에는 shadcn 스타일의 설정이 들어 있습니다. 또한 `package.json`에는 여러 `@radix-ui/react-*` 패키지가 포함되어 있습니다.

다만 현재 화면 대부분은 `src/components/ui`에 shadcn 컴포넌트를 대량 생성해 쓰는 방식이 아니라, 프로젝트 목적에 맞춘 커스텀 컴포넌트로 구성되어 있습니다.

발표에서는 다음처럼 설명하는 것이 정확합니다.

- Radix UI와 shadcn 스타일은 접근성 있는 headless primitive와 프로젝트 소유 컴포넌트를 만들기 위한 기반이다.
- MUI나 Ant Design처럼 강한 디자인을 가진 완성형 UI 라이브러리에 종속되지 않는다.
- Tailwind CSS와 잘 맞기 때문에 Olfit의 브랜드 색상, 간격, 모션을 직접 제어할 수 있다.
- 현재 구현은 custom component 중심이고, 복잡한 dialog/select/popover가 늘어날 경우 Radix 기반 컴포넌트를 확장할 수 있다.

## 기존 UI 라이브러리와의 차이

| 구분 | MUI/Ant Design 계열 | shadcn/Radix + Tailwind 계열 |
| --- | --- | --- |
| 디자인 | 라이브러리 기본 디자인이 강함 | 프로젝트 브랜드에 맞춰 직접 구성 |
| 컴포넌트 소유권 | 패키지 내부 구현에 의존 | 소스 코드를 프로젝트에서 소유하는 패턴 |
| 접근성 | 제공되지만 스타일 커스텀에 제약 가능 | Radix primitive로 접근성 로직을 가져오고 스타일은 직접 작성 |
| Olfit 적합성 | 빠른 관리자 페이지에 유리 | 감성적 브랜드 UI와 세밀한 커스텀에 유리 |

## 디테일 1: 개인정보 동의 UX

동의 전에는 `PrivacyConsentModal`을 띄우고, 뒤쪽 화면은 blur와 pointer-events 차단을 적용합니다.

사용자에게 중요한 이유:

- 이미지 분석 전에 개인정보 처리 흐름을 먼저 인지하게 한다.
- 동의하지 않은 상태에서 업로드 영역을 조작하지 못하게 한다.
- 단순 alert가 아니라 서비스 화면 위에 자연스럽게 쌓이는 모달 경험을 제공한다.

## 디테일 2: 이미지 업로드 안정성

이미지 업로드는 사용자가 가장 먼저 만나는 핵심 인터랙션입니다. 그래서 다음 상태를 명확히 나눴습니다.

- 업로드 전: drag & drop 영역
- 업로드 중: S3 업로드 시뮬레이션 overlay
- 분석 가능: `분석 시작` 버튼 활성화
- 분석 중: `분석 시작` 클릭 후 progress와 분석 단계 문구
- 오류: `ErrorFallback`과 retry 안내

중복 요청 방지는 `ImageUploader`와 `AIInterviewSection` 양쪽에서 처리합니다. 업로더에서 막더라도 분석 섹션은 callback boundary이므로 한 번 더 방어하는 구조입니다.

## 디테일 2-1: 최신 UI 문구와 상호작용 보정

최근 UI refinement에서는 발표에서 과장되지 않도록 실제 데이터와 실제 구현 기준으로 문구를 조정했습니다.

- `PhilosophySection`: `55,717+` 분석 데이터, `13+` 프리미엄 브랜드, `1,240+` 향수 아카이브 수치를 노출한다.
- `SafetyValuesSection`: 기존의 넓은 마케팅 문구보다 `IFRA 성분 가이드`, `브랜드 윤리성 공개`, `아우라 매칭 알고리즘`으로 확인 기준을 구체화했다.
- `FamilyCarousel`: 자동 전환 주기를 30초로 늘리고, hover/focus 시 좌우 이동 버튼을 노출하며, 수동 조작 시 타이머를 리셋한다.
- `AIInterviewSection`: 분석 100% 이후 API 응답 대기 동안 랜덤 팁이 아니라 고정된 마무리 상태 문구를 순환 표시한다.
- `RecommendationList`: 가격순 정렬은 표시 문자열이 아니라 `price_krw` 숫자 값을 기준으로 처리한다.

## 디테일 3: 리포트 UI

리포트는 단순 텍스트 결과가 아니라 사용자가 자신의 결과를 이해하고 저장할 수 있게 설계했습니다.

- `RadarChart`: SVG 기반 5축 향기 성향 시각화
- `ScentBlueprint`: Top/Middle/Base 향기 슬롯 시각화
- `AuraAnalysisSteps`: 분석 과정 문장화
- `RecommendationList`: 추천순/가격순 정렬과 추천 사유 표시
- `ProductModal`: 상품 이미지, 스토리, 노트 피라미드, 추천 상황 제공

## 디테일 4: 한글 UX

한글 문장은 영어보다 줄바꿈이 어색해지기 쉽습니다. 그래서 다음 처리를 사용했습니다.

- `break-keep`: 단어 단위 줄바꿈 유지
- `.text-balance`: 제목과 설명 문장의 줄 길이 균형
- `normalizeSubjectParticle()`: 상품명 뒤 조사 표현 보정
- 작은 uppercase label과 한국어 본문을 분리해 정보 위계를 명확히 함

## 디테일 5: 테스트와 검증 포인트

프론트엔드는 다음 테스트 도구를 사용합니다.

- TypeScript build: 타입 계약 검증
- Vitest: 훅과 서비스 로직 단위 테스트
- Playwright: 실제 브라우저 업로드 흐름 E2E 테스트
- ESLint: 사용하지 않는 변수, hooks 규칙 등 정적 검사

기본 검증 명령:

```bash
cd frontend
yarn build
yarn test:run
yarn test:e2e
```

## 발표 Q&A

Q. TypeScript를 쓰면 런타임 오류가 완전히 없어지나요?

A. 아닙니다. TypeScript는 개발 단계의 타입 오류를 줄이는 도구입니다. 서버에서 잘못된 JSON이 내려오는 문제는 API 계약, 테스트, 런타임 검증으로 추가 방어해야 합니다.

Q. Tailwind CSS는 그냥 className을 많이 쓰는 것 아닌가요?

A. 단순히 className이 많은 것이 아니라, 색상, 간격, 반응형, 상태 스타일을 표준 유틸리티로 조합하는 방식입니다. Olfit에서는 브랜드 팔레트와 반복 패턴을 설정 파일과 공통 컴포넌트로 관리했습니다.

Q. 분석 요청이 두 번 나가지 않게 어떻게 막았나요?

A. `ImageUploader`에서 업로드 처리 중인지 `useRef` lock으로 막고, `AIInterviewSection`에서도 분석 진행 중인지 별도 `processingRef`로 막습니다. React state는 반영 시점이 늦을 수 있어 중복 클릭이나 빠른 drop 이벤트를 즉시 막는 데 ref가 더 적합합니다.

Q. 리포트 캡처가 왜 별도 서비스로 분리되어 있나요?

A. DOM 캡처는 폰트, 이미지 CORS, 애니메이션, 반응형 layout 영향을 많이 받습니다. 그래서 `reportCapture.ts`에서 캡처 전용 보정 로직을 모아 리포트 컴포넌트와 분리했습니다.

Q. 현재 이미지가 실제 S3에 올라가나요?

A. 현재 `uploadToCloudStorage()`는 클라우드 업로드를 시뮬레이션하고 fake URL을 반환합니다. 실제 분석 요청은 base64 이미지를 백엔드로 보내는 구조입니다. 발표에서는 “향후 실제 스토리지 연동을 고려한 구조”라고 설명하는 것이 정확합니다.

## 마무리 강조 문장

Olfit 프론트엔드는 TypeScript로 데이터 계약을 안정화하고, Tailwind CSS로 브랜드 UI를 빠르게 구현했으며, 이미지 업로드부터 리포트 캡처까지 사용자가 체감하는 흐름의 안정성과 디테일을 함께 챙긴 구조입니다.
