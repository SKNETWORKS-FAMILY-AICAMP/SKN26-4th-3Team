# Frontend QA & Code Review

Date: 2026-05-15

Scope: `frontend` folder only. This review covers security risk, functional correctness, QA coverage, accessibility, and build/test health.

## Executive Summary

Critical security issues such as hardcoded secrets, `eval`, `new Function`, arbitrary script execution, or user-controlled `innerHTML` were not found in the current frontend code path.

The main risks are functional and QA-related:

- `price_krw` was added to the sort logic, but product data does not populate it, so price sorting currently has no effective behavior.
- E2E tests are stale and fail against the current upload UX, so CI would not reliably protect image upload and duplicate request behavior.
- The upload flow presents a simulated S3/cloud upload, but the returned URL is ignored and the backend request still sends the base64 image directly.
- Several clickable UI regions are implemented as non-keyboard-accessible `div`s.

## QA Commands

| Command | Result | Notes |
| --- | --- | --- |
| `yarn install --frozen-lockfile` | Pass | Local `node_modules` initially missed dev deps such as `vitest`; lockfile install fixed it. |
| `yarn lint` | Pass | No ESLint errors. |
| `yarn test:run` | Pass | 1 test passed: `src/services/uploadService.test.ts`. |
| `yarn build` | Pass | Build completed. Tailwind emitted ambiguous-class warnings for `duration-[3000ms]` and `ease-[cubic-bezier(...)]`. |
| `yarn test:e2e` | Fail | 2 Playwright tests failed because the tests no longer match current UI/flow. |
| `yarn audit --level moderate` | Pass | 0 vulnerabilities found across 667 packages. |

## Findings

### High: Price Sorting Is Effectively Broken

Files:

- `frontend/src/hooks/useInsightReport.ts:60`
- `frontend/src/types/index.ts:19`
- `frontend/src/data/personalData.ts:3`

`useInsightReport` now sorts by `price_krw`, but `price_krw` is optional and no current product entries define it. As a result, every local product falls back to `0`, so `가격순` preserves the recommendation order instead of sorting by price.

Recommended fix:

- Populate `price_krw` for every product, or
- Use `price_krw ?? parsePrice(product.price)` as a fallback, and add a unit test for price sorting.

### High: E2E Tests Are Out Of Sync With Current Upload UX

Files:

- `frontend/e2e/image-upload.spec.ts:88`
- `frontend/e2e/image-upload.spec.ts:128`
- `frontend/src/components/common/ImageUploader.tsx:261`
- `frontend/src/components/common/ImageUploader.tsx:318`

The first E2E test waits for text `Drag & Drop or Click to browse`, but the app renders `Click to browse or Drag & Drop`. More importantly, the test expects analysis immediately after selecting a file, while the current app requires clicking `분석 시작`.

The second E2E test expects duplicate rapid drops to create 2 API requests. Current code has an upload lock and also requires the analysis button, so the test receives 0 requests.

Recommended fix:

- Update E2E selectors to stable roles/test IDs instead of exact marketing text.
- Reflect the current flow: select/drop file, wait for upload completion, click `분석 시작`, then assert exactly 1 API request.
- Replace the duplicate test expectation with the desired behavior: rapid double drop should not create duplicate uploads or duplicate analysis requests.

### Medium: Upload Flow Claims Cloud/S3 Upload But Sends Base64 To Backend

Files:

- `frontend/src/services/uploadService.ts:11`
- `frontend/src/components/common/ImageUploader.tsx:161`
- `frontend/src/components/sections/AIInterviewSection.tsx:43`
- `frontend/src/services/api.ts:47`

`uploadToCloudStorage` is a simulation that returns a fake S3 URL. `ImageUploader` passes `(base64, remoteUrl)`, but `AIInterviewSection` only accepts `base64` and ignores the remote URL. The final API request sends the base64 image directly to `/api/analyze/`.

This is not an exploit by itself, but it is a privacy/architecture mismatch. The UI says the image is being uploaded to S3/a secure server, while the code path uses a fake URL and sends full image content to the analysis API.

Recommended fix:

- Decide on the real contract: backend receives base64, or backend receives a storage URL.
- If storage URL is intended, implement real upload and send only the URL/token to analysis.
- If base64 is intended, remove S3 wording and fake URL plumbing.

