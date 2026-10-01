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

## Assignment write-ups

See [`docs/ASSIGNMENT.md`](docs/ASSIGNMENT.md) for Parts 1–3, and [`docs/submission.pdf`](docs/submission.pdf) for the PDF submission package (includes screenshots from Part 3).

## License

MIT
