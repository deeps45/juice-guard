/**
 * Client-side validation + CSRF-protected login for the hardened form.
 */
(function () {
  const form = document.getElementById("login-form");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const emailHint = document.getElementById("email-hint");
  const passwordHint = document.getElementById("password-hint");
  const statusEl = document.getElementById("form-status");
  const submitBtn = document.getElementById("submit-btn");

  let csrfToken = "";

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

  async function refreshCsrf() {
    const res = await fetch("/api/csrf", { credentials: "same-origin" });
    const data = await res.json();
    if (!res.ok || !data.csrfToken) {
      throw new Error("Could not fetch CSRF token");
    }
    csrfToken = data.csrfToken;
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

  refreshCsrf().catch(() => {
    setStatus("Could not initialize CSRF protection. Refresh the page.", "err");
  });

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    setStatus("");

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!validateClient(email, password)) {
      setStatus("Fix the highlighted fields before submitting.", "err");
      return;
    }

    submitBtn.disabled = true;
    setStatus("Checking credentials…");

    try {
      if (!csrfToken) await refreshCsrf();

      const response = await fetch("/api/login", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": csrfToken,
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok || !data.ok) {
        setStatus(data.error || "Login failed.", "err");
        // rotate token after failures too
        await refreshCsrf().catch(() => {});
        return;
      }

      setStatus(data.message, "ok");
      await refreshCsrf().catch(() => {});
    } catch (_err) {
      setStatus("Could not reach the server. Is it running?", "err");
    } finally {
      submitBtn.disabled = false;
    }
  });
})();
