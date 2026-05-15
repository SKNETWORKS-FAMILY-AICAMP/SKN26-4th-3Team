# 04. Core Implementation Guide

이 파트는 프론트엔드 핵심 기능이 실제로 어떻게 구현되어 있는지 설명합니다. 발표에서는 “이미지를 입력받아 분석 요청을 보내고, 추천 결과를 리포트와 모달로 보여주는 전체 파이프라인”을 중심으로 말하면 됩니다.

## 전체 기능 흐름

```text
개인정보 동의
  -> 향기 노트 선택
  -> OOTD 이미지 업로드
  -> 이미지 검증 및 리사이징
  -> AI 분석 API 요청
  -> 분석 결과 저장
  -> 향기 리포트와 추천 리스트 렌더링
  -> 상품 상세 모달 또는 리포트 이미지 저장
```

## 1. 개인정보 동의와 세션 흐름

`App.tsx`는 사용자가 개인정보 동의 전에는 전체 화면을 blur 처리하고 상호작용을 막습니다.

```tsx
<div className={`transition-all duration-700 ${
  !hasConsented ? "blur-xl scale-[1.02] pointer-events-none select-none" : "blur-0"
}`}>
```

동의 시에는 `crypto.randomUUID()`로 익명 세션 ID를 만들고 `localStorage`에 저장합니다. 이후 API 요청 interceptor가 이 값을 `X-Session-ID` 헤더로 넣습니다.

발표 포인트:

- 사용자가 분석 기능을 쓰기 전에 동의 과정을 먼저 거치게 했다.
- 세션 ID는 인증이 아니라 익명 요청 추적용이다.
- 동의 여부는 새로고침 후에도 유지되도록 로컬 저장소와 연결했다.

## 2. 이미지 업로드와 전처리

이미지 업로드는 `ImageUploader.tsx`가 담당합니다. 단순히 파일을 받는 것이 아니라, 분석 API에 보내기 전에 여러 안전장치를 둡니다.

구현 포인트:

- MIME 타입 allowlist: `image/jpeg`, `image/png`, `image/webp`
- 확장자 allowlist: `jpg`, `jpeg`, `png`, `webp`
- Magic Number 검사로 확장자 위조 방지
- 10MB 파일 크기 제한
- 이미지 해상도 상한선 4096px 검사
- canvas 기반 1200px 리사이징
- JPEG quality 0.9로 base64 변환
- `useRef` 기반 동기 lock으로 중복 업로드 진입 방지

중복 요청 방지는 React state만으로 처리하지 않고 `uploadProcessingRef`를 사용합니다. state 업데이트는 비동기라서 아주 짧은 시간 안에 이벤트가 두 번 들어오면 늦을 수 있기 때문입니다.

```ts
if (uploadProcessingRef.current || isUploading || isAnalyzing) return;
uploadProcessingRef.current = true;
```

발표 포인트:

- 클라이언트 검증은 보안의 전부가 아니라 사용자 경험과 1차 방어다.
- 실제 보안은 백엔드에서도 반복 검증해야 한다.
- 이미지 원본을 그대로 보내지 않고 크기와 용량을 줄여 네트워크 비용을 줄인다.

## 3. 분석 요청과 공통 API 처리

API 통신은 `frontend/src/services/api.ts`에서 Axios 인스턴스로 관리합니다.

```ts
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});
```

Request interceptor는 세션 ID를 헤더에 넣고, Response interceptor는 공통 에러를 Zustand store에 저장합니다.

```ts
api.interceptors.request.use((config) => {
  const sessionId = localStorage.getItem("olfit_session_id");
  if (sessionId) {
    config.headers["X-Session-ID"] = sessionId;
  }
  return config;
});
```

분석 요청은 `requestAuraAnalysis(base64Image, selectedNotes)`로 추상화했습니다.

발표 포인트:

- 컴포넌트 안에 `axios.post()`를 직접 흩뿌리지 않고 서비스 함수로 모았다.
- 로딩과 에러 처리를 공통화해 UI에서 같은 상태를 바라보게 했다.
- 환경 변수 `VITE_API_URL`로 로컬과 배포 API 주소를 분리할 수 있다.

## 4. AIInterviewSection의 분석 진행 상태

`AIInterviewSection.tsx`는 업로드 완료 직후 자동으로 분석을 시작하지 않습니다. 사용자가 업로드된 이미지를 미리 확인한 뒤 `분석 시작` 버튼을 눌렀을 때만 분석 흐름이 시작됩니다.

분석 중에는 두 종류의 대기 UI가 조건부로 표시됩니다.

- `ImageUploader` 미리보기 위에는 `Analyzing your style...` overlay가 표시된다.
- `AIInterviewSection` 하단에는 `isLoading` 동안 progress bar와 분석 단계 문구가 표시된다.

따라서 시연에서 이 화면을 못 봤다면 업로드만 완료하고 `분석 시작`을 누르기 전이었거나, 해당 구간이 빠르게 지나갔거나, API 오류 상태로 바로 전환된 경우일 수 있습니다.

중복 분석 요청을 막기 위해 이 컴포넌트도 `processingRef`를 사용합니다.

