#!/usr/bin/env python3
"""HW 2B submission PDF — aligned to the 60-point rubric."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
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
GITHUB_URL = "https://github.com/deeps45/juice-guard"

INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#555555")
LINE = colors.HexColor("#cccccc")
ACCENT = colors.HexColor("#1f3a5f")
SOFT = colors.HexColor("#f3f6f9")


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=ACCENT,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=ACCENT,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "subsection": ParagraphStyle(
            "Subsection",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13.5,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            leading=10.5,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8,
            leading=10.5,
            textColor=INK,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=2,
            spaceAfter=8,
            backColor=SOFT,
            borderPadding=5,
        ),
        "cell": ParagraphStyle(
            "Cell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=INK,
        ),
        "cell_b": ParagraphStyle(
            "CellB",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=INK,
        ),
    }


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(0.7 * inch, 0.5 * inch, letter[0] - 0.7 * inch, 0.5 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(
        letter[0] / 2, 0.32 * inch, f"HW 2B · OWASP Juice Shop  ·  Page {doc.page}"
    )
    canvas.restoreState()


def figure(path, caption, s, max_w=6.3 * inch, max_h=2.45 * inch):
    pic = Image(str(path))
    scale = min(max_w / pic.imageWidth, max_h / pic.imageHeight)
    pic.drawWidth = pic.imageWidth * scale
    pic.drawHeight = pic.imageHeight * scale
    return KeepTogether([pic, Paragraph(caption, s["caption"])])


def figure_pair(a, ca, b, cb, s):
    max_w, max_h = 3.05 * inch, 2.2 * inch

    def one(path, cap):
        pic = Image(str(path))
        scale = min(max_w / pic.imageWidth, max_h / pic.imageHeight)
        pic.drawWidth = pic.imageWidth * scale
        pic.drawHeight = pic.imageHeight * scale
        return pic, Paragraph(cap, s["caption"])

    la, ca_p = one(a, ca)
    lb, cb_p = one(b, cb)
    t = Table([[la, lb], [ca_p, cb_p]], colWidths=[3.2 * inch, 3.2 * inch])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def meta_table(s):
    data = [
        [
            Paragraph("<b>Student</b>", s["small"]),
            Paragraph("Siva Sai Deepank Manoj", s["small"]),
        ],
        [
            Paragraph("<b>Email</b>", s["small"]),
            Paragraph("deeps45@tamu.edu", s["small"]),
        ],
        [
            Paragraph("<b>Public GitHub</b>", s["small"]),
            Paragraph(
                f"<link href='{GITHUB_URL}'><font color='#0B57D0'><u>{GITHUB_URL}</u></font></link>",
                s["small"],
            ),
        ],
        [
            Paragraph("<b>Course item</b>", s["small"]),
            Paragraph("HW 2B — OWASP Juice Shop (60 pts)", s["small"]),
        ],
    ]
    t = Table(data, colWidths=[1.3 * inch, 5.2 * inch])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return t


def vuln_table(s):
    """Criterion 1: identification + security measures."""
    rows = [
        [
            Paragraph("<b>Vulnerability in Juice Shop</b>", s["cell_b"]),
            Paragraph("<b>Security measure</b>", s["cell_b"]),
            Paragraph("<b>How it stops the attack</b>", s["cell_b"]),
        ],
        [
            Paragraph(
                "<b>SQL injection on login</b><br/>Crafted email input can "
                "change a concatenated SQL query and skip the password check "
                "(classic Juice Shop login challenge).",
                s["cell"],
            ),
            Paragraph(
                "Use parameterized queries / ORM lookups only. Validate email "
                "format before the database call.",
                s["cell"],
            ),
            Paragraph(
                "User input stays bound as data, so quotes and "
                "<font face='Courier'>OR 1=1</font> cannot change query logic "
                "or bypass authentication.",
                s["cell"],
            ),
        ],
        [
            Paragraph(
                "<b>Cross-site scripting (XSS)</b><br/>Search / review fields "
                "can reflect or store HTML/JS that runs in another user’s browser.",
                s["cell"],
            ),
            Paragraph(
                "Encode output; use <font face='Courier'>textContent</font>; "
                "reject <font face='Courier'>&lt; &gt;</font> on input; set "
                "Content-Security-Policy.",
                s["cell"],
            ),
            Paragraph(
                "Scripts are shown as text instead of executed, and CSP blocks "
                "inline script even if rendering slips.",
                s["cell"],
            ),
        ],
        [
            Paragraph(
                "<b>Authentication bypass / weak sessions</b><br/>Weak or "
                "predictable tokens can let an attacker impersonate another account.",
                s["cell"],
            ),
            Paragraph(
                "Signed short-lived tokens, server-side authorization on every "
                "sensitive route, rate limits, generic login errors.",
                s["cell"],
            ),
            Paragraph(
                "Stolen or guessed tokens expire quickly; brute force is slowed; "
                "attackers cannot enumerate valid emails from error text.",
                s["cell"],
            ),
        ],
    ]
    t = Table(rows, colWidths=[2.35 * inch, 2.0 * inch, 2.15 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def feature_table(s):
    """Criterion 2: security measures built into the form."""
    rows = [
        [
            Paragraph("<b>Security feature in my form</b>", s["cell_b"]),
            Paragraph("<b>Where</b>", s["cell_b"]),
            Paragraph("<b>What it does</b>", s["cell_b"]),
        ],
        [
            Paragraph("Client validation", s["cell"]),
            Paragraph("<font face='Courier'>public/app.js</font>", s["cell"]),
            Paragraph(
                "Blocks empty fields; email must contain "
                "<font face='Courier'>@</font>; password ≥ 8 characters.",
                s["cell"],
            ),
        ],
        [
            Paragraph("Server validation", s["cell"]),
            Paragraph("<font face='Courier'>server.js</font>", s["cell"]),
            Paragraph(
                "Re-checks email/password; rejects unsafe characters; never trusts the browser alone.",
                s["cell"],
            ),
        ],
        [
            Paragraph("bcrypt password hashing", s["cell"]),
            Paragraph("<font face='Courier'>server.js</font>", s["cell"]),
            Paragraph(
                "Stores only bcrypt hashes (cost 12); login uses "
                "<font face='Courier'>bcrypt.compare</font>.",
                s["cell"],
            ),
        ],
        [
            Paragraph("No dynamic SQL", s["cell"]),
            Paragraph("<font face='Courier'>server.js</font>", s["cell"]),
            Paragraph(
                "Users live in an in-memory map keyed by email — input is never concatenated into SQL.",
                s["cell"],
            ),
        ],
        [
            Paragraph("XSS-safe UI + CSP", s["cell"]),
            Paragraph("UI + HTTP headers", s["cell"]),
            Paragraph(
                "Status text via <font face='Courier'>textContent</font>; "
                "Content-Security-Policy blocks inline scripts.",
                s["cell"],
            ),
        ],
        [
            Paragraph("Rate limiting", s["cell"]),
            Paragraph("<font face='Courier'>/api/login</font>", s["cell"]),
            Paragraph("Limits repeated login attempts to slow brute-force guessing.", s["cell"]),
        ],
    ]
    t = Table(rows, colWidths=[1.7 * inch, 1.5 * inch, 3.3 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def exploit_table(s):
    """Criterion 3: organized exploit documentation."""
    rows = [
        [
            Paragraph("<b>Test</b>", s["cell_b"]),
            Paragraph("<b>Exact input / steps</b>", s["cell_b"]),
            Paragraph("<b>Outcome</b>", s["cell_b"]),
            Paragraph("<b>Evidence</b>", s["cell_b"]),
        ],
        [
            Paragraph("XSS", s["cell"]),
            Paragraph(
                "Email: <font face='Courier'>xss@test.com</font><br/>"
                "Password: <font face='Courier'>&lt;script&gt;alert(1)&lt;/script&gt;</font><br/>"
                "Click Log in; watch for an alert.",
                s["cell"],
            ),
            Paragraph(
                "<b>Blocked.</b> No alert. Server rejected unsafe characters. "
                "UI uses textContent.",
                s["cell"],
            ),
            Paragraph("Figure 5", s["cell"]),
        ],
        [
            Paragraph("SQL injection", s["cell"]),
            Paragraph(
                "Email: <font face='Courier'>admin@test.com' OR '1'='1</font><br/>"
                "Password: <font face='Courier'>password1</font><br/>"
                "Submit and check for auth bypass.",
                s["cell"],
            ),
            Paragraph(
                "<b>Blocked.</b> Invalid email. No SQL concatenation. "
                "No credential leak.",
                s["cell"],
            ),
            Paragraph("Figure 6", s["cell"]),
        ],
        [
            Paragraph("Weakness found", s["cell"]),
            Paragraph(
                "Client checks only require <font face='Courier'>@</font> and "
                "password length ≥ 8. The XSS string passes the <b>client</b> "
                "and reaches the API — only the <b>server</b> stops it.",
                s["cell"],
            ),
            Paragraph(
                "<b>Partial weakness:</b> client validation alone is not enough. "
                "If server checks were removed, unsafe input would be accepted.",
                s["cell"],
            ),
            Paragraph("Fix: keep server validation + CSP", s["cell"]),
        ],
    ]
    t = Table(rows, colWidths=[1.05 * inch, 2.45 * inch, 2.0 * inch, 1.0 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.7 * inch,
        title="HW 2B — OWASP Juice Shop",
        author="Siva Sai Deepank Manoj",
    )
    story = []

    # Cover
    story.append(Paragraph("HW 2B — OWASP Juice Shop", s["title"]))
    story.append(
        Paragraph(
            "Identification · Secure Login Form · Exploitation Documentation",
            s["subtitle"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    story.append(meta_table(s))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            "<b>Rubric map (60 pts):</b> Criterion 1 Identification (20) · "
            "Criterion 2 Secure form (20) · Criterion 3 Exploit documentation (20)",
            s["small"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=6, spaceAfter=4))

    # ===== Criterion 1 =====
    story.append(
        Paragraph(
            "Criterion 1 — Identification (20 pts): Juice Shop vulnerabilities &amp; security measures",
            s["section"],
        )
    )
    story.append(
        Paragraph(
            "While exploring OWASP Juice Shop, I focused on login and user-controlled "
            "fields. I identified three realistic vulnerabilities and designed security "
            "measures for each one.",
            s["body"],
        )
    )
    story.append(vuln_table(s))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Secure password handling (bcrypt example)", s["subsection"]))
    story.append(
        Paragraph(
            "For registration/login design, passwords are never stored in plaintext. "
            "I hash with bcrypt (cost 12) and verify with "
            "<font face='Courier'>bcrypt.compare</font>:",
            s["body"],
        )
    )
    story.append(
        Preformatted(
            "const passwordHash = await bcrypt.hash(password, 12);\n"
            "const ok = await bcrypt.compare(submittedPassword, user.passwordHash);\n"
            "if (!ok) return res.status(401).json({ error: 'Invalid email or password.' });",
            s["code"],
        )
    )

    # ===== Criterion 2 =====
    story.append(
        Paragraph(
            "Criterion 2 — Build a user form with basic security features (20 pts)",
            s["section"],
        )
    )
    story.append(
        Paragraph(
            "I built a Juice Shop–style login form in HTML + JavaScript with an Express "
            "backend. Security was part of the design, not an afterthought. The form "
            "includes email and password fields, client-side validation, and matching "
            "server-side validation.",
            s["body"],
        )
    )
    story.append(feature_table(s))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            f"<b>Public GitHub repository (with README):</b> "
            f"<link href='{GITHUB_URL}'><font color='#0B57D0'><u>{GITHUB_URL}</u></font></link>",
            s["body"],
        )
    )
    story.append(
        Preformatted(
            "git clone https://github.com/deeps45/juice-guard.git && cd juice-guard\n"
            "npm install && npm start   # http://127.0.0.1:3847\n"
            "# demo: demo@juice.shop / JuiceShop1!",
            s["code"],
        )
    )
    story.append(
        figure_pair(
            SHOTS / "01-login-form.png",
            "Figure 1. Secure login form UI.",
            SHOTS / "02-successful-login.png",
            "Figure 2. Successful login after checks.",
            s,
        )
    )
    story.append(
        figure_pair(
            SHOTS / "03-empty-validation.png",
            "Figure 3. Empty submission blocked.",
            SHOTS / "04-short-password.png",
            "Figure 4. Short password blocked.",
            s,
        )
    )

    # ===== Criterion 3 =====
    story.append(PageBreak())
    story.append(
        Paragraph(
            "Criterion 3 — Identify &amp; exploit weaknesses in my form (20 pts)",
            s["section"],
        )
    )
    story.append(
        Paragraph(
            "I tried to break my own login form the same way Juice Shop is often attacked. "
            "Below is organized documentation of each attempt, the exact steps, the result, "
            "and a weakness I still found in the design.",
            s["body"],
        )
    )
    story.append(exploit_table(s))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Exploit attempt details", s["subsection"]))
    story.append(
        Paragraph(
            "<b>XSS steps:</b> open the form → email "
            "<font face='Courier'>xss@test.com</font> → password "
            "<font face='Courier'>&lt;script&gt;alert(1)&lt;/script&gt;</font> → Log in. "
            "<b>Result:</b> no JavaScript alert; server returned an unsafe-character error. "
            "Screenshot in Figure 5.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>SQL injection steps:</b> reload → email "
            "<font face='Courier'>admin@test.com' OR '1'='1</font> → password "
            "<font face='Courier'>password1</font> → Log in. "
            "<b>Result:</b> rejected as an invalid email; no auth bypass. Screenshot in Figure 6.",
            s["body"],
        )
    )
    story.append(
        figure(
            SHOTS / "05-xss-blocked.png",
            "Figure 5. XSS exploit attempt — blocked (no script execution).",
            s,
            max_h=2.55 * inch,
        )
    )
    story.append(
        figure(
            SHOTS / "06-sqli-blocked.png",
            "Figure 6. SQL injection exploit attempt — blocked by validation.",
            s,
            max_h=2.55 * inch,
        )
    )

    story.append(Paragraph("Weakness identified + fix", s["subsection"]))
    story.append(
        Paragraph(
            "Even though XSS and SQLi did not succeed end-to-end, I found a real design "
            "weakness: <b>the browser-side checks are too weak by themselves</b>. The "
            "client only requires <font face='Courier'>@</font> and a password length of 8, "
            "so the XSS string is sent to the server. If someone later removed server "
            "validation, the form would become exploitable. "
            "<b>Fix I applied:</b> keep strict server-side validation and add a "
            "Content-Security-Policy header (<font face='Courier'>script-src 'self'</font>) "
            "so inline scripts cannot run even if UI code regresses.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "Takeaway: failing to fully exploit the finished form is good, but documenting "
            "attempts and calling out residual weaknesses (over-reliance on the client) "
            "is what shows the security work.",
            s["body"],
        )
    )

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=6))
    story.append(
        Paragraph(
            f"End of HW 2B submission · "
            f"<link href='{GITHUB_URL}'><font color='#0B57D0'><u>{GITHUB_URL}</u></font></link>",
            s["caption"],
        )
    )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
