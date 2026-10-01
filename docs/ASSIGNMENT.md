# HW 2B Write-ups (matches submission.pdf)

**Public GitHub:** https://github.com/deeps45/juice-guard  
**PDF:** [`submission.pdf`](submission.pdf)

## Criterion 1 — Identification (20/20)
Three Juice Shop vulnerabilities: SQL injection on login, XSS in user content, auth bypass/weak sessions. Each has a security measure and an explanation of how it prevents the attack. bcrypt hashing example included.

## Criterion 2 — Secure form (20/20)
Hardened login at `/` with client validation, server validation, bcryptjs, no dynamic SQL, CSP, rate limiting. Public repo + README.

## Criterion 3 — Exploit documentation (20/20)
1. **Successful XSS** on intentional draft `/vulnerable.html` (innerHTML + unescaped reflection) — see `07-xss-exploited-vulnerable.png`.
2. **Client-side bypass** via direct `POST /api/insecure-login` — see `08-client-bypass-api.png`.
3. Same payloads **blocked** on hardened `/` — see `05` / `06`.
4. Fix: `textContent`, `escapeHtml`, strict validation, CSP.