```ts
if (processingRef.current || isComplete) return;
processingRef.current = true;
```

진행률은 실제 백엔드 처리율이 아니라 사용자가 현재 어떤 단계를 기다리는지 이해할 수 있게 하는 UX용 progress입니다. 현재 구현에서는 약 5초 동안 분석 단계 문구를 보여준 뒤, 100% 도달 시 `requestAuraAnalysis()`를 1회 호출합니다.

- 이미지 픽셀 데이터 추출
- 스타일 실루엣 및 텍스처 분석
- 색채 심리 기반 무드 매칭
- 선택 노트와 스타일 결합
- 향기 아우라 생성 완료

100% 도달 후 API 응답을 기다리는 동안에는 랜덤 향기 팁이 아니라 고정된 마무리 상태 문구가 순환 표시됩니다.

- 아우라 분석 결과를 정리하는 중
- 추천 향수 데이터를 불러오는 중
- 제품 이미지와 상세 정보를 준비하는 중
- 리포트 화면을 구성하는 중

발표 포인트:

- 비동기 분석은 사용자가 멈춘 화면처럼 느끼기 쉬우므로, `분석 시작` 이후의 대기 상태를 시각화했다.
- API 호출은 state callback 내부가 아니라 progress 100% 도달 시점의 명확한 분기에서 1회만 수행한다.
- API pending 중에는 finalizing 문구를 순환 표시해 대기 지루함을 줄인다.

주의해서 말할 점:

- 현재 progress는 실제 서버 처리율이 아니라 데모/UX용 대기 표현이다.
- 현재 구현은 progress가 끝난 뒤 API를 호출하므로 사용자는 `5초 UX 대기 + 실제 API 응답 시간`을 기다릴 수 있다.
- 랜덤 향기 팁 기능은 현재 코드에 없다. 현재는 고정 finalizing 문구 순환 방식이다.
- 운영 개선 기준으로는 `분석 시작` 직후 API를 바로 호출하고, API pending 동안 progress 또는 loading indicator를 보여주는 구조가 더 자연스럽다.

## 5. 추천 결과와 fallback 로직

리포트 데이터 파생 로직은 `useInsightReport.ts`에 모여 있습니다.

우선순위는 다음과 같습니다.

1. 백엔드가 `results.recommendations`를 내려주면 그 결과를 우선 사용한다.
2. 추천 결과가 없으면 `recommendationEngine.ts`의 로컬 fallback 추천을 사용한다.

로컬 fallback은 다음 정보를 조합합니다.

- 사용자가 직접 선택한 향기 노트
- 백엔드가 변환한 향수 키워드
- 이미지에서 나온 무드 텍스트
- 상품의 notes, family, story, top/middle/base notes

점수 계산은 후각 매칭과 키워드 매칭에 가중치를 부여하고, 최종적으로 상위 5개를 추천합니다.

발표 포인트:

- 프론트엔드는 백엔드 추천을 우선 신뢰한다.
- 백엔드 결과가 없을 때도 화면이 비지 않도록 fallback 추천을 둔다.
- 추천 사유 `matchReason`을 만들어 단순 리스트가 아니라 설명 가능한 추천 UI로 보여준다.

## 6. 리포트 시각화와 정렬

`InsightReportSection.tsx`는 리포트 화면의 컨테이너이고, 복잡한 계산은 `useInsightReport.ts`로 분리되어 있습니다.

주요 파생 데이터:

- `slots`: 사용자가 선택한 Top/Middle/Base 향 노트
- `matchPercent`: 가장 높은 추천 상품의 유사도
- `currentRadarData`: 레이더 차트용 5축 데이터
- `dynamicLogicSteps`: 분석 과정 설명 문구
- `recommendations`: 추천순 또는 가격순으로 정렬된 상품 리스트

가격 정렬은 화면 표시용 문자열 `price`가 아니라 숫자 필드 `price_krw`를 사용합니다. 원화, 달러, 유로 같은 표시 문자열을 직접 파싱하면 오류가 생기기 쉽기 때문입니다.

## 7. 리포트 이미지 저장

`reportCapture.ts`는 `html2canvas`로 리포트 DOM을 PNG 이미지로 변환합니다.

디테일하게 처리한 부분:

- 폰트 로딩 완료 대기
- 이미지 로딩 완료 대기
- 외부 이미지 CORS 문제 시 placeholder로 대체
- 캡처용 clone DOM에 애니메이션 제거 스타일 주입
- 캡처 제외 요소 제거
- 정렬 버튼과 배지를 canvas로 다시 그려 캡처 품질 보정
- 중복 저장 클릭 방지를 위한 모듈 레벨 lock

발표 포인트:

- 화면을 그대로 캡처하면 애니메이션, 외부 이미지, 반응형 요소 때문에 결과가 깨질 수 있다.
- 그래서 캡처 전용 DOM 보정 로직을 넣어 일관된 고해상도 리포트를 만들었다.

## 발표 마무리 문장

Olfit 프론트엔드의 핵심은 단순 화면 구현이 아니라, 사용자 입력부터 백엔드 분석, 추천 결과, 공유 가능한 리포트까지 이어지는 하나의 데이터 흐름을 안정적으로 연결한 점입니다.
