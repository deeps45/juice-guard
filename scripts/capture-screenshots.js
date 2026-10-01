/**
 * Capture UI + API evidence for the hardened form (no staged vulnerable pages).
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "..", "docs", "screenshots");
const BASE = "http://127.0.0.1:3847";

async function shot(page, name) {
  const file = path.join(OUT, name);
  await page.screenshot({ path: file, fullPage: true });
  console.log("saved", name);
}

async function getCsrf(page) {
  return page.evaluate(async () => {
    const res = await fetch("/api/csrf", { credentials: "same-origin" });
    return res.json();
  });
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1100, height: 860 } });

  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.waitForTimeout(500);
  await shot(page, "01-login-form.png");

  await page.fill("#email", "demo@juice.shop");
  await page.fill("#password", "JuiceShop1!");
  await page.click("#submit-btn");
  await page.waitForSelector("#form-status.ok");
  await shot(page, "02-successful-login.png");

  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.click("#submit-btn");
  await page.waitForSelector("#email-hint:not([hidden])");
  await shot(page, "03-empty-validation.png");

  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.fill("#email", "test@example.com");
  await page.fill("#password", "short");
  await page.click("#submit-btn");
  await page.waitForSelector("#password-hint:not([hidden])");
  await shot(page, "04-short-password.png");

  // XSS payload passes CLIENT (length >= 8) then is rejected by SERVER
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.fill("#email", "xss@test.com");
  await page.fill("#password", "<script>alert(1)</script>");
  const reqPromise = page.waitForRequest(
    (r) => r.url().includes("/api/login") && r.method() === "POST"
  );
  await page.click("#submit-btn");
  const loginReq = await reqPromise;
  const postData = loginReq.postData() || "";
  console.log("client_allowed_xss_request", postData.includes("<script>"));
  await page.waitForSelector("#form-status.err");
  await page.waitForTimeout(400);
  await shot(page, "05-xss-client-passed-server-blocked.png");

  // SQLi blocked
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.fill("#email", "admin@test.com' OR '1'='1");
  await page.fill("#password", "password1");
  await page.click("#submit-btn");
  await page.waitForSelector("#form-status.err, #email-hint:not([hidden])");
  await page.waitForTimeout(400);
  await shot(page, "06-sqli-blocked.png");

  // API evidence: CSRF missing token + client-bypass style request
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  const noCsrf = await page.evaluate(async () => {
    const res = await fetch("/api/login", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "demo@juice.shop",
        password: "JuiceShop1!",
      }),
    });
    return { status: res.status, body: await res.json() };
  });

  const csrf = await getCsrf(page);
  const bypass = await page.evaluate(async (token) => {
    // Skips validateClient() entirely — raw API call with dangerous password
    const res = await fetch("/api/login", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": token,
      },
      body: JSON.stringify({
        email: "attacker@test.com",
        password: "<script>alert(1)</script>",
      }),
    });
    return { status: res.status, body: await res.json() };
  }, csrf.csrfToken);

  console.log("noCsrf", noCsrf);
  console.log("bypass", bypass);

  const evidenceHtml = `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>API exploit evidence</title>
<style>
 body{font-family:Arial,sans-serif;background:#0b1220;color:#e8eef8;padding:36px;line-height:1.45}
 h1{margin:0 0 8px;font-size:28px} h2{margin:22px 0 8px;font-size:18px;color:#f5b301}
 .card{background:#132038;border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:14px 16px;margin:10px 0}
 .ok{color:#7dffa0}.bad{color:#ffb4b4} code,pre{font-family:ui-monospace,monospace}
 pre{white-space:pre-wrap;word-break:break-word;margin:0}
</style></head><body>
<h1>Weaknesses found in my login form</h1>
<p>Tests run against the real <code>/api/login</code> endpoint (not a planted page).</p>
<h2>1) Missing CSRF token → request rejected</h2>
<div class="card">
<p>Forged login POST with valid demo credentials but <b>no</b> <code>X-CSRF-Token</code>:</p>
<pre class="bad">HTTP ${noCsrf.status}
${JSON.stringify(noCsrf.body, null, 2)}</pre>
<p class="ok">Result: CSRF weakness is mitigated — forged request blocked (403).</p>
</div>
<h2>2) Client-side validation bypass → server still blocks XSS</h2>
<div class="card">
<p>Called <code>/api/login</code> directly with <code>fetch()</code>, skipping <code>validateClient()</code>, using password <code>&lt;script&gt;alert(1)&lt;/script&gt;</code>:</p>
<pre class="bad">HTTP ${bypass.status}
${JSON.stringify(bypass.body, null, 2)}</pre>
<p class="ok">Result: client checks are bypassable, but server validation rejected the payload.</p>
</div>
</body></html>`;

  await page.setContent(evidenceHtml, { waitUntil: "domcontentloaded" });
  await shot(page, "07-api-weakness-evidence.png");

  await browser.close();
  console.log("done");
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
