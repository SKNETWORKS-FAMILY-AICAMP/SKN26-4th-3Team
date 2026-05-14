/**
 * @file reportCapture.ts
 * @description 리포트 섹션을 고해상도 이미지로 캡처하고 저장/공유하는 기능을 담당하는 서비스입니다.
 * html2canvas를 사용하여 DOM 요소를 캔버스로 변환하며, 외부 이미지 및 스타일 예외 처리를 수행합니다.
 */

import html2canvas from "html2canvas";

const CAPTURE_BACKGROUND = "#FDFCF0";
const CAPTURE_WIDTH = 1000;
const CAPTURE_VIEWPORT_WIDTH = 1200;
const CAPTURE_TIMEOUT = 45000;
const IMAGE_LOAD_TIMEOUT = 15000;

const wait = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

const waitForNextPaint = () =>
  new Promise<void>((resolve) => {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => resolve());
    });
  });

const waitForImage = async (img: HTMLImageElement, timeout = IMAGE_LOAD_TIMEOUT): Promise<boolean> => {
  if (!img.src && !img.currentSrc) return true;

  const decode = async () => {
    try {
      await img.decode?.();
    } catch {
      // decode() can reject for cached/SVG images even after a successful load.
    }
  };

  if (img.complete && img.naturalWidth > 0) {
    await decode();
    return true;
  }

  const loaded = await new Promise<boolean>((resolve) => {
    const handleLoad = () => {
      cleanup();
      resolve(img.naturalWidth > 0);
    };
    const handleError = () => {
      cleanup();
      resolve(false);
    };

    const cleanup = () => {
      window.clearTimeout(timer);
      img.removeEventListener("load", handleLoad);
      img.removeEventListener("error", handleError);
    };

    const timer = window.setTimeout(() => {
      cleanup();
      resolve(false);
    }, timeout);

    img.addEventListener("load", handleLoad, { once: true });
    img.addEventListener("error", handleError, { once: true });
  });

  if (loaded) await decode();
  return loaded;
};

const waitForImages = async (root: ParentNode, timeout = IMAGE_LOAD_TIMEOUT) => {
  const images = Array.from(root.querySelectorAll("img"));
  await Promise.all(images.map((img) => waitForImage(img, timeout)));
};

const injectCaptureStyles = (clonedDoc: Document) => {
  const style = clonedDoc.createElement("style");
  style.textContent = `
    #report-content,
    #report-content * {
      animation: none !important;
      transition-delay: 0s !important;
      transition-duration: 0s !important;
    }

    #report-content {
      opacity: 1 !important;
      filter: none !important;
      transform: none !important;
      background: ${CAPTURE_BACKGROUND} !important;
      color: #3D2B1F !important;
    }

    #report-content img {
      opacity: 1 !important;
      filter: none !important;
      image-rendering: auto !important;
    }
  `;
  clonedDoc.head.appendChild(style);
};

const normalizeCapturePills = (root: ParentNode) => {
  root.querySelectorAll<HTMLElement>("[data-capture-pill]").forEach((pill) => {
    const type = pill.dataset.capturePill;

    pill.style.display = "inline-flex";
    pill.style.alignItems = "center";
    pill.style.justifyContent = "center";
    pill.style.boxSizing = "border-box";
    pill.style.lineHeight = "1";
    pill.style.paddingTop = "0";
    pill.style.paddingBottom = "0";
    pill.style.whiteSpace = "nowrap";

    if (type === "sort") {
      pill.style.height = "32px";
      pill.style.minWidth = "72px";
      pill.style.borderRadius = "9999px";
    } else if (type === "match") {
      pill.style.height = "28px";
      pill.style.minWidth = "74px";
      pill.style.borderRadius = "9999px";
    } else if (type === "best") {
      pill.style.height = "24px";
      pill.style.minWidth = "78px";
    }

    const label = pill.firstElementChild;
    if (label instanceof HTMLElement) {
      label.style.display = "inline-flex";
      label.style.alignItems = "center";
      label.style.justifyContent = "center";
      label.style.height = "100%";
      label.style.lineHeight = "1";
      label.style.position = "relative";
      label.style.top = "0";
      label.style.transform = type === "best" ? "translateY(1px)" : "translateY(1.5px)";
      if (type !== "match") {
        label.style.textIndent = "0.15em";
      }
    }
  });
};

const prependCaptureHeader = (clonedDoc: Document, el: HTMLElement) => {
  const header = clonedDoc.createElement("div");
  header.style.cssText = "display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:60px; border-bottom:1px solid rgba(107,68,35,0.1); padding-bottom:20px;";
  header.innerHTML = `
    <div style="display: flex; align-items: center;">
      <div>
        <div style="font-family: 'Playfair Display', serif; font-size:28px; font-weight: 300; letter-spacing: 0.25em; color:#6B4423; text-transform: uppercase; line-height: 1;">OLFIT</div>
        <div style="font-size: 10px; color: #6B4423; margin-top: 8px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase;">Visual Identity Matching</div>
      </div>
    </div>
    <div style="text-align: right;">
      <div style="font-size: 11px; font-weight: 600; color: #6B4423; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 4px;">Precision Analysis Report</div>
      <div style="font-size:10px; color:rgba(107, 68, 35, 0.5); letter-spacing: 0.05em;">${new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}</div>
    </div>
  `;
  el.prepend(header);
};

