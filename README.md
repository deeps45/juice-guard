# OWASP Juice Shop — Secure Login Assignment

A small **HTML + JavaScript** login form (with an Express server) inspired by [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/). It demonstrates client-side validation, server-side validation, and secure password handling with **bcrypt**.

Built for a web security coursework assignment covering secure feature design, a front-end login form, and responsible exploitation testing against the form itself.

## Features

- Email + password login UI styled after a Juice Shop–like sign-in page
- **Client-side validation**
  - Blocks empty submissions
  - Email must contain `@`
  - Password must be at least 8 characters
- **Server-side validation** (never trust the browser)
  - Stricter email format checks
  - Password length + unsafe-character rejection
  - Generic auth errors (no user enumeration)
- **bcrypt** password hashing (cost factor 12) — plaintext passwords are never stored
- Rate limiting on login/register endpoints
- XSS-safe status messages via `textContent` / HTML escaping

## Demo account

| Field    | Value           |
|----------|-----------------|
| Email    | `demo@juice.shop` |
| Password | `JuiceShop1!`     |

## Requirements

- Node.js 18+ and npm

## How to run

```bash
npm install
npm start
```

Open **http://127.0.0.1:3847** in your browser.

Optional: set a custom port with `PORT=4000 npm start`.

## Project structure

```
├── public/
│   ├── index.html   # Login form markup
│   ├── app.js       # Client-side validation + fetch to /api/login
│   └── styles.css   # Page styles
├── server.js        # Express API, bcrypt hashing, server validation
├── package.json
└── README.md
```

## Secure password handling (example)

On registration / seed, passwords are hashed once:

```js
const passwordHash = await bcrypt.hash(password, 12);
```

On login, compare with the stored hash (never reverse the hash):

```js
const match = await bcrypt.compare(password, user.passwordHash);
```

## Intentionally vulnerable draft (Part 3 only)

For the exploitation write-up there is a labeled insecure draft:

- UI: http://127.0.0.1:3847/vulnerable.html
- API: `POST /api/insecure-login` (reflects email without escaping)

Do **not** use that page as a template for production. The hardened form at `/` is the secure implementation.

## Assignment write-ups

See [`docs/ASSIGNMENT.md`](docs/ASSIGNMENT.md) and the graded PDF [`docs/submission.pdf`](docs/submission.pdf).

### Repository link

**Public GitHub:** https://github.com/deeps45/juice-guard

## License

MIT
