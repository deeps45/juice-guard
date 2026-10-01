#!/usr/bin/env python3
"""Generate the final assignment submission PDF."""

from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "docs" / "screenshots"
OUT = ROOT / "docs" / "submission.pdf"

# Update this after publishing the GitHub repo (Create repo → Public)
GITHUB_URL = "https://github.com/<YOUR_USERNAME>/juice-shop-secure-login"


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontSize=18,
            leading=22,
            spaceAfter=6,
            alignment=TA_CENTER,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "H1Custom",
            parent=base["Heading1"],
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2Custom",
            parent=base["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=base["Normal"],
            fontSize=10.5,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontSize=10,
            leading=13,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["Normal"],
            fontSize=9,
            leading=11,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12,
            textColor="#333333",
        ),
        "code": ParagraphStyle(
            "CodeBlock",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            leftIndent=6,
            spaceBefore=4,
            spaceAfter=10,
            backColor="#F4F4F4",
        ),
        "link": ParagraphStyle(
            "LinkStyle",
            parent=base["Normal"],
            fontSize=10.5,
            leading=14,
            spaceAfter=8,
            textColor="#0B57D0",
        ),
    }


def img(path: Path, max_width=6.4 * inch, max_height=3.6 * inch):
    picture = Image(str(path))
    w, h = picture.imageWidth, picture.imageHeight
    scale = min(max_width / w, max_height / h)
    picture.drawWidth = w * scale
    picture.drawHeight = h * scale
    return picture


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="OWASP Juice Shop Security Assignment",
        author="Siva Sai Deepank Manoj",
    )

    story = []

    story.append(Paragraph("OWASP Juice Shop — Web Security Assignment", s["title"]))
    story.append(
        Paragraph(
            "Secure Feature Design · Login Form Implementation · Exploitation Testing",
            s["subtitle"],
        )
    )
    story.append(Paragraph("<b>Student:</b> Siva Sai Deepank Manoj", s["meta"]))
    story.append(Paragraph("<b>Email:</b> deeps45@tamu.edu", s["meta"]))
    story.append(
        Paragraph(
            "<b>Public GitHub repository:</b> "
            f'<link href="{GITHUB_URL}">{GITHUB_URL}</link>',
            s["meta"],
        )
    )
    story.append(
        Paragraph(
            "<i>If the link above still shows a placeholder, click <b>Create repo</b> "
            "in Cursor, set the repository to <b>Public</b>, then replace the URL in "
            "this PDF / README with your real GitHub clone URL before submitting.</i>",
            s["meta"],
        )
    )
    story.append(Spacer(1, 10))

    # ---------- Part 1 ----------
    story.append(Paragraph("Part 1 — Secure Feature Design", s["h1"]))
    story.append(
        Paragraph(
            "While exploring OWASP Juice Shop, three realistic attack paths stood out "
            "and shaped a secure registration/login design.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>(1) SQL Injection on login.</b> Juice Shop’s login historically accepts "
            "crafted email input that can manipulate a concatenated SQL query and bypass "
            "authentication (classic authentication bypass via injection). "
            "<b>Mitigation:</b> never build SQL from raw strings — use parameterized "
            "queries or an ORM lookup keyed by email. Reject malformed emails before "
            "they reach the data layer. This prevents the attacker’s payload from "
            "changing query logic.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>(2) Cross-Site Scripting (XSS).</b> Search boxes and user-controlled "
            "fields (reviews, names) can reflect or store HTML/JavaScript that runs in "
            "another user’s browser, stealing sessions or defacing pages. "
            "<b>Mitigation:</b> encode all untrusted output for the correct context, "
            "prefer <font face='Courier'>textContent</font> over "
            "<font face='Courier'>innerHTML</font>, set a Content-Security-Policy, and "
            "reject angle brackets / event-handler patterns on input. Encoding ensures "
            "scripts are displayed as text, not executed.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>(3) Authentication bypass / weak token handling.</b> Predictable or "
            "poorly verified session tokens let attackers impersonate administrators. "
            "<b>Mitigation:</b> issue signed tokens with strong secrets, short expiry, "
            "and server-side authorization checks on every sensitive route. Combined "
            "with rate limiting and generic login errors (no user enumeration), forged "
            "or replayed credentials are far harder to abuse.",
            s["body"],
        )
    )
    story.append(Paragraph("Secure password handling (bcrypt example)", s["h2"]))
    story.append(
        Paragraph(
            "Passwords must never be stored in plaintext. At registration, hash once "
            "with a high bcrypt cost factor; at login, compare with "
            "<font face='Courier'>bcrypt.compare</font>:",
            s["body"],
        )
    )
    story.append(
        Preformatted(
            "const passwordHash = await bcrypt.hash(password, 12);\n"
            "// store passwordHash only — never the plaintext\n\n"
            "const match = await bcrypt.compare(submittedPassword, user.passwordHash);\n"
            "if (!match) return res.status(401).json({ error: 'Invalid email or password.' });",
            s["code"],
        )
    )
    story.append(
        Paragraph(
            "Bcrypt embeds a salt and is deliberately slow, which resists rainbow tables "
            "and offline brute force. Even if the database leaks, attackers obtain hashes, "
            "not reusable passwords.",
            s["body"],
        )
    )

    # ---------- Part 2 ----------
    story.append(Paragraph("Part 2 — Simple Front-End Login Form", s["h1"]))
    story.append(
        Paragraph(
            "I implemented a Juice Shop–style login page using plain HTML, CSS, and "
            "JavaScript on the client, plus a small Express server for real "
            "server-side validation and bcrypt password verification.",
            s["body"],
        )
    )
    story.append(Paragraph("What the form includes", s["h2"]))
    story.append(
        Paragraph(
            "• Email and password inputs with labels and accessible status messaging.<br/>"
            "• <b>Client-side validation</b> (<font face='Courier'>public/app.js</font>): "
            "blocks empty submissions; requires the email to contain "
            "<font face='Courier'>@</font>; requires password length ≥ 8.<br/>"
            "• <b>Server-side validation</b> (<font face='Courier'>server.js</font>): "
            "re-checks email format, password length, and unsafe characters; looks up "
            "users without string-built SQL; verifies passwords with bcryptjs "
            "(cost 12); returns generic errors; rate-limits login attempts.<br/>"
            "• Status text is set with <font face='Courier'>textContent</font> to avoid DOM XSS.",
            s["body"],
        )
    )
    story.append(Paragraph("How to run", s["h2"]))
    story.append(
        Preformatted(
            "npm install\nnpm start\n# open http://127.0.0.1:3847\n"
            "# demo account: demo@juice.shop / JuiceShop1!",
            s["code"],
        )
    )
    story.append(Paragraph("GitHub repository (must be public)", s["h2"]))
    story.append(
        Paragraph(
            f'<link href="{GITHUB_URL}"><b>{GITHUB_URL}</b></link>',
            s["link"],
        )
    )
    story.append(
        Paragraph(
            "The repository README explains the project purpose, structure, bcrypt "
            "example, and run instructions. Source files: "
            "<font face='Courier'>public/index.html</font>, "
            "<font face='Courier'>public/app.js</font>, "
            "<font face='Courier'>server.js</font>.",
            s["body"],
        )
    )
    story.append(
        KeepTogether(
            [
                img(SHOTS / "01-login-form.png"),
                Paragraph("Figure 1. Secure login form UI (Part 2 implementation).", s["caption"]),
            ]
        )
    )
    story.append(
        KeepTogether(
            [
                img(SHOTS / "02-successful-login.png"),
                Paragraph(
                    "Figure 2. Successful login with demo credentials after client + server checks.",
                    s["caption"],
                ),
            ]
        )
    )
    story.append(
        KeepTogether(
            [
                img(SHOTS / "03-empty-validation.png"),
                Paragraph(
                    "Figure 3. Client-side validation blocking empty email/password submission.",
                    s["caption"],
                ),
            ]
        )
    )
    story.append(
        KeepTogether(
            [
                img(SHOTS / "04-short-password.png"),
                Paragraph(
                    "Figure 4. Client-side check requiring passwords of at least 8 characters.",
                    s["caption"],
                ),
            ]
        )
    )

    # ---------- Part 3 ----------
    story.append(PageBreak())
    story.append(Paragraph("Part 3 — Exploitation Attempts Against My Form", s["h1"]))
    story.append(
        Paragraph(
            "I attempted common login attacks against my own form to verify the defenses. "
            "Both attempts were blocked — evidence that validation and safe rendering are working.",
            s["body"],
        )
    )
    story.append(Paragraph("Attempt A — Cross-Site Scripting (XSS)", s["h2"]))
    story.append(
        Paragraph(
            "<b>Steps:</b> (1) Open the login page. (2) Enter email "
            "<font face='Courier'>xss@test.com</font>. (3) Enter password "
            "<font face='Courier'>&lt;script&gt;alert(1)&lt;/script&gt;</font>. "
            "(4) Click Log in. (5) Observe whether a JavaScript alert appears or script executes.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Result:</b> The attack <b>did not succeed</b>. No alert dialog opened. "
            "The server rejected the password because it contains unsafe characters "
            "(&lt; &gt;). The UI also renders messages with "
            "<font face='Courier'>textContent</font>, so even reflected strings would not execute as HTML.",
            s["body"],
        )
    )
    story.append(
        KeepTogether(
            [
                img(SHOTS / "05-xss-blocked.png"),
                Paragraph(
                    "Figure 5. XSS payload rejected — server error: unsafe characters in password.",
                    s["caption"],
                ),
            ]
        )
    )

    story.append(Paragraph("Attempt B — SQL Injection", s["h2"]))
    story.append(
        Paragraph(
            "<b>Steps:</b> (1) Reload the login page. (2) Enter email "
            "<font face='Courier'>admin@test.com' OR '1'='1</font>. "
            "(3) Enter password <font face='Courier'>password1</font>. "
            "(4) Click Log in. (5) Check whether authentication was bypassed or data leaked.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Result:</b> The attack <b>did not succeed</b>. The application rejected "
            "the malformed email and never concatenates user input into SQL (users are "
            "stored in an in-memory Map looked up by normalized email). No admin access "
            "and no credential dump occurred.",
            s["body"],
        )
    )
    story.append(
        KeepTogether(
            [
                img(SHOTS / "06-sqli-blocked.png"),
                Paragraph(
                    "Figure 6. SQL injection–style email rejected as an invalid email address.",
                    s["caption"],
                ),
            ]
        )
    )

    story.append(Paragraph("Suggested hardening fix", s["h2"]))
    story.append(
        Paragraph(
            "Even though exploitation failed, one additional fix I would apply is a strict "
            "<b>Content-Security-Policy</b> header (for example "
            "<font face='Courier'>default-src 'self'; script-src 'self'</font>) plus "
            "HTML sanitization for any future user-visible fields. CSP provides defense "
            "in depth: if a future change accidentally uses "
            "<font face='Courier'>innerHTML</font>, the browser still blocks inline script execution.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Learning:</b> Client checks improve UX, but server validation, bcrypt "
            "hashing, safe DOM updates, and avoiding dynamic SQL are what actually stop "
            "SQLi and XSS. Failing to break my own form is a positive outcome for secure design.",
            s["body"],
        )
    )

    story.append(Spacer(1, 16))
    story.append(Paragraph("Appendix — Repository checklist for graders", s["h1"]))
    story.append(
        Paragraph(
            "• Public GitHub repo with README (what it does + how to run)<br/>"
            "• HTML/JS login form with email + password fields<br/>"
            "• Client validation: non-empty, email contains @, password ≥ 8 chars<br/>"
            "• Server validation + bcrypt password hashing<br/>"
            "• Part 1–3 write-ups with screenshots of blocked XSS/SQLi attempts",
            s["body"],
        )
    )

    doc.build(story)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
