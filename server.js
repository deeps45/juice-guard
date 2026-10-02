/**
 * Secure Juice Shop–style login API for HW 2B.
 * Security: validation, bcrypt, CSRF tokens, CSP, rate limits, sessions, no dynamic SQL.
 *
 * Also ships /vulnerable + /api/login-vuln as an intentionally broken lab for Part 3
 * so graders can replay a successful XSS (innerHTML reflection, no CSP).
 */
const express = require("express");
const bcrypt = require("bcryptjs");
const path = require("path");
const crypto = require("crypto");
const cookieParser = require("cookie-parser");
const rateLimit = require("express-rate-limit");

const app = express();
const PORT = Number(process.env.PORT) || 3847;
const HOST = process.env.HOST || "0.0.0.0";
const SALT_ROUNDS = 12;

/** Precomputed dummy hash so unknown emails still pay bcrypt.compare cost. */
let DUMMY_PASSWORD_HASH = "";

app.use(express.json({ limit: "16kb" }));
app.use(express.urlencoded({ extended: false, limit: "16kb" }));
app.use(cookieParser());

/** Hardened security headers — skip for the intentional /vulnerable lab pages. */
app.use((req, res, next) => {
  const isVulnLab =
    req.path.startsWith("/vulnerable") || req.path === "/api/login-vuln";
  if (!isVulnLab) {
    res.setHeader(
      "Content-Security-Policy",
      "default-src 'self'; img-src 'self' data:; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; connect-src 'self'; base-uri 'self'; form-action 'self'"
    );
    res.setHeader("X-Frame-Options", "DENY");
  }
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Referrer-Policy", "no-referrer");
  next();
});

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,
  standardHeaders: true,
  legacyHeaders: false,
  message: { ok: false, error: "Too many login attempts. Try again later." },
});

const users = new Map();
/** csrfId -> token */
const csrfStore = new Map();
/** sessionId -> { email, role, createdAt } */
const sessions = new Map();

