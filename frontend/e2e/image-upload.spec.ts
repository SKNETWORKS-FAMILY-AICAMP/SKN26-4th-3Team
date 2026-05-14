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
  recommendations: [],
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

test("single file selection uploads once and requests analysis once", async ({ page }) => {
  const logs: string[] = [];
  const apiRequests: string[] = [];
  page.on("console", (message) => logs.push(message.text()));
  await prepareApp(page, apiRequests);

  const chooser = page.waitForEvent("filechooser");
  await page.getByText("Drag & Drop or Click to browse").click();
  const fileChooser = await chooser;
  await fileChooser.setFiles({
    name: "one.png",
    mimeType: "image/png",
    buffer: pixelPng,
  });

  await expect.poll(() => apiRequests.length).toBe(1);
  expect(logs.filter((line) => line.includes("Uploading image to cloud storage")).length).toBe(1);
});

test("documents current rapid double drop duplicate analysis behavior", async ({ page }) => {
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

  await expect.poll(() => apiRequests.length).toBe(2);
  expect(logs.filter((line) => line.includes("Uploading image to cloud storage")).length).toBe(2);
});
