/**
 * @file reportCapture.ts
 * @description 글자 잘림 및 레이아웃 오류를 완벽하게 해결한 초정밀 캡처 서비스입니다.
 */

import html2canvas from "html2canvas";

/**
 * 리포트 요소를 캡처하여 Blob 형태의 고해상도 이미지를 생성합니다.
 */
export const captureReportBlob = async (reportElement: HTMLElement | null): Promise<Blob | null> => {
  if (!reportElement) return null;

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
