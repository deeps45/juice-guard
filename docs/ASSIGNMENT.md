# Assignment Write-ups — OWASP Juice Shop Security

**Student:** Siva Sai Deepank Manoj  
**Submission PDF:** [`docs/submission.pdf`](submission.pdf)

> **GitHub (required public):** After clicking **Create repo** in Cursor and setting visibility to **Public**, paste your real clone URL into Part 2 of the PDF (and below). Example shape: `https://github.com/<you>/juice-shop-secure-login`

---

## Part 1: Secure Feature Design (~100 words)

While exploring OWASP Juice Shop, three realistic attack paths stood out.

**(1) SQL injection on login** — crafted email input can manipulate concatenated SQL and bypass authentication. **Mitigation:** parameterized queries / ORM lookups only; reject malformed emails before the data layer. This stops payloads from changing query logic.

**(2) XSS in search/reviews** — attacker HTML/JS can run in other users’ browsers. **Mitigation:** context-aware output encoding, prefer `textContent` over `innerHTML`, Content-Security-Policy, and reject angle brackets on input so scripts display as text instead of executing.

**(3) Authentication bypass / weak tokens** — predictable or poorly verified sessions impersonate admins. **Mitigation:** signed tokens with strong secrets, short expiry, server-side authorization, rate limits, and generic login errors.

**Secure password handling:** hash with bcrypt (cost ≥ 12), store only the hash, verify with `bcrypt.compare`. Never log plaintext. Even if the DB leaks, attackers get slow-to-crack hashes—not reusable passwords.

```js
const passwordHash = await bcrypt.hash(password, 12);
const match = await bcrypt.compare(submittedPassword, user.passwordHash);
```

---

## Part 2: Implement a Simple Front-End Form (~100 words)

I built a Juice Shop–style login page in plain **HTML + JavaScript**, served by a small **Express** API.

**Client-side (`public/app.js`):** on submit, the form blocks empty fields, requires `@` in the email, and requires passwords ≥ 8 characters before calling the API.

**Server-side (`server.js`):** re-validates email format, password length, and unsafe characters; looks up users in memory (no string-built SQL); verifies passwords with **bcryptjs**; returns escaped, generic errors; rate-limits attempts.

**Run locally:** `npm install && npm start` → open http://127.0.0.1:3847  
**Demo user:** `demo@juice.shop` / `JuiceShop1!`

**Public GitHub repo:** `https://github.com/<YOUR_USERNAME>/juice-shop-secure-login`  
*(Replace with your real public URL after Create repo.)*

---

## Part 3: Exploit a Vulnerability in Your Own Form (~100 words)

I attempted XSS and SQL injection against my own form.

**XSS steps:** email `xss@test.com`, password `<script>alert(1)</script>`, click Log in. **Result:** blocked — no alert; server rejected unsafe characters; UI uses `textContent` (see `docs/screenshots/05-xss-blocked.png`).

**SQLi steps:** email `admin@test.com' OR '1'='1`, password `password1`. **Result:** blocked — invalid email; no SQL concatenation; no auth bypass (see `docs/screenshots/06-sqli-blocked.png`).

**Fix if needed:** add a strict Content-Security-Policy (`default-src 'self'`) so even a future `innerHTML` mistake cannot execute inline scripts. Failing to break the form is a good sign the defenses hold.
