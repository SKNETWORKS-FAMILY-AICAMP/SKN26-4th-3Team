# Image Upload Troubleshooting

## Symptom

이미지 업로드 후 다음 현상이 의심될 때 확인할 기준을 정리한다. 아래 중복 요청 문제는 과거 회귀 위험으로 관리하며, 현재 E2E 기준에서는 방지 동작이 검증되어 있다.

- 업로드 로직이 중복 실행된다.
- progress bar가 예상보다 빠르게 증가한다.
- `/api/analyze/` 요청이 두 번 발생한다.
- 분석 완료 콜백이 두 번 들어와 리포트 상태가 중복 갱신된다.

## Confirmed Root Causes

### 1. Parent click bubbling

`ImageUploader`의 업로드 영역은 부모 `div`에 click handler를 두고, 그 안에서 숨겨진 file input을 클릭한다.

```tsx
<div onClick={() => fileInputRef.current?.click()}>
  <input type="file" ref={fileInputRef} onChange={handleFileChange} />
</div>
```

브라우저 이벤트 흐름상 input click 이벤트가 부모로 bubble되어 부모 click handler가 한 번 더 실행될 수 있다.

확인 결과:

- 부모 click handler는 2번 실행됨
- file chooser는 1번만 열림
- input change도 1번만 발생함

따라서 이 구조는 좋지 않지만, 현재 테스트 기준으로 클릭 1회가 곧바로 분석 API 2회로 이어진 증거는 없다.

### 2. In-flight guard in `ImageUploader`

`processImage(file)`는 이미지 리사이징과 업로드 시뮬레이션을 비동기로 실행한다. 현재 구현은 함수 진입 시점에 동기 lock을 확인해 빠른 중복 drop을 차단한다.

현재 흐름:

```tsx
const processImage = async (file: File) => {
  if (uploadProcessingRef.current || isUploading || isAnalyzing) return;
  uploadProcessingRef.current = true;
  // validation
  const reader = new FileReader();
  reader.onload = async () => {
    // canvas resize
    setIsUploading(true);
    const remoteUrl = await uploadToCloudStorage(base64);
    setIsUploading(false);
    onImageProcessed(base64, remoteUrl);
  };
  reader.readAsDataURL(file);
};
```

`setIsUploading(true)`는 FileReader와 image load 이후에 실행된다. 그 전에 drop 또는 change 이벤트가 한 번 더 들어오면 두 번째 `processImage()`도 통과할 수 있다.

확인 결과:

- 빠른 double drop에서 `uploadToCloudStorage()` 1회 호출
- `/api/analyze/` 1회 호출

### 3. In-flight guard in `AIInterviewSection`

`handleImageProcessed()`는 progress timer를 만들고 분석 API를 호출한다. 현재 구현은 `processingRef`로 이미 분석 중인 경우 추가 진입을 차단한다.

```tsx
if (processingRef.current || isComplete) return;
processingRef.current = true;

const progressTimer = setInterval(() => {
  setProgress(...)
}, interval);

const results = await requestAuraAnalysis(base64, selectedNotes);
```

상위 `ImageUploader`가 중복 이벤트를 받더라도 분석 섹션에서 다시 한 번 방어한다.

결과:

- progress timer 중복 생성 위험을 낮춘다.
- `requestAuraAnalysis()`가 중복 호출되지 않도록 방어한다.
- 먼저 끝난 요청과 나중에 끝난 요청이 상태를 덮어쓰는 상황을 방지한다.

## Not Confirmed

### File chooser opens twice

테스트에서는 file chooser가 1번만 열렸다. 부모 click handler가 2번 실행되는 것과 file chooser가 2번 뜨는 것은 별개다.

### File input `onChange` fires twice on one selection

파일 선택 1회에서는 `change` 1회만 확인됐다.

### React StrictMode directly causes duplicate API requests

`frontend/src/main.tsx`에서 `StrictMode`는 켜져 있다. 하지만 테스트된 중복 API 요청은 이벤트 중복 진입과 in-flight guard 부재로 재현됐다.

StrictMode는 개발 환경에서 렌더링과 일부 effect를 의도적으로 반복할 수 있지만, 이번 케이스의 직접 원인으로 확인되지는 않았다.

## Current Guarding Strategy

### 1. Use native label/input behavior

업로드 영역은 native file input을 포함한 label 기반 구조로 관리한다. E2E에서는 숨겨진 input에 직접 `setInputFiles()`를 사용해 브라우저 file chooser 의존성을 줄인다.

```tsx
<label htmlFor="ootd-image-input">
  ...
</label>
<input id="ootd-image-input" type="file" />
```

### 2. Keep synchronous processing guard in `ImageUploader`

React state만으로는 같은 tick의 중복 이벤트를 막기 어렵다. `useRef`로 즉시 반영되는 lock을 둔다.

```tsx
const uploadProcessingRef = useRef(false);

const processImage = async (file: File) => {
  if (uploadProcessingRef.current || isUploading || isAnalyzing) return;
  uploadProcessingRef.current = true;
  setIsUploading(true);

  try {
    // read, resize, upload
  } finally {
    uploadProcessingRef.current = false;
    setIsUploading(false);
  }
};
```

핵심은 FileReader 시작 전에 lock을 잡는 것이다.

### 3. Keep in-flight guard in `AIInterviewSection`

`handleImageProcessed()`에도 별도 lock을 둔다. 업로더에서 막더라도 분석 섹션이 public callback boundary이므로 방어 로직을 갖는 것이 안전하다.

```tsx
const processingRef = useRef(false);

const handleImageProcessed = async (base64: string, remoteUrl: string) => {
  if (processingRef.current || isComplete) return;
  processingRef.current = true;

  try {
    // progress timer, requestAuraAnalysis
  } finally {
    // 성공 시 lock 유지, 실패 시 재시도를 위해 해제
  }
};
```

### 4. Clear timers defensively

새 분석을 시작하기 전 이전 timer가 남아 있으면 정리한다. 컴포넌트 unmount 시에도 timer를 cleanup한다.

## Verification After Fix

현재 E2E 기준은 다음 결과를 기대한다.

```text
single file selection:
  uploadLogs: 1
  apiRequests: 1

rapid double drop:
  uploadLogs: 1
  apiRequests: 1
```

또한 다음 명령이 모두 통과해야 한다.

```bash
cd frontend
yarn test:run
yarn test:e2e
```

`test:e2e`는 production build를 포함한다. 현재 `frontend/e2e/image-upload.spec.ts`의 rapid double drop 기대값은 회귀 검증용 `1`이다.
