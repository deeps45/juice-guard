/**
 * Defensive UI capture script — documents validation blocking unsafe input.
 * Not an exploit; used only to produce assignment screenshots.
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "..", "docs", "screenshots");
const BASE = "http://127.0.0.1:3847";

async function shot(page, name) {
  const file = path.join(OUT, name);
  await page.screenshot({ path: file, fullPage: true });
  console.log("saved", file);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });

  // 1. Clean form
  await page.goto(BASE, { waitUntil: "networkidle" });
  await shot(page, "01-login-form.png");

  // 2. Successful login
  await page.fill("#email", "demo@juice.shop");
  await page.fill("#password", "JuiceShop1!");
  await page.click("#submit-btn");
  await page.waitForSelector("#form-status.ok");
  await shot(page, "02-successful-login.png");

  // 3. Empty validation
  await page.goto(BASE, { waitUntil: "networkidle" });
  await page.fill("#email", "");
  await page.fill("#password", "");
  await page.click("#submit-btn");
  await page.waitForSelector("#email-hint:not([hidden])");
  await shot(page, "03-empty-validation.png");

  // 4. Short password
  await page.goto(BASE, { waitUntil: "networkidle" });
  await page.fill("#email", "test@example.com");
  await page.fill("#password", "short");
  await page.click("#submit-btn");
  await page.waitForSelector("#password-hint:not([hidden])");
  await shot(page, "04-short-password.png");

  // 5. XSS-like password blocked (defensive)
  await page.goto(BASE, { waitUntil: "networkidle" });
  let dialogOpened = false;
  page.on("dialog", async (d) => {
    dialogOpened = true;
    await d.dismiss();
  });
  await page.fill("#email", "xss@test.com");
  await page.fill("#password", "<script>alert(1)</script>");
  await page.click("#submit-btn");
  await page.waitForTimeout(800);
  await shot(page, "05-xss-blocked.png");
  console.log("xss_dialog_opened=", dialogOpened);

  // 6. SQLi-like email blocked (defensive)
  await page.goto(BASE, { waitUntil: "networkidle" });
  await page.fill("#email", "admin@test.com' OR '1'='1");
  await page.fill("#password", "password1");
  await page.click("#submit-btn");
  await page.waitForTimeout(800);
  await shot(page, "06-sqli-blocked.png");

  await browser.close();
  console.log("done");
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