/**
 * 리포트 요소를 캡처하여 Blob 형태의 고해상도 이미지를 생성합니다.
 * 
 * @param reportRef 캡처할 DOM 요소의 Ref
 * @returns {Promise<Blob | null>} 생성된 이미지 Blob
 */
export const captureReportBlob = async (reportElement: HTMLElement | null): Promise<Blob | null> => {
  if (!reportElement) return null;

  // 원본 DOM, 클론 DOM, html2canvas 내부 이미지 로딩까지 기다릴 수 있도록 여유를 둡니다.
  const overallTimeout = new Promise<null>((_, reject) => 
    setTimeout(() => reject(new Error("Capture Timeout")), CAPTURE_TIMEOUT)
  );

  const captureProcess = (async () => {
    // 폰트 로딩 대기
    if (document.fonts) await document.fonts.ready;
    
    // 이미지 로딩 대기
    await waitForImages(reportElement);

    // 안정적인 렌더링을 위한 지연
    await wait(1000);
    await waitForNextPaint();

    const canvas = await html2canvas(reportElement, {
      backgroundColor: CAPTURE_BACKGROUND,
      scale: Math.min(3, Math.max(2, window.devicePixelRatio || 2)),
      useCORS: true,
      allowTaint: false,
      logging: false,
      imageTimeout: IMAGE_LOAD_TIMEOUT,
      scrollX: 0,
      scrollY: -window.scrollY,
      windowWidth: CAPTURE_VIEWPORT_WIDTH,
      windowHeight: Math.max(reportElement.scrollHeight, window.innerHeight),
      onclone: async (clonedDoc) => {
        // 🛠️ FIX (중복 복사 해결): 반응형 구조에서 동일 ID가 여러 개 존재할 가능성을 차단하고, 캡처 전용 타겟만 남김
        const targets = clonedDoc.querySelectorAll("#report-content");
        targets.forEach((target, index) => {
          if (index > 0) target.remove(); 
        });

        const el = clonedDoc.getElementById("report-content");
        if (!el) return;

        injectCaptureStyles(clonedDoc);

        // 클론 DOM은 애니메이션이 처음부터 다시 시작되므로, 캡처용으로 즉시 최종 상태에 고정합니다.
        el.getAnimations?.({ subtree: true }).forEach((animation) => {
          try {
            animation.finish();
          } catch {
            // Infinite animations cannot be finished; disabling CSS animations above handles them.
          }
        });

        // 원본 상품 이미지를 유지해야 선명하게 저장됩니다. 로딩만 eager/sync로 고정합니다.
        const clonedImages = el.querySelectorAll("img");
        clonedImages.forEach((img) => {
          img.loading = "eager";
          img.decoding = "sync";
        });
        
        el.style.width = `${CAPTURE_WIDTH}px`;
        el.style.maxWidth = "none";
        el.style.padding = "60px";
        el.style.filter = "none";
        el.style.transform = "none";
        el.style.opacity = "1";

        prependCaptureHeader(clonedDoc, el);
        normalizeCapturePills(el);
        await waitForImages(el);
        await waitForNextPaint();
      }
    });

    return new Promise<Blob | null>((resolve) => {
      canvas.toBlob((blob) => resolve(blob), "image/png", 1.0);
    });
  })();

  return Promise.race([captureProcess, overallTimeout]) as Promise<Blob | null>;
};

// 모듈 레벨 중복 호출 가드
let _isSharing = false;

/**
 * 생성된 이미지를 네이티브 공유, 클립보드 복사 또는 다운로드 방식으로 사용자에게 제공합니다.
 * 
 * @param blob 이미지 Blob
 */
export const shareOrDownloadImage = async (blob: Blob): Promise<"shared" | "copied" | "downloaded" | "failed"> => {
  if (_isSharing) return "failed";
  _isSharing = true;

  try {
    const file = new File([blob], `Olfit_Analysis_${Date.now()}.png`, { type: "image/png" });

    // 1. 네이티브 공유 API (모바일 등)
    if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
      try {
        await navigator.share({
          files: [file],
          title: "Olfit Scent Analysis Report",
          text: "나만의 고유한 향기 아우라 분석 결과를 확인해보세요.",
        });
        return "shared";
      } catch (shareErr) {
        if ((shareErr as Error).name === "AbortError") return "failed";
        console.warn("Share failed", shareErr);
      }
    }

    // 2. 클립보드 복사
    try {
      if (navigator.clipboard && window.ClipboardItem) {
        const item = new ClipboardItem({ "image/png": blob });
        await navigator.clipboard.write([item]);
        return "copied";
      }
    } catch (clipboardErr) {
      console.warn("Clipboard failed", clipboardErr);
    }

    // 3. 강제 다운로드
    try {
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `Olfit_Analysis_${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(() => window.URL.revokeObjectURL(url), 100);
      return "downloaded";
    } catch (downloadErr) {
      console.error("Download failed", downloadErr);
      return "failed";
    }
  } finally {
    _isSharing = false;
  }
};

// EOF: reportCapture.ts
