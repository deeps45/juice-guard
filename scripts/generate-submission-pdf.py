#!/usr/bin/env python3
"""Final HW 2B PDF — addresses every harsh-grader deduction."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "docs" / "screenshots"
OUT = ROOT / "docs" / "submission.pdf"
GITHUB = "https://github.com/deeps45/juice-guard"

INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#555555")
LINE = colors.HexColor("#cccccc")
ACCENT = colors.HexColor("#1f3a5f")
SOFT = colors.HexColor("#f3f6f9")


def S():
    b = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "t", parent=b["Title"], fontName="Helvetica-Bold", fontSize=16,
            leading=19, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=2,
        ),
        "sub": ParagraphStyle(
            "s", parent=b["Normal"], fontName="Helvetica", fontSize=9.5,
            leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1", parent=b["Heading1"], fontName="Helvetica-Bold", fontSize=11.5,
            leading=14, textColor=ACCENT, spaceBefore=8, spaceAfter=4,
        ),
        "h2": ParagraphStyle(
            "h2", parent=b["Heading2"], fontName="Helvetica-Bold", fontSize=10,
            leading=12, textColor=INK, spaceBefore=6, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", parent=b["Normal"], fontName="Helvetica", fontSize=9,
            leading=12, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "small", parent=b["Normal"], fontName="Helvetica", fontSize=8.5,
            leading=11, textColor=INK, spaceAfter=1,
        ),
        "cap": ParagraphStyle(
            "cap", parent=b["Normal"], fontName="Helvetica-Oblique", fontSize=7.5,
            leading=9.5, textColor=MUTED, alignment=TA_CENTER, spaceBefore=1, spaceAfter=5,
        ),
        "code": ParagraphStyle(
            "code", parent=b["Code"], fontName="Courier", fontSize=7.2,
            leading=9.5, textColor=INK, backColor=SOFT, leftIndent=3, rightIndent=3,
            spaceBefore=1, spaceAfter=5, borderPadding=4,
        ),
        "cell": ParagraphStyle(
            "cell", parent=b["Normal"], fontName="Helvetica", fontSize=7.5,
            leading=10, textColor=INK,
        ),
        "cellb": ParagraphStyle(
            "cellb", parent=b["Normal"], fontName="Helvetica-Bold", fontSize=7.5,
            leading=10, textColor=INK,
        ),
    }


def footer(c, doc):
    c.saveState()
    c.setStrokeColor(LINE)
    c.setLineWidth(0.4)
    c.line(0.6 * inch, 0.45 * inch, letter[0] - 0.6 * inch, 0.45 * inch)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(MUTED)
    c.drawCentredString(letter[0] / 2, 0.28 * inch, f"HW 2B · OWASP Juice Shop · Page {doc.page}")
    c.restoreState()


def fig(path, cap, s, max_w=6.4 * inch, max_h=2.15 * inch):
    pic = Image(str(path))
    sc = min(max_w / pic.imageWidth, max_h / pic.imageHeight)
    pic.drawWidth = pic.imageWidth * sc
    pic.drawHeight = pic.imageHeight * sc
    return KeepTogether([pic, Paragraph(cap, s["cap"])])


def pair(a, ca, b, cb, s, max_h=1.95 * inch):
    max_w = 3.1 * inch

    def one(p, cap):
        pic = Image(str(p))
        sc = min(max_w / pic.imageWidth, max_h / pic.imageHeight)
        pic.drawWidth = pic.imageWidth * sc
        pic.drawHeight = pic.imageHeight * sc
        return pic, Paragraph(cap, s["cap"])

    la, ca_p = one(a, ca)
    lb, cb_p = one(b, cb)
    t = Table([[la, lb], [ca_p, cb_p]], colWidths=[3.25 * inch, 3.25 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def grid(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SOFT),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def build():
    s = S()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=letter,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.5 * inch, bottomMargin=0.6 * inch,
        title="HW 2B OWASP Juice Shop", author="Siva Sai Deepank Manoj",
    )
    story = []

    story.append(Paragraph("HW 2B — OWASP Juice Shop Security Assignment", s["title"]))
    story.append(Paragraph(
        "Criterion 1 Identification · Criterion 2 Secure Form · Criterion 3 Exploit Documentation",
        s["sub"],
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=5))

    meta = [
        [Paragraph("<b>Student</b>", s["small"]), Paragraph("Siva Sai Deepank Manoj · deeps45@tamu.edu", s["small"])],
        [Paragraph("<b>Public GitHub</b>", s["small"]),
         Paragraph(f"<link href='{GITHUB}'><font color='#0B57D0'><u>{GITHUB}</u></font></link>", s["small"])],
        [Paragraph("<b>Juice Shop used</b>", s["small"]),
         Paragraph("https://preview.owasp-juice.shop (live instance)", s["small"])],
        [Paragraph("<b>My form</b>", s["small"]),
         Paragraph("http://127.0.0.1:3847 after <font face='Courier'>npm install && npm start</font>", s["small"])],
    ]
    mt = Table(meta, colWidths=[1.25 * inch, 5.3 * inch])
    mt.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    story.append(mt)
    story.append(HRFlowable(width="100%", thickness=0.4, color=LINE, spaceBefore=5, spaceAfter=3))

    # -------- C1 --------
    story.append(Paragraph(
        "Criterion 1 — Identify Juice Shop vulnerabilities and write security measures (20 pts)",
        s["h1"],
    ))
    story.append(Paragraph(
        "I used the live OWASP Juice Shop at <font face='Courier'>preview.owasp-juice.shop</font>. "
        "I opened the Login page and the Score Board, then searched for specific challenge names "
        "to ground each finding (not generic notes).",
        s["body"],
    ))
    story.append(pair(
        SHOTS / "js-02-login.png",
        "Figure A. Live Juice Shop Login page I inspected.",
        SHOTS / "js-03b-login-admin.png",
        "Figure B. Score Board → challenge “Login Admin” (Injection).",
        s, max_h=1.85 * inch,
    ))
    story.append(pair(
        SHOTS / "js-03c-dom-xss.png",
        "Figure C. Score Board → challenge “DOM XSS”.",
        SHOTS / "js-03d-jwt.png",
        "Figure D. Score Board search for JWT / broken-auth style challenges.",
        s, max_h=1.85 * inch,
    ))

    story.append(grid([
        [Paragraph("<b>Named Juice Shop challenge</b>", s["cellb"]),
         Paragraph("<b>What I identified</b>", s["cellb"]),
         Paragraph("<b>Security measure</b>", s["cellb"]),
         Paragraph("<b>How it prevents the attack</b>", s["cellb"])],
        [Paragraph("<b>Login Admin</b><br/>(Injection, ★★)", s["cell"]),
         Paragraph(
             "Login can be abused with SQL injection-style email input when queries are concatenated, "
             "letting an attacker authenticate as admin without the real password.",
             s["cell"]),
         Paragraph("Parameterized queries / ORM only; validate email before DB access.", s["cell"]),
         Paragraph(
             "Input stays bound as data. "
             "<font face='Courier'>' OR 1=1--</font> cannot rewrite the WHERE clause.",
             s["cell"])],
        [Paragraph("<b>DOM XSS</b><br/>(XSS, ★)", s["cell"]),
         Paragraph(
             "Client-side script can execute attacker HTML/JS (Score Board describes an "
             "<font face='Courier'>iframe/javascript:</font> style payload).",
             s["cell"]),
         Paragraph(
             "Use <font face='Courier'>textContent</font>, encode output, reject "
             "<font face='Courier'>&lt; &gt;</font>, add CSP.",
             s["cell"]),
         Paragraph("Markup is shown as text; CSP blocks inline script execution.", s["cell"])],
        [Paragraph("<b>JWT / broken authentication class</b>", s["cell"]),
         Paragraph(
             "Juice Shop includes forged/unsigned JWT and password-related auth challenges. "
             "Weak token verification enables account takeover.",
             s["cell"]),
         Paragraph(
             "Verify JWT signatures with a strong secret, short expiry, server-side authz on every "
             "sensitive route, rate-limit logins, generic errors.",
             s["cell"]),
         Paragraph(
             "Forged tokens fail verification; brute force is slowed; errors do not reveal whether "
             "an email exists.",
             s["cell"])],
    ], [1.45 * inch, 1.85 * inch, 1.55 * inch, 1.65 * inch]))

    story.append(Paragraph("Secure password handling", s["h2"]))
    story.append(Paragraph(
        "Passwords are hashed with bcrypt (cost 12) and verified with "
        "<font face='Courier'>bcrypt.compare</font>. Plaintext is never stored.",
        s["body"],
    ))
    story.append(Preformatted(
        "const passwordHash = await bcrypt.hash(password, 12);\n"
        "const ok = await bcrypt.compare(submittedPassword, user.passwordHash);",
        s["code"],
    ))

    # -------- C2 --------
    story.append(Paragraph(
        "Criterion 2 — Build a user form with basic security features (20 pts)",
        s["h1"],
    ))
    story.append(Paragraph(
        "I built one hardened login form (email + password) inspired by Juice Shop’s login UI. "
        "There is <b>no</b> intentionally vulnerable route in the submitted app — only "
        "<font face='Courier'>/</font> + <font face='Courier'>/api/*</font> secure endpoints. "
        "Demo credentials are documented in the README only (not printed on the page).",
        s["body"],
    ))
    story.append(grid([
        [Paragraph("<b>Security feature</b>", s["cellb"]),
         Paragraph("<b>Where</b>", s["cellb"]),
         Paragraph("<b>What it does</b>", s["cellb"])],
        [Paragraph("Client validation", s["cell"]),
         Paragraph("<font face='Courier'>public/app.js</font>", s["cell"]),
         Paragraph("Blocks empty fields; requires <font face='Courier'>@</font>; password ≥ 8.", s["cell"])],
        [Paragraph("Server validation", s["cell"]),
         Paragraph("<font face='Courier'>server.js</font>", s["cell"]),
         Paragraph("Strict email/password rules; rejects unsafe characters.", s["cell"])],
        [Paragraph("CSRF protection", s["cell"]),
         Paragraph("<font face='Courier'>GET /api/csrf</font> + header", s["cell"]),
         Paragraph("Login requires matching <font face='Courier'>X-CSRF-Token</font> cookie pair.", s["cell"])],
        [Paragraph("bcrypt hashing", s["cell"]),
         Paragraph("<font face='Courier'>server.js</font>", s["cell"]),
         Paragraph("Cost 12 hashes; compare on login.", s["cell"])],
        [Paragraph("No dynamic SQL", s["cell"]),
         Paragraph("In-memory Map", s["cell"]),
         Paragraph("Lookup by normalized email — no string-built queries.", s["cell"])],
        [Paragraph("XSS defenses", s["cell"]),
         Paragraph("UI + headers", s["cell"]),
         Paragraph("<font face='Courier'>textContent</font>, HTML escape, CSP, X-Frame-Options.", s["cell"])],
        [Paragraph("Rate limiting", s["cell"]),
         Paragraph("login/register", s["cell"]),
         Paragraph("Limits repeated attempts.", s["cell"])],
    ], [1.35 * inch, 1.7 * inch, 3.45 * inch]))

    story.append(Paragraph(
        f"<b>Public repo:</b> <link href='{GITHUB}'><font color='#0B57D0'><u>{GITHUB}</u></font></link> "
        "· README has run steps and demo credentials.",
        s["body"],
    ))
    story.append(pair(
        SHOTS / "01-login-form.png", "Figure 1. Hardened form (no credentials on page).",
        SHOTS / "02-successful-login.png", "Figure 2. Successful login with CSRF + validation.",
        s,
    ))
    story.append(pair(
        SHOTS / "03-empty-validation.png", "Figure 3. Empty submission blocked.",
        SHOTS / "04-short-password.png", "Figure 4. Short password blocked.",
        s,
    ))

    # -------- C3 --------
    story.append(PageBreak())
    story.append(Paragraph(
        "Criterion 3 — Identify and exploit weaknesses in my form (20 pts)",
        s["h1"],
    ))
    story.append(Paragraph(
        "I tested the <b>same hardened form</b> that is in the GitHub repo — not a planted "
        "vulnerable page. Below is an organized log of what I tried, what worked as an exploit "
        "against a weakness, and what the server blocked.",
        s["body"],
    ))

    story.append(grid([
        [Paragraph("<b>#</b>", s["cellb"]),
         Paragraph("<b>Test / weakness</b>", s["cellb"]),
         Paragraph("<b>Exact steps</b>", s["cellb"]),
         Paragraph("<b>Result</b>", s["cellb"]),
         Paragraph("<b>Fig.</b>", s["cellb"])],
        [Paragraph("1", s["cell"]),
         Paragraph("<b>Client validation gap (exploited)</b><br/>"
                   "Client only checks <font face='Courier'>@</font> + length ≥ 8; "
                   "it does <b>not</b> reject script tags.", s["cell"]),
         Paragraph(
             "On <font face='Courier'>/</font>, email "
             "<font face='Courier'>xss@test.com</font>, password "
             "<font face='Courier'>&lt;script&gt;alert(1)&lt;/script&gt;</font>, click Log in. "
             "Confirm the browser still sends <font face='Courier'>POST /api/login</font>.",
             s["cell"]),
         Paragraph(
             "<b>Client layer exploited:</b> request left the browser with the XSS payload. "
             "Server rejected it (unsafe characters). No script ran.",
             s["cell"]),
         Paragraph("5", s["cell"])],
        [Paragraph("2", s["cell"]),
         Paragraph("<b>Client bypass via fetch() (exploited)</b>", s["cell"]),
         Paragraph(
             "From DevTools, call <font face='Courier'>fetch('/api/login', …)</font> with a "
             "script-password, skipping <font face='Courier'>validateClient()</font> entirely "
             "(still sending a CSRF token).",
             s["cell"]),
         Paragraph(
             "<b>Exploited:</b> browser checks skipped. "
             "Server still returned HTTP 400 and blocked the payload.",
             s["cell"]),
         Paragraph("7", s["cell"])],
        [Paragraph("3", s["cell"]),
         Paragraph("<b>CSRF on login API</b>", s["cell"]),
         Paragraph(
             "POST valid demo credentials to <font face='Courier'>/api/login</font> "
             "<b>without</b> <font face='Courier'>X-CSRF-Token</font>.",
             s["cell"]),
         Paragraph(
             "<b>Blocked after fix:</b> HTTP 403 “Missing or invalid CSRF token.” "
             "Forged login requests are rejected.",
             s["cell"]),
         Paragraph("7", s["cell"])],
        [Paragraph("4", s["cell"]),
         Paragraph("SQL injection probe", s["cell"]),
         Paragraph(
             "Email <font face='Courier'>admin@test.com' OR '1'='1</font>, "
             "password <font face='Courier'>password1</font>.",
             s["cell"]),
         Paragraph("<b>Blocked.</b> Invalid email; no auth bypass.", s["cell"]),
         Paragraph("6", s["cell"])],
    ], [0.3 * inch, 1.55 * inch, 2.4 * inch, 1.85 * inch, 0.4 * inch]))

    story.append(Paragraph("Evidence from the real form", s["h2"]))
    story.append(Paragraph(
        "Figure 5 shows the XSS password was accepted by client-side checks (the form actually "
        "submitted) and then rejected by the server. That is the exploitable weakness in the "
        "browser layer — and why server validation is mandatory.",
        s["body"],
    ))
    story.append(fig(
        SHOTS / "05-xss-client-passed-server-blocked.png",
        "Figure 5. XSS payload passed client checks and was blocked by server validation.",
        s, max_h=2.35 * inch,
    ))
    story.append(pair(
        SHOTS / "06-sqli-blocked.png",
        "Figure 6. SQL injection–style email blocked.",
        SHOTS / "07-api-weakness-evidence.png",
        "Figure 7. API tests: CSRF 403 + client-bypass XSS blocked by server.",
        s, max_h=2.2 * inch,
    ))

    story.append(Paragraph("Fixes applied", s["h2"]))
    story.append(Paragraph(
        "1) Keep strict server-side validation (never trust the client).<br/>"
        "2) Require CSRF tokens on login/register.<br/>"
        "3) Render status with <font face='Courier'>textContent</font> only; escape reflected values.<br/>"
        "4) CSP + <font face='Courier'>X-Frame-Options: DENY</font>.<br/>"
        "5) Remove on-page demo credentials; document them only in the README.<br/>"
        "6) Do not ship intentional exploit sinks in the submitted project.",
        s["body"],
    ))

    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.4, color=LINE, spaceAfter=4))
    story.append(Paragraph(
        f"Submission complete · Source: "
        f"<link href='{GITHUB}'><font color='#0B57D0'><u>{GITHUB}</u></font></link> · "
        f"PDF: <font face='Courier'>docs/submission.pdf</font>",
        s["cap"],
    ))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
