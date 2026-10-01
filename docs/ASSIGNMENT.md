# Assignment Write-ups

**Student:** Siva Sai Deepank Manoj  
**Public GitHub:** https://github.com/deeps45/juice-guard  
**Submission PDF:** [`submission.pdf`](submission.pdf)

---

## Part 1 — Secure Feature Design

I looked through OWASP Juice Shop with a focus on registration and login. Three issues stood out.

**1. SQL injection on login.** If the login query is built by joining strings, a crafted email can change the query and skip password checks. Mitigation: parameterized queries / ORM only, plus email format checks so input stays data, not code.

**2. XSS.** Search or review fields can reflect or store HTML/JS that runs in another user’s browser. Mitigation: output encoding, `textContent` instead of `innerHTML`, reject angle brackets, and Content-Security-Policy.

**3. Auth bypass / weak sessions.** Weak tokens make impersonation easier. Mitigation: signed short-lived tokens, server-side authorization, rate limits, and generic login errors.

**Password handling:** hash with bcrypt (cost 12); verify with `bcrypt.compare`; never store plaintext.

```js
const passwordHash = await bcrypt.hash(password, 12);
const ok = await bcrypt.compare(submittedPassword, user.passwordHash);
```

---

## Part 2 — Front-End Login Form

I built a Juice Shop–style login page in HTML/CSS/JS with an Express backend.

- **Client (`public/app.js`):** blocks empty fields; email must contain `@`; password ≥ 8 characters.
- **Server (`server.js`):** stricter validation, bcryptjs verification, no string-built SQL, rate limiting, safe status rendering.

**Run:** `npm install && npm start` → http://127.0.0.1:3847  
**Demo:** `demo@juice.shop` / `JuiceShop1!`  
**Repo:** https://github.com/deeps45/juice-guard

---

## Part 3 — Breaking My Own Form

**XSS:** email `xss@test.com`, password `<script>alert(1)</script>`. Result: blocked; no alert; unsafe characters rejected (see `05-xss-blocked.png`).

**SQLi:** email `admin@test.com' OR '1'='1`, password `password1`. Result: blocked; invalid email; no auth bypass (see `06-sqli-blocked.png`).

**Fix applied:** Content-Security-Policy header so inline scripts cannot run even if rendering mistakes happen later.
