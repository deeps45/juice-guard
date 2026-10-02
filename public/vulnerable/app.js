/**
 * Intentionally vulnerable login UI for Part 3 exploit replay.
 * - Client validation only (@ + length)
 * - Reflects email with innerHTML (XSS sink)
 * - No CSRF header; talks to a relaxed demo endpoint
 */
(function () {
  const form = document.getElementById("login-form");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const emailHint = document.getElementById("email-hint");
  const passwordHint = document.getElementById("password-hint");
  const statusEl = document.getElementById("form-status");
  const reflected = document.getElementById("reflected");
  const submitBtn = document.getElementById("submit-btn");

  function setHint(el, message) {
    if (!message) {
      el.hidden = true;
      el.textContent = "";
      return;
    }
    el.hidden = false;
    el.textContent = message;
  }

  function setStatus(message, type) {
    statusEl.textContent = message;
    statusEl.classList.remove("ok", "err");
    if (type) statusEl.classList.add(type);
  }

  function validateClient(email, password) {
    let valid = true;
    emailInput.classList.remove("invalid");
    passwordInput.classList.remove("invalid");
    setHint(emailHint, "");
    setHint(passwordHint, "");

    if (!email) {
      setHint(emailHint, "Email cannot be empty.");
      emailInput.classList.add("invalid");
      valid = false;
    } else if (!email.includes("@")) {
      setHint(emailHint, 'Email must contain an "@" symbol.');
      emailInput.classList.add("invalid");
      valid = false;
    }

    if (!password) {
      setHint(passwordHint, "Password cannot be empty.");
      passwordInput.classList.add("invalid");
      valid = false;
    } else if (password.length < 8) {
      setHint(passwordHint, "Password must be at least 8 characters.");
      passwordInput.classList.add("invalid");
      valid = false;
    }

    return valid;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    setStatus("");
    reflected.innerHTML = "";

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!validateClient(email, password)) {
      setStatus("Fix the highlighted fields before submitting.", "err");
      return;
    }

    submitBtn.disabled = true;
    setStatus("Checking credentials…");

    try {
      const response = await fetch("/api/login-vuln", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      setStatus(data.message || data.error || "Done.", data.ok ? "ok" : "err");
      // VULNERABLE: unescaped email reflected into the DOM
      reflected.innerHTML = "Submitted email: " + email;
    } catch (_err) {
      setStatus("Could not reach the server. Is it running?", "err");
      reflected.innerHTML = "Submitted email: " + email;
    } finally {
      submitBtn.disabled = false;
    }
  });
})();
