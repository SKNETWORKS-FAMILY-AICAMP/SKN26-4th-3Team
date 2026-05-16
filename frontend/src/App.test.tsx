/**
 * @file App.test.tsx
 * @description 회귀 방지를 위한 테스트 파일입니다.
 * @lastModified 2026-05-16
 */

import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import { useOlfitStore } from "@/store/useStore";

const originalCrypto = globalThis.crypto;

describe("App consent flow", () => {
  beforeEach(() => {
    localStorage.clear();
    useOlfitStore.setState({
      analysisResults: null,
      selectedNotes: [],
      hasConsented: false,
      selectedProduct: null,
      isLoading: false,
      error: null,
      restartToken: 0,
    });
  });

  afterEach(() => {
    Object.defineProperty(globalThis, "crypto", {
      value: originalCrypto,
      configurable: true,
    });
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("continues consent when randomUUID is unavailable in insecure browser contexts", async () => {
    Object.defineProperty(globalThis, "crypto", {
      value: { ...originalCrypto, randomUUID: undefined },
      configurable: true,
    });

    render(<App />);

    await userEvent.click(
      screen.getByRole("button", { name: /agree and continue/i }),
    );

    expect(localStorage.getItem("olfit_consent")).toBe("true");
    expect(localStorage.getItem("olfit_session_id")).toMatch(/^session-/);
    expect(
      screen.queryByRole("button", { name: /agree and continue/i }),
    ).not.toBeInTheDocument();
  });
});

// EOF: App.test.tsx
