/**
 * @file reportCapture.ts
<<<<<<< HEAD
 * @description 리포트 섹션을 고해상도 이미지로 캡처하고 저장/공유하는 기능을 담당하는 서비스입니다.
 * html2canvas를 사용하여 DOM 요소를 캔버스로 변환하며, 외부 이미지 및 스타일 예외 처리를 수행합니다.
=======
 * @description 글자 잘림 및 레이아웃 오류를 완벽하게 해결한 초정밀 캡처 서비스입니다.
>>>>>>> olfit-repo/dev
 */

import html2canvas from "html2canvas";

<<<<<<< HEAD
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
=======
/**
 * 리포트 요소를 캡처하여 Blob 형태의 고해상도 이미지를 생성합니다.
>>>>>>> olfit-repo/dev
 */
export const captureReportBlob = async (reportElement: HTMLElement | null): Promise<Blob | null> => {
  if (!reportElement) return null;

<<<<<<< HEAD
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

/**
 * 생성된 이미지를 네이티브 공유, 클립보드 복사 또는 다운로드 방식으로 사용자에게 제공합니다.
 * 
 * @param blob 이미지 Blob
 */
export const shareOrDownloadImage = async (blob: Blob): Promise<"shared" | "copied" | "downloaded" | "failed"> => {
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
};

// EOF: reportCapture.ts
=======
  const container = document.createElement("div");
  container.style.position = "absolute";
  container.style.top = "-99999px";
  container.style.left = "0";
  container.style.width = "1200px";
  container.style.backgroundColor = "#FDFCF0";
  document.body.appendChild(container);

  const clone = reportElement.cloneNode(true) as HTMLElement;
  
  // 1. UI 요소 및 애니메이션 제거
  const uiElements = clone.querySelectorAll("button, .sr-only, .animate-pulse, [role='button']");
  uiElements.forEach(el => el.remove());

  // 전역 스타일 정적화
  const allElements = clone.querySelectorAll("*");
  allElements.forEach((el) => {
    const htmlEl = el as HTMLElement;
    htmlEl.style.height = "auto";
    htmlEl.style.maxHeight = "none";
    htmlEl.style.overflow = "visible";
    htmlEl.style.transition = "none";
    htmlEl.style.animation = "none";
    htmlEl.style.transform = "none";
    htmlEl.style.boxSizing = "border-box";
  });

  clone.style.width = "1200px";
  clone.style.padding = "100px";
  clone.style.backgroundColor = "#FDFCF0";
  container.appendChild(clone);

  try {
    if (document.fonts) await document.fonts.ready;
    
    // 2. [섹션별 초정밀 보정]

    // A. 피라미드 영역 (크기 유지 및 정렬)
    const blueprint = clone.querySelector(".flex-col.md\\:flex-row.items-center.justify-center.gap-12") as HTMLElement;
    if (blueprint) {
      blueprint.style.display = "flex";
      blueprint.style.flexDirection = "row";
      blueprint.style.alignItems = "center";
      blueprint.style.gap = "100px";
      blueprint.style.marginBottom = "150px";
      
      const pyramidContainer = blueprint.querySelector("div");
      if (pyramidContainer) {
        pyramidContainer.style.width = "350px";
        pyramidContainer.style.height = "350px";
        pyramidContainer.style.flex = "0 0 350px";
      }
    }

    // B. 향수 카드 (Best Pick 잘림 및 Notes 겹침 해결)
    const listContainer = clone.querySelector(".flex") as HTMLElement;
    if (listContainer) {
      listContainer.style.display = "block";
      listContainer.style.width = "100%";

      const cards = listContainer.querySelectorAll(".flex-\\[0_0_100\\%\\]");
      cards.forEach(card => {
        const c = card as HTMLElement;
        c.style.display = "block";
        c.style.width = "100%";
        c.style.marginBottom = "100px";
        
        const inner = c.querySelector(".group") as HTMLElement;
        if (inner) {
          inner.style.display = "flex";
          inner.style.flexDirection = "row";
          inner.style.alignItems = "flex-start";
          inner.style.padding = "80px";
          inner.style.gap = "80px";
          inner.style.backgroundColor = "white";
          inner.style.border = "1px solid rgba(107,68,35,0.1)";
        }

        // Best Pick 배지 잘림 방지
        const bestPickBadge = c.querySelector(".inline-flex") as HTMLElement;
        if (bestPickBadge) {
          bestPickBadge.style.display = "block";
          bestPickBadge.style.width = "fit-content";
          bestPickBadge.style.padding = "10px 20px";
          bestPickBadge.style.marginBottom = "20px";
          bestPickBadge.style.lineHeight = "1";
          const span = bestPickBadge.querySelector("span");
          if (span) span.style.display = "block";
        }

        // 우측 정보 영역 레이아웃 강제 (Block Sequencing 기법 적용)
        const textArea = c.querySelector(".md\\:w-1\\/2.text-left") as HTMLElement;
        if (textArea) {
          textArea.style.flex = "1";
          textArea.style.display = "block"; 
          textArea.style.textAlign = "left";
          textArea.style.overflow = "visible";
          textArea.style.paddingLeft = "20px";

          // 제목 영역
          const title = textArea.querySelector("h4") as HTMLElement;
          if (title) {
            title.style.display = "block";
            title.style.marginBottom = "30px";
            title.style.fontSize = "32px";
          }

          // Notes 섹션 (고정 간격 부여)
          const notesSection = textArea.querySelector(".space-y-4") as HTMLElement;
          if (notesSection) {
            notesSection.style.display = "block";
            notesSection.style.position = "relative";
            notesSection.style.marginBottom = "80px"; // 하단 요소와의 물리적 간격 확대
            
            const noteText = notesSection.querySelector("p") as HTMLElement;
            if (noteText) {
              noteText.style.display = "block";
              noteText.style.position = "relative";
              noteText.style.fontSize = "18px";
              noteText.style.lineHeight = "1.8";
              noteText.style.marginBottom = "20px";
            }
          }

          // 하단 스펙 그리드 (Notes와 물리적으로 분리)
          const specGrid = textArea.querySelector(".flex.flex-wrap") as HTMLElement;
          if (specGrid) {
            specGrid.style.display = "flex";
            specGrid.style.flexDirection = "row";
            specGrid.style.position = "relative";
            specGrid.style.marginTop = "40px";
            specGrid.style.gap = "40px";
          }
        }
      });
    }

    // 3. 전용 고해상도 헤더
    const header = document.createElement("div");
    header.style.cssText = "display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:120px; border-bottom:3px solid #6B4423; padding-bottom:40px; width:1000px; margin: 0 auto;";
    header.innerHTML = `
      <div style="text-align:left;">
        <div style="font-family: serif; font-size:36px; letter-spacing: 0.3em; color:#6B4423; font-weight:300;">OLFIT</div>
        <div style="font-size: 11px; color: #6B4423; margin-top: 10px; letter-spacing: 0.15em;">PRECISION SCENT ANALYSIS</div>
      </div>
      <div style="text-align:right;">
        <div style="font-size:12px; color:rgba(107, 68, 35, 0.4); font-weight:600;">REPORT NO. ${Math.floor(Math.random()*100000)}</div>
        <div style="font-size:11px; color:rgba(107, 68, 35, 0.4);">${new Date().toLocaleDateString("en-US", { year: 'numeric', month: 'long', day: 'numeric' })}</div>
      </div>
    `;
    clone.prepend(header);

    const safety = document.createElement("div");
    safety.style.height = "150px";
    clone.appendChild(safety);

    await new Promise(resolve => setTimeout(resolve, 1200));

    // 4. 최종 캡처 실행
    const canvas = await html2canvas(clone, {
      backgroundColor: "#FDFCF0",
      scale: 3, 
      useCORS: true,
      allowTaint: true,
      logging: false,
      width: 1200,
      height: clone.getBoundingClientRect().height + 100,
      windowWidth: 1200
    });

    return new Promise((resolve) => canvas.toBlob(resolve, "image/png", 1.0));
  } catch (err) {
    console.error("Capture Failed:", err);
    return null;
  } finally {
    document.body.removeChild(container);
  }
};

/**
 * 저장 및 공유
 */
export const shareOrDownloadImage = async (blob: Blob): Promise<"shared" | "copied" | "downloaded" | "failed"> => {
  try {
    const timestamp = new Date().getTime();
    const fileName = `Olfit_Report_${timestamp}.png`;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => document.body.removeChild(a), 100);
    await new Promise(resolve => setTimeout(resolve, 500));
    const file = new File([blob], fileName, { type: "image/png" });
    if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
      try { await navigator.share({ files: [file], title: "Olfit Report" }); return "shared"; } catch (e) {}
    }
    if (navigator.clipboard && window.ClipboardItem) {
      try { await navigator.clipboard.write([new ClipboardItem({ "image/png": blob })]); } catch (ce) {}
    }
    setTimeout(() => URL.revokeObjectURL(url), 5000);
    return "downloaded";
  } catch (err) { return "failed"; }
};
>>>>>>> olfit-repo/dev
