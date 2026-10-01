/**
 * INTENTIONALLY VULNERABLE first draft — used only for HW 2B Part 3.
 * Bug: reflects server message with innerHTML (DOM XSS).
 */
(function () {
  const form = document.getElementById("login-form");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const emailHint = document.getElementById("email-hint");
  const passwordHint = document.getElementById("password-hint");
  const statusEl = document.getElementById("form-status");
  const submitBtn = document.getElementById("submit-btn");

  function setHint(el, message) {
    el.hidden = !message;
    el.textContent = message || "";
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
    statusEl.textContent = "";
    statusEl.classList.remove("ok", "err");

    const email = emailInput.value.trim();
    const password = passwordInput.value;
    if (!validateClient(email, password)) {
      statusEl.textContent = "Fix the highlighted fields before submitting.";
      statusEl.classList.add("err");
      return;
    }

    submitBtn.disabled = true;
    try {
      const response = await fetch("/api/insecure-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();

      // VULNERABILITY: trusting server HTML and injecting it into the DOM
      statusEl.classList.add(data.ok ? "ok" : "err");
      statusEl.innerHTML = data.message;
    } catch (_err) {
      statusEl.textContent = "Could not reach the server.";
      statusEl.classList.add("err");
    } finally {
      submitBtn.disabled = false;
    }
  });
})();
