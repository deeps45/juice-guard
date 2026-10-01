/**
 * Secure Juice Shop–style login API for HW 2B.
 * Security: validation, bcrypt, CSRF tokens, CSP, rate limits, no dynamic SQL.
 */
const express = require("express");
const bcrypt = require("bcryptjs");
const path = require("path");
const crypto = require("crypto");
const cookieParser = require("cookie-parser");
const rateLimit = require("express-rate-limit");

const app = express();
const PORT = process.env.PORT || 3847;
const SALT_ROUNDS = 12;

app.use(express.json({ limit: "16kb" }));
app.use(express.urlencoded({ extended: false, limit: "16kb" }));
app.use(cookieParser());

app.use((_req, res, next) => {
  res.setHeader(
    "Content-Security-Policy",
    "default-src 'self'; img-src 'self' data:; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; connect-src 'self'; base-uri 'self'; form-action 'self'"
  );
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("X-Frame-Options", "DENY");
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

async function seedUsers() {
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

app.use(express.static(path.join(__dirname, "public")));

app.get("/api/health", (_req, res) => {
  res.json({ ok: true, service: "secure-login" });
});

/** Issue a per-browser CSRF token (double-submit cookie pattern). */
app.get("/api/csrf", (_req, res) => {
  const csrfId = crypto.randomBytes(16).toString("hex");
  const csrfToken = crypto.randomBytes(24).toString("hex");
  csrfStore.set(csrfId, csrfToken);
  // avoid unbounded growth in long-running demos
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
    const hashToCheck = user
      ? user.passwordHash
      : "$2b$12$invalidhashpaddinginvalidhashpaddinginv";

    let match = false;
    try {
      match = user ? await bcrypt.compare(password, hashToCheck) : false;
    } catch {
      match = false;
    }

    if (!user || !match) {
      return res.status(401).json({
        ok: false,
        error: "Invalid email or password.",
      });
    }

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
    if (users.has(normalizedEmail)) {
      return res.status(409).json({
        ok: false,
        error: "Unable to create account with that email.",
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
      message: "Account created. You can now log in.",
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
  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Secure login demo listening on http://127.0.0.1:${PORT}`);
  });
});
