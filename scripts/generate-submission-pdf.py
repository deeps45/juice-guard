#!/usr/bin/env python3
"""Generate a clean, rubric-aligned assignment submission PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
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


def make_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=ACCENT,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=3,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=ACCENT,
            spaceBefore=16,
            spaceAfter=8,
        ),
        "subsection": ParagraphStyle(
            "Subsection",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14.5,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=11,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=11.5,
            textColor=INK,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=2,
            spaceAfter=10,
            backColor=colors.HexColor("#f5f5f5"),
            borderPadding=6,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(0.75 * inch, 0.55 * inch, letter[0] - 0.75 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(
        letter[0] / 2,
        0.35 * inch,
        f"OWASP Juice Shop Security Assignment  ·  Page {doc.page}",
    )
    canvas.restoreState()


def figure(path: Path, caption: str, styles, max_w=6.2 * inch, max_h=2.55 * inch):
    picture = Image(str(path))
    scale = min(max_w / picture.imageWidth, max_h / picture.imageHeight)
    picture.drawWidth = picture.imageWidth * scale
    picture.drawHeight = picture.imageHeight * scale
    return KeepTogether([picture, Paragraph(caption, styles["caption"])])


def figure_pair(path_a: Path, cap_a: str, path_b: Path, cap_b: str, styles):
    """Two compact screenshots side by side for denser layout."""
    max_w, max_h = 3.05 * inch, 2.35 * inch

    def one(path, cap):
        picture = Image(str(path))
        scale = min(max_w / picture.imageWidth, max_h / picture.imageHeight)
        picture.drawWidth = picture.imageWidth * scale
        picture.drawHeight = picture.imageHeight * scale
        return [picture, Paragraph(cap, styles["caption"])]

    left = one(path_a, cap_a)
    right = one(path_b, cap_b)
    table = Table([[left[0], right[0]], [left[1], right[1]]], colWidths=[3.2 * inch, 3.2 * inch])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.75 * inch,
        title="OWASP Juice Shop Security Assignment",
        author="Siva Sai Deepank Manoj",
    )

    story = []

    # ---------- Cover ----------
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("OWASP Juice Shop", styles["cover_title"]))
    story.append(Paragraph("Web Security Assignment Submission", styles["cover_sub"]))
    story.append(
        HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=2, spaceAfter=14)
    )

    meta_data = [
        ["Student", "Siva Sai Deepank Manoj"],
        ["Email", "deeps45@tamu.edu"],
        ["GitHub (public)", GITHUB_URL],
        ["Demo account", "demo@juice.shop / JuiceShop1!"],
    ]
    meta_table = Table(meta_data, colWidths=[1.45 * inch, 5.0 * inch])
    meta_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10.5),
                ("TEXTCOLOR", (0, 0), (-1, -1), INK),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 0.12 * inch))
    story.append(
        HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=4, spaceAfter=6)
    )

    # ---------- Part 1 ----------
    story.append(Paragraph("Part 1 — Secure Feature Design", styles["section"]))
    story.append(
        Paragraph(
            "I looked through OWASP Juice Shop with a focus on registration and login. "
            "Three issues stood out, and each one shaped how I would design a safer signup flow.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>1. SQL injection on login.</b> If the login query is built by joining "
            "strings, a crafted email can change the query and skip password checks. "
            "I would only look up users with parameterized queries (or an ORM), and I "
            "would validate the email format first. That way user input stays data, not code.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>2. Cross-site scripting (XSS).</b> Fields like search or product reviews "
            "can store or reflect HTML and JavaScript. If that content is rendered raw, "
            "it can run in another user’s browser. I would encode output, prefer "
            "<font face='Courier'>textContent</font> over "
            "<font face='Courier'>innerHTML</font>, reject angle brackets on input, "
            "and add a Content-Security-Policy header so scripts cannot run inline.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>3. Authentication bypass / weak sessions.</b> Weak or predictable tokens "
            "make it easier to impersonate another account. I would use signed tokens "
            "with short expiry, check authorization on the server for every sensitive "
            "route, rate-limit login attempts, and always return a generic "
            "“Invalid email or password” message so attackers cannot tell which field was wrong.",
            styles["body"],
        )
    )
    story.append(Paragraph("Secure password handling", styles["subsection"]))
    story.append(
        Paragraph(
            "Passwords should never be stored in plaintext. On registration I hash once "
            "with bcrypt (cost factor 12). On login I compare with "
            "<font face='Courier'>bcrypt.compare</font>. Even if the database leaks, "
            "attackers only get slow-to-crack hashes.",
            styles["body"],
        )
    )
    story.append(
        Preformatted(
            "const passwordHash = await bcrypt.hash(password, 12);\n"
            "// store passwordHash only — never the plaintext password\n\n"
            "const ok = await bcrypt.compare(submittedPassword, user.passwordHash);\n"
            "if (!ok) return res.status(401).json({ error: 'Invalid email or password.' });",
            styles["code"],
        )
    )

    # ---------- Part 2 ----------
    story.append(Paragraph("Part 2 — Front-End Login Form", styles["section"]))
    story.append(
        Paragraph(
            "I built a simple Juice Shop–style login page in HTML, CSS, and JavaScript, "
            "with a small Express server behind it. The form has email and password fields, "
            "a submit button, and an on-page status message.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Client-side validation</b> (<font face='Courier'>public/app.js</font>) "
            "runs before any network call. Empty submissions are blocked. The email must "
            "contain <font face='Courier'>@</font>. The password must be at least 8 characters. "
            "If a check fails, the field is highlighted and a short error is shown.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Server-side validation</b> (<font face='Courier'>server.js</font>) repeats "
            "the checks more strictly: email shape, password length, and rejection of "
            "unsafe characters. Users are stored in memory and looked up by email — there "
            "is no string-built SQL. Passwords are verified with bcryptjs. Responses use "
            "safe text rendering (<font face='Courier'>textContent</font>), and login is "
            "rate-limited.",
            styles["body"],
        )
    )
    story.append(Paragraph("How to run", styles["subsection"]))
    story.append(
        Preformatted(
            "git clone https://github.com/deeps45/juice-guard.git\n"
            "cd juice-guard\n"
            "npm install\n"
            "npm start\n"
            "# open http://127.0.0.1:3847\n"
            "# demo login: demo@juice.shop / JuiceShop1!",
            styles["code"],
        )
    )
    story.append(
        Paragraph(
            f"<b>Public GitHub repository:</b> <link href='{GITHUB_URL}'>"
            f"<font color='#0B57D0'><u>{GITHUB_URL}</u></font></link><br/>"
            "The README explains what the project does and how to run it.",
            styles["body"],
        )
    )
    story.append(
        figure_pair(
            SHOTS / "01-login-form.png",
            "Figure 1. Login form (email + password).",
            SHOTS / "02-successful-login.png",
            "Figure 2. Successful login after both checks.",
            styles,
        )
    )
    story.append(Spacer(1, 0.04 * inch))
    story.append(
        figure_pair(
            SHOTS / "03-empty-validation.png",
            "Figure 3. Empty fields blocked on the client.",
            SHOTS / "04-short-password.png",
            "Figure 4. Password must be at least 8 characters.",
            styles,
        )
    )

    # ---------- Part 3 ----------
    story.append(PageBreak())
    story.append(Paragraph("Part 3 — Trying to Break My Own Form", styles["section"]))
    story.append(
        Paragraph(
            "After building the form, I tried the same kinds of attacks Juice Shop is known "
            "for — XSS and SQL injection — against my own login page.",
            styles["body"],
        )
    )

    story.append(Paragraph("Attempt 1: Cross-site scripting (XSS)", styles["subsection"]))
    story.append(
        Paragraph(
            "<b>Steps.</b> I opened the login page, entered "
            "<font face='Courier'>xss@test.com</font> as the email, and put "
            "<font face='Courier'>&lt;script&gt;alert(1)&lt;/script&gt;</font> in the "
            "password field. Then I clicked Log in and watched for a JavaScript alert "
            "or any script execution in the page.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Result.</b> The attack did not work. No alert appeared. The server rejected "
            "the password because it contained unsafe characters "
            "(<font face='Courier'>&lt;</font> / <font face='Courier'>&gt;</font>). "
            "The UI also writes status messages with "
            "<font face='Courier'>textContent</font>, so even a reflected string would "
            "not be treated as HTML.",
            styles["body"],
        )
    )
    story.append(
        figure(
            SHOTS / "05-xss-blocked.png",
            "Figure 5. XSS attempt blocked — no script ran in the browser.",
            styles,
            max_h=2.7 * inch,
        )
    )

    story.append(Paragraph("Attempt 2: SQL injection", styles["subsection"]))
    story.append(
        Paragraph(
            "<b>Steps.</b> I reloaded the page and entered "
            "<font face='Courier'>admin@test.com' OR '1'='1</font> as the email and "
            "<font face='Courier'>password1</font> as the password, then submitted the form. "
            "I checked whether login succeeded or any credentials were exposed.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Result.</b> The attack did not work. The app treated the email as invalid "
            "and never built a SQL string from user input (accounts live in an in-memory "
            "map keyed by email). There was no authentication bypass and no data leak.",
            styles["body"],
        )
    )
    story.append(
        figure(
            SHOTS / "06-sqli-blocked.png",
            "Figure 6. SQL injection–style email rejected by validation.",
            styles,
            max_h=2.7 * inch,
        )
    )

    story.append(Paragraph("One fix I applied", styles["subsection"]))
    story.append(
        Paragraph(
            "Even though both attacks failed, I added a Content-Security-Policy header "
            "(<font face='Courier'>default-src 'self'; script-src 'self'</font>, with "
            "limited exceptions for fonts). If someone later uses "
            "<font face='Courier'>innerHTML</font> by mistake, the browser still blocks "
            "inline script. That is useful defense in depth on top of input checks and "
            "bcrypt hashing.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Overall takeaway: client checks help with usability, but server validation, "
            "safe DOM updates, and never concatenating SQL are what actually stop XSS and "
            "injection. Not being able to break my own form was a good sign.",
            styles["body"],
        )
    )

    story.append(Spacer(1, 0.15 * inch))
    story.append(
        HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=4, spaceAfter=8)
    )
    story.append(
        Paragraph(
            f"End of submission · Source and README: "
            f"<link href='{GITHUB_URL}'><font color='#0B57D0'><u>{GITHUB_URL}</u></font></link>",
            styles["caption"],
        )
    )

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
