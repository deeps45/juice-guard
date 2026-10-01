# HW 2B Write-ups

**Public GitHub:** https://github.com/deeps45/juice-guard  
**PDF:** [`submission.pdf`](submission.pdf)

## Criterion 1 — Identification
Hands-on on live Juice Shop (`preview.owasp-juice.shop`): Login page + Score Board challenges **Login Admin**, **DOM XSS**, and JWT/broken-auth class. Measures + prevention for each. bcrypt example included.

## Criterion 2 — Secure form
Hardened `/` only (no planted vuln routes). Client + server validation, CSRF, bcrypt, CSP, rate limits, no dynamic SQL. Demo credentials in README only.

## Criterion 3 — Exploit documentation
On the real form: client validation gap exploited (XSS payload submitted by browser), `fetch()` client bypass documented, CSRF absence tested (now 403), SQLi blocked. Fixes listed in the PDF.
