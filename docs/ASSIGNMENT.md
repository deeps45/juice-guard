# Assignment Write-ups — OWASP Juice Shop Security

> Paste the GitHub repository URL into Part 2 of your PDF after you make the repo public (Create repo in Cursor, then ensure visibility is Public).

---

## Part 1: Secure Feature Design (~100 words)

While exploring OWASP Juice Shop, three realistic attack paths stand out. **(1) SQL injection on login** — classic payloads in the email field can bypass auth when queries are concatenated. **Mitigation:** parameterized queries / ORM lookups only; never build SQL from raw input. **(2) Stored/reflected XSS** — product searches and reviews can run attacker JavaScript in other users’ browsers. **Mitigation:** context-aware output encoding, Content-Security-Policy, and rejecting HTML tags on input. **(3) Authentication bypass / weak secrets** — forged or predictable tokens let attackers impersonate admins. **Mitigation:** signed JWTs with strong secrets, short expiry, and server-side session checks.

**Secure password handling:** hash with bcrypt (cost ≥ 12), store only the hash, and verify with `bcrypt.compare`. Never log plaintext passwords. Combined with rate limits and generic “invalid email or password” messages, this registration/login design blocks injection, XSS reflection, and trivial auth bypass.

---

## Part 2: Implement a Simple Front-End Form (~100 words)

I built a Juice Shop–style login page in plain **HTML + JavaScript**, served by a small **Express** API.

**Client-side (`public/app.js`):** on submit, the form blocks empty fields, requires `@` in the email, and requires passwords ≥ 8 characters before calling the API.

**Server-side (`server.js`):** re-validates email format, password length, and unsafe characters; looks up users in memory (no string-built SQL); verifies passwords with **bcrypt**; returns escaped, generic errors.

**Run locally:** `npm install && npm start` → open http://127.0.0.1:3847. Demo user: `demo@juice.shop` / `JuiceShop1!`.

**GitHub repo (public):** see repository README — after publishing, use your public clone URL here (example shape: `https://github.com/<you>/<repo>`).

---

## Part 3: Exploit a Vulnerability in Your Own Form (~100 words)

I attempted common login attacks against my own form.

**SQL injection attempt:** submitted email payloads that try to short-circuit auth (quote / OR-style patterns). The server rejected invalid email shapes and never concatenates SQL — login stayed denied; no credential dump.

**XSS attempt:** entered script-like strings in email/password. Client validation and server unsafe-character checks rejected them; the UI renders status with `textContent` (not `innerHTML`), so no script executed.

**Result:** attacks **did not succeed** — a good sign that validation + bcrypt + safe rendering hold. **One hardening fix:** add a strict Content-Security-Policy header (`default-src 'self'`) and sanitize any future user-visible fields with a trusted library so reflected content cannot introduce executable markup even if validation is later loosened.

Screenshots of the failed attempts are included in `docs/screenshots/` and in `docs/submission.pdf`.
