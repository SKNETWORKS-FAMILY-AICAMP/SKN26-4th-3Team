# Image Upload Tests

## Scope

`ImageUploader`와 `AIInterviewSection`에서 이미지 선택, 업로드 시뮬레이션, 분석 API 요청이 중복 실행되는지 확인했다.

대상 파일:

- `frontend/src/components/common/ImageUploader.tsx`
- `frontend/src/components/sections/AIInterviewSection.tsx`
- `frontend/src/services/uploadService.ts`
- `frontend/src/services/api.ts`

## Test Environment

- Unit test runner: Vitest
- Unit test DOM environment: jsdom
- Browser automation: Playwright
- E2E browser: Chromium
- Static serving: Node HTTP server inside `frontend/e2e/image-upload.spec.ts`
- API call interception: Playwright route interception for `**/api/analyze/`

테스트 중 실제 백엔드는 호출하지 않고 `/api/analyze/` 요청만 계측했다.

## Commands

의존성 설치:

```bash
cd frontend
yarn install
```

단위 테스트:

```bash
cd frontend
yarn test:run
```

E2E 테스트:

```bash
cd frontend
yarn test:e2e
```

`test:e2e`는 내부적으로 `yarn build && playwright test`를 실행한다.

현재 확인된 결과:

- TypeScript build 통과
- Vite production build 통과
- Vitest `uploadService` 테스트 통과
- Playwright image upload E2E 4개 통과
- Tailwind ambiguous class 경고와 chunk size 경고는 기존 경고이며 이미지 업로드 중복 이슈와 직접 관련 없음

## Test Cases

### 1. Minimal DOM click propagation

부모 `div`가 `onClick`에서 내부 file input의 `.click()`을 호출하는 최소 DOM을 만들고 클릭 이벤트 횟수를 측정했다.

구조:

```html
<div id="drop">
  <input id="file" type="file" style="display:none" />
  <span>click</span>
</div>
```

측정 결과:

```text
dropClicks: 2
inputClicks: 1
```

판정:

- 부모 click handler가 2번 실행되는 현상은 실제다.
- 원인은 input 클릭 이벤트가 부모로 bubble되기 때문이다.

### 2. Minimal DOM file chooser and change

같은 최소 DOM에서 file chooser와 change 이벤트 횟수를 측정했다.

측정 결과:

```text
chooserCount: 1
dropClicks: 2
inputClicks: 1
changes: 1
```

판정:

- 클릭 1회로 file chooser가 2번 뜨는 현상은 재현되지 않았다.
- 클릭 1회로 input `change`가 2번 발생하는 현상도 재현되지 않았다.

### 3. Actual app single file selection

`frontend/e2e/image-upload.spec.ts`에서 빌드된 실제 앱을 띄우고 file chooser를 통해 이미지 1개를 선택한다. `uploadToCloudStorage` console log와 `/api/analyze/` 요청 수를 계측한다.

측정 결과:

```text
uploadLogs: 1
cloudSuccessLogs: 1
apiRequests: 1
```

판정:

- 일반적인 파일 선택 1회는 정상이다.
- 이 경로에서는 업로드와 분석 요청이 중복 실행되지 않았다.

### 4. Actual app rapid double drop

`frontend/e2e/image-upload.spec.ts`에서 실제 앱의 drop 영역에 `drop` 이벤트를 거의 동시에 2번 dispatch한다.

측정 결과:

```text
uploadLogs: 1
apiRequests: 1
```

판정:

- 빠른 중복 drop은 현재 구현에서 중복 처리되지 않는다.
- `ImageUploader`의 동기 lock이 두 번째 drop 진입을 차단한다.
- `AIInterviewSection`의 분석 lock도 분석 요청 중복 실행을 방어한다.

### 5. Invalid file upload

텍스트 파일을 업로드하면 validation message가 표시되고 분석 요청은 발생하지 않는다.

측정 결과:

```text
validationMessage: JPG, PNG, WEBP 형식의 이미지만 업로드 가능합니다.
apiRequests: 0
```

판정:

- MIME 타입과 확장자 validation이 잘못된 파일을 차단한다.
- 유효하지 않은 파일은 `/api/analyze/` 요청으로 이어지지 않는다.

### 6. Recommendation modal

분석 응답에 추천 상품 fixture를 포함하고, 추천 카드 클릭 시 상세 모달을 확인한다.

측정 결과:

```text
modalTitle: 테스트 향수
brand: OLFIT
notes: 베르가못, 자스민, 머스크
image: visible
```

판정:

- 분석 결과에서 추천 카드가 렌더링된다.
- 추천 카드 클릭 시 상품명, 브랜드, 노트, 이미지가 포함된 상세 모달이 열린다.

## Findings

실제 확인된 항목:

- 부모 `div onClick`과 내부 `input.click()` 조합은 부모 click handler를 2번 실행시킨다.
- 현재 앱의 이미지 업로드 경로는 일반 파일 선택과 빠른 double drop 모두 업로드/분석 요청을 1회로 제한한다.
- 잘못된 파일 업로드는 validation message를 표시하고 분석 요청을 보내지 않는다.
- 추천 상품 카드는 상세 모달을 열고 상품명, 브랜드, 노트, 이미지를 표시한다.

실제 확인되지 않은 항목:

- 파일 선택창이 클릭 1회로 두 번 뜨는 현상
- 일반적인 파일 선택 1회에서 `onChange`가 두 번 발생하는 현상
- `React.StrictMode`가 이 중복 API 요청의 직접 원인이라는 증거

## Recommended Regression Checks

이미지 업로드 회귀 테스트는 다음 조건을 기준으로 유지한다.

- 파일 선택 1회: 업로드 1회, 분석 API 1회
- 빠른 double drop: 업로드 1회, 분석 API 1회
- 잘못된 파일 업로드: validation message 표시, 분석 API 0회
- 추천 카드 클릭: 상세 모달에 상품명, 브랜드, 노트, 이미지 표시
- 분석 중 재선택 또는 drop: 기존 분석이 끝나기 전 새 분석 요청이 시작되지 않음
- retry: 의도적으로 재시도할 때만 분석 API 1회 호출

현재 double drop E2E는 중복 방지 회귀 테스트로 운영하며 `apiRequests.length === 1`을 기대한다.
