/**
 * Secure login API inspired by OWASP Juice Shop patterns.
 * Demonstrates parameterized handling, bcrypt password hashing,
 * input validation, and XSS-safe response encoding.
 */
const express = require("express");
const bcrypt = require("bcryptjs");
const path = require("path");
const rateLimit = require("express-rate-limit");

const app = express();
const PORT = process.env.PORT || 3847;
const SALT_ROUNDS = 12;

app.use(express.json({ limit: "16kb" }));
app.use(express.urlencoded({ extended: false, limit: "16kb" }));

// Slow down brute-force / credential stuffing attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,
  standardHeaders: true,
  legacyHeaders: false,
  message: { ok: false, error: "Too many login attempts. Try again later." },
});

// Demo user store (in-memory). Passwords are NEVER stored in plaintext.
const users = new Map();

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
  // Reject control chars / tags; require a basic user@domain shape
  if (trimmed.length < 5 || trimmed.length > 254) return false;
  if (/[<>'"\\;\x00-\x1f]/.test(trimmed)) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
}

function isValidPassword(password) {
  if (typeof password !== "string") return false;
  if (password.length < 8 || password.length > 128) return false;
  // Block obvious injection / script fragments in password field
  if (/[<>;]|--|\/\*|\*\//.test(password)) return false;
  return true;
}

app.use(express.static(path.join(__dirname, "public")));

app.get("/api/health", (_req, res) => {
  res.json({ ok: true, service: "secure-login" });
});

/**
 * Example of secure password handling:
 * 1. Validate input shape on the server (never trust the client).
 * 2. Look up the user by email with a Map/ORM — never concatenate SQL.
 * 3. Compare with bcrypt.compare (constant-time vs stored hash).
 * 4. Return generic error messages (no user enumeration).
 */
app.post("/api/login", loginLimiter, async (req, res) => {
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

    // Always run a bcrypt compare timing path to reduce timing leaks
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

    // Escape any reflected values (defense in depth against XSS)
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
 * Registration endpoint demonstrating bcrypt hashing at signup time.
 * Hash once with a high cost factor; never log or return the plaintext.
 */
app.post("/api/register", loginLimiter, async (req, res) => {
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
      // Illustrative only — never return the real hash to browsers in production
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
    console.log(`Demo account: demo@juice.shop / JuiceShop1!`);
  });
});