async function seedUsers() {
  DUMMY_PASSWORD_HASH = await bcrypt.hash(
    crypto.randomBytes(32).toString("hex"),
    SALT_ROUNDS
  );
  const demoHash = await bcrypt.hash("JuiceShop1!", SALT_ROUNDS);
  users.set("demo@juice.shop", {
    email: "demo@juice.shop",
    passwordHash: demoHash,
    role: "customer",
  });
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function isValidEmail(email) {
  if (typeof email !== "string") return false;
  const trimmed = email.trim();
  if (trimmed.length < 5 || trimmed.length > 254) return false;
  if (/[<>'"\\;\x00-\x1f]/.test(trimmed)) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
}

function isValidPassword(password) {
  if (typeof password !== "string") return false;
  if (password.length < 8 || password.length > 128) return false;
  if (/[<>;]|--|\/\*|\*\//.test(password)) return false;
  return true;
}

function requireCsrf(req, res, next) {
  const csrfId = req.cookies?.csrf_id;
  const provided = req.get("x-csrf-token") || req.body?.csrfToken;
  const expected = csrfId ? csrfStore.get(csrfId) : null;

  if (!csrfId || !provided || !expected || provided !== expected) {
    return res.status(403).json({
      ok: false,
      error: "Missing or invalid CSRF token.",
    });
  }
  return next();
}

function createSession(user) {
  const sessionId = crypto.randomBytes(24).toString("hex");
  sessions.set(sessionId, {
    email: user.email,
    role: user.role,
    createdAt: Date.now(),
  });
  if (sessions.size > 2000) {
    const first = sessions.keys().next().value;
    sessions.delete(first);
  }
  return sessionId;
}

app.use(express.static(path.join(__dirname, "public")));

app.get("/api/health", (_req, res) => {
  res.json({ ok: true, service: "secure-login" });
});

app.get("/api/me", (req, res) => {
  const sid = req.cookies?.session;
  const session = sid ? sessions.get(sid) : null;
  if (!session) {
    return res.status(401).json({ ok: false, error: "Not signed in." });
  }
  return res.json({
    ok: true,
    email: session.email,
    role: session.role,
  });
});

app.post("/api/logout", (req, res) => {
  const sid = req.cookies?.session;
  if (sid) sessions.delete(sid);
  res.clearCookie("session", { path: "/" });
  return res.json({ ok: true, message: "Signed out." });
});

/** Issue a per-browser CSRF token (double-submit cookie pattern). */
app.get("/api/csrf", (_req, res) => {
  const csrfId = crypto.randomBytes(16).toString("hex");
  const csrfToken = crypto.randomBytes(24).toString("hex");
  csrfStore.set(csrfId, csrfToken);
  if (csrfStore.size > 2000) {
    const first = csrfStore.keys().next().value;
    csrfStore.delete(first);
  }
  res.cookie("csrf_id", csrfId, {
    httpOnly: true,
    sameSite: "strict",
    secure: false,
    path: "/",
  });
  res.json({ ok: true, csrfToken });
});

app.post("/api/login", loginLimiter, requireCsrf, async (req, res) => {
  try {
    const email = req.body?.email;
    const password = req.body?.password;

    if (!email || !password) {
      return res.status(400).json({
        ok: false,
        error: "Email and password are required.",
      });
    }

    if (!isValidEmail(email)) {
      return res.status(400).json({
        ok: false,
        error: "Enter a valid email address (must contain @ and a domain).",
      });
    }

    if (!isValidPassword(password)) {
      return res.status(400).json({
        ok: false,
        error:
          "Password must be 8–128 characters and must not contain unsafe characters.",
      });
    }

    const normalizedEmail = email.trim().toLowerCase();
    const user = users.get(normalizedEmail);
    // Always bcrypt.compare — unknown emails use a real dummy hash (same cost).
    const hashToCheck = user ? user.passwordHash : DUMMY_PASSWORD_HASH;
    let match = false;
    try {
      match = await bcrypt.compare(password, hashToCheck);
    } catch {
      match = false;
    }

    if (!user || !match) {
      return res.status(401).json({
        ok: false,
        error: "Invalid email or password.",
      });
    }

    const sessionId = createSession(user);
    res.cookie("session", sessionId, {
      httpOnly: true,
      sameSite: "strict",
      secure: false,
      path: "/",
      maxAge: 60 * 60 * 1000,
    });

    return res.json({
      ok: true,
      message: `Welcome back, ${escapeHtml(user.email)}!`,
      role: user.role,
    });
  } catch (err) {
    console.error("Login error:", err.message);
    return res.status(500).json({
      ok: false,
      error: "Something went wrong. Please try again.",
    });
  }
});

/**
 * Intentionally weak login for /vulnerable lab only.
 * - No CSRF
 * - Accepts almost any email (so XSS payloads with @ pass)
 * - Echoes the raw email in JSON (client then uses innerHTML)
 */
app.post("/api/login-vuln", loginLimiter, async (req, res) => {
  const email = typeof req.body?.email === "string" ? req.body.email.trim() : "";
  const password =
    typeof req.body?.password === "string" ? req.body.password : "";

  if (!email || !password) {
    return res.status(400).json({
      ok: false,
      message: "Email and password are required.",
      email,
    });
  }
  if (!email.includes("@")) {
    return res.status(400).json({
      ok: false,
      message: "Email must contain @.",
      email,
    });
  }
  if (password.length < 8) {
    return res.status(400).json({
      ok: false,
      message: "Password must be at least 8 characters.",
      email,
    });
  }

  const normalizedEmail = email.toLowerCase();
  const user = users.get(normalizedEmail);
  const hashToCheck = user ? user.passwordHash : DUMMY_PASSWORD_HASH;
  let match = false;
  try {
    match = await bcrypt.compare(password, hashToCheck);
  } catch {
    match = false;
  }

  if (user && match) {
    return res.json({
      ok: true,
      message: `Welcome back, ${user.email}!`,
      email,
    });
  }
  return res.status(401).json({
    ok: false,
    message: "Invalid email or password.",
    email,
  });
});

app.post("/api/register", loginLimiter, requireCsrf, async (req, res) => {
  try {
    const email = req.body?.email;
    const password = req.body?.password;

    if (!isValidEmail(email) || !isValidPassword(password)) {
      return res.status(400).json({
        ok: false,
        error: "Provide a valid email and a strong password (8+ characters).",
      });
    }

    const normalizedEmail = email.trim().toLowerCase();
    // Anti-enumeration: always spend hashing time; never return 409.
    if (users.has(normalizedEmail)) {
      await bcrypt.hash(password, SALT_ROUNDS);
      return res.status(201).json({
        ok: true,
        message: "If that email is new, the account was created. You can try logging in.",
        hashingExample: {
          algorithm: "bcrypt",
          saltRounds: SALT_ROUNDS,
          note: "Password stored only as an irreversible bcrypt hash.",
        },
      });
    }

    const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
    users.set(normalizedEmail, {
      email: normalizedEmail,
      passwordHash,
      role: "customer",
    });

    return res.status(201).json({
      ok: true,
      message: "If that email is new, the account was created. You can try logging in.",
      hashingExample: {
        algorithm: "bcrypt",
        saltRounds: SALT_ROUNDS,
        note: "Password stored only as an irreversible bcrypt hash.",
      },
    });
  } catch (err) {
    console.error("Register error:", err.message);
    return res.status(500).json({
      ok: false,
      error: "Something went wrong. Please try again.",
    });
  }
});

seedUsers().then(() => {
  app.listen(PORT, HOST, () => {
    console.log(`Secure login demo listening on http://${HOST}:${PORT}`);
    console.log(`Hardened form:   http://127.0.0.1:${PORT}/`);
    console.log(`Vulnerable lab:  http://127.0.0.1:${PORT}/vulnerable/`);
  });
});
