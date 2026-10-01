# HW 2B Write-ups

**Public GitHub:** https://github.com/deeps45/juice-guard  
**Submission PDF:** [`submission.pdf`](submission.pdf)

## Criterion 1 — Identification (20)
Three Juice Shop issues: SQL injection on login, XSS in user-controlled fields, auth bypass/weak sessions — each with a security measure and how it stops the attack. bcrypt password hashing example included.

## Criterion 2 — Secure form (20)
HTML/JS login form + Express server with client validation (`@`, password ≥ 8, no empties), server validation, bcryptjs, no dynamic SQL, CSP, rate limiting. README + public repo.

## Criterion 3 — Exploit documentation (20)
XSS and SQLi attempts documented with exact steps, blocked outcomes, screenshots. Residual weakness: client checks alone are insufficient; server validation + CSP required.