### Medium: Keyboard Accessibility Gaps In Clickable Cards/Regions

Files:

- `frontend/src/components/report/ProductCarousel.tsx:56`
- `frontend/src/components/guide/NoteGlossary.tsx:61`
- `frontend/src/components/guide/ScentNoteCarousel.tsx:192`
- `frontend/src/components/common/ScentPyramid.tsx:39`

Several interactive areas use `div onClick` without keyboard handling, `role`, or focusability. Mouse users can interact, but keyboard and assistive technology users may not be able to select products or scent notes.

Recommended fix:

- Prefer native `<button>` for interactive regions.
- If a `div` must remain, add `role="button"`, `tabIndex={0}`, and Enter/Space key handling.

### Medium: Client-Generated Session ID Must Not Be Trusted Server-Side

Files:

- `frontend/src/App.tsx:45`
- `frontend/src/App.tsx:48`
- `frontend/src/services/api.ts:37`

The frontend generates `olfit_session_id` and sends it as `X-Session-ID`. This is fine for anonymous analytics/correlation, but it is forgeable because users can edit `localStorage`.

Recommended fix:

- Treat `X-Session-ID` as an untrusted correlation ID only.
- Do not use it for authorization, data ownership, or privacy boundaries unless the backend signs or issues it.

### Low: Raw HTML Rendering Is Currently Static But Easy To Misuse Later

Files:

- `frontend/src/components/guide/ScentNoteCarousel.tsx:126`
- `frontend/src/components/guide/ScentNoteCarousel.tsx:216`
- `frontend/src/components/guide/ConcentrationList.tsx:32`
- `frontend/src/components/guide/FamilyCarousel.tsx:48`
- `frontend/src/components/guide/FamilyCarousel.tsx:80`
- `frontend/src/components/guide/NoteGlossary.tsx:99`

`dangerouslySetInnerHTML` is used for line breaks in local static data. In the current code path, the source is not user-controlled, so this is not an immediate XSS finding.

Recommended fix:

- Prefer structured text rendering, for example splitting on a known marker and rendering `<br />`.
- If these descriptions ever come from an API/CMS, sanitize before rendering.

### Low: Browser Storage Errors Can Crash Consent/Session Setup

Files:

- `frontend/src/store/useStore.ts:34`
- `frontend/src/App.tsx:48`
- `frontend/src/services/api.ts:37`

`localStorage` access is not wrapped in `try/catch`. Some privacy modes, browser policies, embedded contexts, or storage quota errors can throw and break app startup or consent handling.

Recommended fix:

- Add a small safe storage helper for `getItem`/`setItem`.
- Fall back to in-memory session state if persistent storage is unavailable.

### Low: Tailwind Warnings Should Be Cleaned Up

Files:

- `frontend/src/components/sections/HeroSection.tsx:25`
- `frontend/src/components/guide/FamilyCarousel.tsx:57`

The production build passes, but Tailwind warns that `duration-[3000ms]` and `ease-[cubic-bezier(0.23,1,0.32,1)]` are ambiguous. This does not currently block build output, but it adds noise and can hide more important warnings later.

Recommended fix:

- Escape arbitrary values as suggested by Tailwind, or move these values into named theme utilities.

## Security Notes

- No hardcoded secrets, tokens, passwords, or API keys were found in `frontend/src`.
- No `eval`, `new Function`, `document.write`, or dynamic script injection was found.
- File upload validation has useful client-side checks: MIME allowlist, extension allowlist, magic number check, 10 MB size limit, image decode failure handling, and canvas dimension cap.
- Client-side upload validation should be treated as UX only. The backend must repeat file type, size, content, and retention validation.

## Recommended Next Actions

1. Fix price sorting by adding `price_krw` data or a robust price parser fallback.
2. Update `e2e/image-upload.spec.ts` to match the current manual analysis flow and assert duplicate prevention.
3. Clarify the image upload architecture: real storage URL vs direct base64 analysis.
4. Convert clickable `div` regions into accessible buttons.
5. Add focused tests for price sorting, invalid file rejection, successful upload plus analysis, and duplicate drop/click prevention.
