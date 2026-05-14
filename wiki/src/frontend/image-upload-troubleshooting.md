# Image Upload Troubleshooting

## Symptom

이미지 업로드 후 다음 현상이 의심되거나 관측될 수 있다.

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

### 2. No in-flight guard in `ImageUploader`

`processImage(file)`는 이미지 리사이징과 업로드 시뮬레이션을 비동기로 실행한다. 하지만 함수 진입 시점에 이미 업로드 중인지 확인하는 동기 가드가 없다.

현재 흐름:

```tsx
const processImage = async (file: File) => {
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

- 빠른 double drop에서 `uploadToCloudStorage()` 2회 호출
- `/api/analyze/` 2회 호출

### 3. No in-flight guard in `AIInterviewSection`

`handleImageProcessed()`는 호출될 때마다 progress timer를 만들고 분석 API를 호출한다.

```tsx
const progressTimer = setInterval(() => {
  setProgress(...)
}, interval);

const results = await requestAuraAnalysis(base64, selectedNotes);
```

상위 `ImageUploader`가 중복으로 `onImageProcessed()`를 호출하면 이 함수도 중복 실행된다.

결과:

- progress timer가 두 개 생길 수 있다.
- `requestAuraAnalysis()`가 중복 호출될 수 있다.
- 먼저 끝난 요청과 나중에 끝난 요청이 상태를 덮어쓸 수 있다.

## Not Confirmed

### File chooser opens twice

테스트에서는 file chooser가 1번만 열렸다. 부모 click handler가 2번 실행되는 것과 file chooser가 2번 뜨는 것은 별개다.

### File input `onChange` fires twice on one selection

파일 선택 1회에서는 `change` 1회만 확인됐다.

### React StrictMode directly causes duplicate API requests

`frontend/src/main.tsx`에서 `StrictMode`는 켜져 있다. 하지만 테스트된 중복 API 요청은 이벤트 중복 진입과 in-flight guard 부재로 재현됐다.

StrictMode는 개발 환경에서 렌더링과 일부 effect를 의도적으로 반복할 수 있지만, 이번 케이스의 직접 원인으로 확인되지는 않았다.

## Recommended Fix

### 1. Replace parent click with a label or button

업로드 영역 전체를 클릭 가능하게 유지하려면 `label htmlFor`와 input `id`를 연결한다.

```tsx
<label htmlFor="ootd-image-input">
  ...
</label>
<input id="ootd-image-input" type="file" />
```

또는 부모 click handler에서 input-originated click을 무시한다.

```tsx
onClick={(event) => {
  if (event.target === fileInputRef.current) return;
  fileInputRef.current?.click();
}}
```

표준 접근성 측면에서는 label 방식이 더 낫다.

### 2. Add synchronous processing guard in `ImageUploader`

React state만으로는 같은 tick의 중복 이벤트를 막기 어렵다. `useRef`로 즉시 반영되는 lock을 둔다.

```tsx
const isProcessingRef = useRef(false);

const processImage = async (file: File) => {
  if (isProcessingRef.current || isAnalyzing) return;
  isProcessingRef.current = true;
  setIsUploading(true);

  try {
    // read, resize, upload
  } finally {
    isProcessingRef.current = false;
    setIsUploading(false);
  }
};
```

핵심은 FileReader 시작 전에 lock을 잡는 것이다.

### 3. Add in-flight guard in `AIInterviewSection`

`handleImageProcessed()`에도 별도 lock을 둔다. 업로더에서 막더라도 분석 섹션이 public callback boundary이므로 방어 로직을 갖는 것이 안전하다.

```tsx
const isAnalyzingRef = useRef(false);

const handleImageProcessed = async (base64: string, remoteUrl: string) => {
  if (isAnalyzingRef.current) return;
  isAnalyzingRef.current = true;

  try {
    // progress timer, requestAuraAnalysis
  } finally {
    isAnalyzingRef.current = false;
  }
};
```

### 4. Clear timers defensively

새 분석을 시작하기 전 이전 timer가 남아 있으면 정리한다. 컴포넌트 unmount 시에도 timer를 cleanup한다.

## Verification After Fix

수정 후 다음 결과가 나와야 한다.

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
corepack yarn test:run
corepack yarn test:e2e
```

`test:e2e`는 production build를 포함한다. 중복 방지 수정 후에는 `frontend/e2e/image-upload.spec.ts`의 rapid double drop 기대값을 현재 동작 기록용 `2`에서 회귀 검증용 `1`로 변경한다.
