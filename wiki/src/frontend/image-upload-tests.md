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
corepack yarn install
```

단위 테스트:

```bash
cd frontend
corepack yarn test:run
```

E2E 테스트:

```bash
cd frontend
corepack yarn test:e2e
```

`test:e2e`는 내부적으로 `yarn build && playwright test`를 실행한다.

현재 확인된 결과:

- TypeScript build 통과
- Vite production build 통과
- Vitest `uploadService` 테스트 통과
- Playwright image upload E2E 2개 통과
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
uploadLogs: 2
cloudSuccessLogs: 2
apiRequests: 2
```

판정:

- 빠른 중복 drop은 실제로 중복 처리된다.
- `ImageUploader`에 처리 중 가드가 없어 `processImage()`가 동시에 두 번 진입할 수 있다.
- 결과적으로 `AIInterviewSection.handleImageProcessed()`도 두 번 호출되고 분석 API 요청도 두 번 발생한다.

## Findings

실제 확인된 항목:

- 부모 `div onClick`과 내부 `input.click()` 조합은 부모 click handler를 2번 실행시킨다.
- 빠른 중복 drop은 업로드와 분석 API 요청을 중복 실행한다.
- `AIInterviewSection`의 progress timer도 `handleImageProcessed()`가 두 번 들어오면 두 개 생성될 수 있다.

실제 확인되지 않은 항목:

- 파일 선택창이 클릭 1회로 두 번 뜨는 현상
- 일반적인 파일 선택 1회에서 `onChange`가 두 번 발생하는 현상
- `React.StrictMode`가 이 중복 API 요청의 직접 원인이라는 증거

## Recommended Regression Checks

이미지 업로드 중복 방지 수정 후에는 다음 조건을 다시 확인한다.

- 파일 선택 1회: 업로드 1회, 분석 API 1회
- 빠른 double drop: 업로드 1회, 분석 API 1회
- 분석 중 재선택 또는 drop: 기존 분석이 끝나기 전 새 분석 요청이 시작되지 않음
- retry: 의도적으로 재시도할 때만 분석 API 1회 호출

현재 double drop E2E는 현 상태를 문서화하기 위해 `apiRequests.length === 2`를 기대한다. 중복 방지 수정 후에는 해당 기대값을 `1`로 바꿔 회귀 테스트로 전환한다.
