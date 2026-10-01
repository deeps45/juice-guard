# OWASP Juice Shop — Secure Login (HW 2B)

Hardened HTML/JavaScript login form with Express server validation, **bcrypt** password hashing, and **CSRF** protection. Built for a web security assignment based on OWASP Juice Shop findings.

## Security features

- Client-side validation: non-empty fields, email contains `@`, password ≥ 8 chars
- Server-side validation (never trust the browser)
- bcrypt password hashing (cost 12)
- CSRF tokens (`GET /api/csrf` + `X-CSRF-Token` on login)
- XSS-safe rendering (`textContent` + HTML escaping)
- Content-Security-Policy, rate limiting, no dynamic SQL

## Requirements

- Node.js 18+

## How to run

```bash
npm install
npm start
```

Open http://127.0.0.1:3847

Local demo credentials (kept in README only, not on the page):

- Email: `demo@juice.shop`
- Password: `JuiceShop1!`

## Project structure

```
public/index.html   Login UI
public/app.js       Client validation + CSRF
public/styles.css
server.js           API, bcrypt, CSRF, CSP
docs/submission.pdf Graded HW 2B write-up
```

## Public repository

https://github.com/deeps45/juice-guard

## License

MIT
