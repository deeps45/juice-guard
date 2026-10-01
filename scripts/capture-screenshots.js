/**
 * Capture Part 3 evidence: successful XSS on vulnerable draft + blocked on secure form.
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "..", "docs", "screenshots");
const BASE = "http://127.0.0.1:3847";
const XSS_EMAIL =
  'x@y.com<img id="xss-flag" src=x onerror="this.outerHTML=\'<strong id=xss-flag style=color:#b42318;font-size:18px;display:block;margin-top:8px\">XSS EXECUTED — script ran in the page</strong>\'">';

async function shot(page, name) {
  const file = path.join(OUT, name);
  await page.screenshot({ path: file, fullPage: true });
  console.log("saved", file);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });

  // Keep existing secure-form shots fresh
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
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

  // SUCCESSFUL XSS on vulnerable draft
  await page.goto(BASE + "/vulnerable.html", { waitUntil: "networkidle" });
  await page.fill("#email", XSS_EMAIL);
  await page.fill("#password", "password1");
  await page.click("#submit-btn");
  await page.waitForSelector("#xss-flag", { timeout: 5000 });
  const flagText = await page.locator("#xss-flag").innerText();
  console.log("xss_flag=", flagText);
  await page.waitForTimeout(400);
  await shot(page, "07-xss-exploited-vulnerable.png");

  // Same payload blocked on hardened form
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.fill("#email", XSS_EMAIL);
  await page.fill("#password", "password1");
  await page.click("#submit-btn");
  await page.waitForTimeout(800);
  const leaked = await page.locator("#xss-flag").count();
  console.log("secure_xss_flags=", leaked);
  await shot(page, "05-xss-blocked.png");

  // SQLi blocked on hardened form
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.fill("#email", "admin@test.com' OR '1'='1");
  await page.fill("#password", "password1");
  await page.click("#submit-btn");
  await page.waitForTimeout(800);
  await shot(page, "06-sqli-blocked.png");

  // Client-side bypass evidence via API (optional page showing result)
  await page.setContent(`<!DOCTYPE html><html><head><title>Client bypass</title>
    <style>body{font-family:Arial,sans-serif;padding:40px;background:#0b1220;color:#f4f7fb}
    pre{background:#132038;padding:16px;border-radius:8px;white-space:pre-wrap}
    .ok{color:#7dffa0}.bad{color:#ff8f8f}</style></head><body>
    <h1>Client-side validation bypass</h1>
    <p>Calling <code>/api/insecure-login</code> directly (no browser checks):</p>
    <pre id="out">running…</pre>
    <script>
      fetch('/api/insecure-login',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({email:'bypass@test.com<script>/*payload*/</script>',password:'password1'})})
        .then(r=>r.json()).then(d=>{
          out.textContent = JSON.stringify(d,null,2);
          out.className = d.message && d.message.includes('<script>') ? 'bad' : 'ok';
        });
    </script></body></html>`);
  await page.waitForTimeout(700);
  await shot(page, "08-client-bypass-api.png");

  await browser.close();
  console.log("done");
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
