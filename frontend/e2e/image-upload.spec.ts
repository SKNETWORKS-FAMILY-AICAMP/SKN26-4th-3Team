import { expect, test, type Page } from "@playwright/test";
import fs from "node:fs";
import http, { type Server } from "node:http";
import path from "node:path";

const distDir = path.resolve(process.cwd(), "dist");
let server: Server;

test.beforeAll(async () => {
  server = http.createServer((request, response) => {
    const requestUrl = request.url?.split("?")[0] || "/";
    const relativePath = requestUrl === "/" ? "index.html" : requestUrl.replace(/^\/+/, "");
    const filePath = path.join(distDir, relativePath);
    const resolvedPath = fs.existsSync(filePath) && fs.statSync(filePath).isFile()
      ? filePath
      : path.join(distDir, "index.html");

    const extension = path.extname(resolvedPath);
    const contentType = extension === ".js"
      ? "text/javascript"
      : extension === ".css"
        ? "text/css"
        : "text/html";

    response.writeHead(200, { "Content-Type": contentType });
    response.end(fs.readFileSync(resolvedPath));
  });

  await new Promise<void>((resolve) => {
    server.listen(4173, "127.0.0.1", () => resolve());
  });
});

test.afterAll(async () => {
  await new Promise<void>((resolve, reject) => {
    server.close((error) => {
      if (error) reject(error);
      else resolve();
    });
  });
});

const pixelPng = Buffer.from(
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADUlEQVR4nGP4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC",
  "base64",
);

const analysisResponse = {
  type: "personal",
  personalMood: "#test",
  perfumeKeywords: [],
  fashionStyle: "test",
  analysisMetadata: {
    base64Image: "x",
    selectedNotes: [],
    radarScores: {},
    readableQuery: "",
  },
  recommendations: [
    {
      id: 1,
      name: "테스트 향수",
      brand: "OLFIT",
      price: "₩120,000",
      price_krw: 120000,
      size: "50ml",
      image: "data:image/png;base64,iVBORw0KGgo=",
      imageUrl: "data:image/png;base64,iVBORw0KGgo=",
      tags: ["fresh"],
      notes: "베르가못, 자스민, 머스크",
      family: "프레시",
      mainAccords: ["시트러스"],
      moods: ["clean"],
      occasions: ["daily"],
      category: "Personal",
      similarity: 91,
      matchReason: "테스트 추천 사유",
      details: {
        story: "테스트 향수의 상세 설명입니다.",
        topNotes: "베르가못",
        middleNotes: "자스민",
        baseNotes: "머스크",
        bestFor: "데일리",
      },
    },
  ],
};

async function prepareApp(page: Page, apiRequests: string[]) {
  await page.addInitScript(() => {
    window.localStorage.setItem("olfit_consent", "true");
    window.localStorage.setItem("olfit_session_id", "test-session");
  });

  await page.route("**/api/analyze/", async (route) => {
    apiRequests.push(route.request().postData() || "");
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(analysisResponse),
    });
  });

  await page.goto("/");
  await page.locator("#interview").scrollIntoViewIfNeeded();
}

async function uploadValidImage(page: Page, fileName = "one.png") {
  await page.locator('input[type="file"]').setInputFiles({
    name: fileName,
    mimeType: "image/png",
    buffer: pixelPng,
  });

  const analyzeButton = page.getByRole("button", { name: /분석 시작/ });
  await expect(analyzeButton).toBeEnabled({ timeout: 10_000 });
  await analyzeButton.click();
}

test("single file selection uploads once and requests analysis once", async ({ page }) => {
  const logs: string[] = [];
  const apiRequests: string[] = [];
  page.on("console", (message) => logs.push(message.text()));
  await prepareApp(page, apiRequests);

  await uploadValidImage(page);

  await expect.poll(() => apiRequests.length, { timeout: 15_000 }).toBe(1);
  expect(logs.filter((line) => line.includes("Uploading image to cloud storage")).length).toBe(1);
});

test("rapid double drop keeps the current duplicate prevention behavior", async ({ page }) => {
  const logs: string[] = [];
  const apiRequests: string[] = [];
  page.on("console", (message) => logs.push(message.text()));
  await prepareApp(page, apiRequests);

  await page.evaluate((pngBytes) => {
    const input = document.querySelector<HTMLInputElement>("input[type=file]");
    const dropTarget = input?.parentElement;
    if (!dropTarget) throw new Error("Image upload drop target was not found.");

    const bytes = Uint8Array.from(pngBytes);
    const dispatchDrop = (name: string) => {
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(new File([bytes], name, { type: "image/png" }));
      dropTarget.dispatchEvent(
        new DragEvent("drop", {
          bubbles: true,
          cancelable: true,
          dataTransfer,
        }),
      );
    };

    dispatchDrop("one.png");
    dispatchDrop("two.png");
  }, Array.from(pixelPng));

  const analyzeButton = page.getByRole("button", { name: /분석 시작/ });
  await expect(analyzeButton).toBeEnabled({ timeout: 10_000 });
  await analyzeButton.click();

  await expect.poll(() => apiRequests.length, { timeout: 15_000 }).toBe(1);
  expect(logs.filter((line) => line.includes("Uploading image to cloud storage")).length).toBe(1);
});

test("invalid file upload does not request analysis", async ({ page }) => {
  const apiRequests: string[] = [];
  await prepareApp(page, apiRequests);

  await page.locator('input[type="file"]').setInputFiles({
    name: "not-image.txt",
    mimeType: "text/plain",
    buffer: Buffer.from("not an image"),
  });

  await expect(
    page.getByText("JPG, PNG, WEBP 형식의 이미지만 업로드 가능합니다."),
  ).toBeVisible();
  expect(apiRequests).toHaveLength(0);
});

test("recommendation card opens product detail modal", async ({ page }) => {
  const apiRequests: string[] = [];
  await prepareApp(page, apiRequests);

  await uploadValidImage(page);
  await expect.poll(() => apiRequests.length, { timeout: 15_000 }).toBe(1);

  await page.locator("#report").scrollIntoViewIfNeeded();
  await page.getByRole("heading", { name: "테스트 향수" }).click();

  const modal = page.locator("div.fixed").filter({
    has: page.getByRole("heading", { level: 3, name: "테스트 향수" }),
  });

  await expect(modal.getByRole("heading", { level: 3, name: "테스트 향수" })).toBeVisible();
  await expect(modal.getByText("OLFIT", { exact: true })).toBeVisible();
  await expect(modal.getByText("베르가못")).toBeVisible();
  await expect(modal.getByText("자스민")).toBeVisible();
  await expect(modal.getByText("머스크")).toBeVisible();
  await expect(modal.locator('img[alt="테스트 향수"]')).toBeVisible();
});
