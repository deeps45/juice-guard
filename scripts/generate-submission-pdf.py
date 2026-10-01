#!/usr/bin/env python3
"""Human-toned HW 2B submission PDF — prose write-ups (~100 words each part)."""

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
GITHUB = "https://github.com/deeps45/juice-guard"

INK = colors.HexColor("#222222")
MUTED = colors.HexColor("#444444")
RULE = colors.HexColor("#999999")


def styles():
    base = getSampleStyleSheet()
    return {
        "course": ParagraphStyle(
            "course",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=12,
            leading=15,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=18,
            leading=22,
            textColor=INK,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=2,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=11,
            leading=14,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "meta": ParagraphStyle(
            "meta",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=14,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=1,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Times-Bold",
            fontSize=13,
            leading=16,
            textColor=INK,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=11.5,
            leading=14,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=11,
            leading=15,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            firstLineIndent=14,
        ),
        "body0": ParagraphStyle(
            "body0",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=11,
            leading=15,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            firstLineIndent=0,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=9.5,
            leading=12,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=10,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=9,
            leading=12,
            textColor=INK,
            leftIndent=10,
            spaceBefore=2,
            spaceAfter=8,
        ),
        "link": ParagraphStyle(
            "link",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=11,
            leading=15,
            textColor=INK,
            spaceAfter=8,
        ),
    }


def fig(path, caption, s, max_w=6.2 * inch, max_h=2.4 * inch):
    pic = Image(str(path))
    scale = min(max_w / pic.imageWidth, max_h / pic.imageHeight)
    pic.drawWidth = pic.imageWidth * scale
    pic.drawHeight = pic.imageHeight * scale
    return KeepTogether([pic, Paragraph(caption, s["caption"])])


def pair(a, ca, b, cb, s, max_h=2.1 * inch):
    max_w = 3.0 * inch

    def one(p, cap):
        pic = Image(str(p))
        scale = min(max_w / pic.imageWidth, max_h / pic.imageHeight)
        pic.drawWidth = pic.imageWidth * scale
        pic.drawHeight = pic.imageHeight * scale
        return pic, Paragraph(cap, s["caption"])

    left_img, left_cap = one(a, ca)
    right_img, right_cap = one(b, cb)
    table = Table(
        [[left_img, right_img], [left_cap, right_cap]],
        colWidths=[3.2 * inch, 3.2 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="HW 2B OWASP Juice Shop",
        author="Siva Sai Deepank Manoj",
    )

    story = []

    # Title / course header
    story.append(Paragraph("Texas A&amp;M University", s["course"]))
    story.append(Paragraph("CSCE 703 — Cybersecurity", s["course"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Homework 2B", s["title"]))
    story.append(Paragraph("OWASP Juice Shop: Secure Design, Login Form, and Exploitation", s["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=INK, spaceBefore=2, spaceAfter=8))

    info = [
        [Paragraph("<b>Name</b>", s["meta"]), Paragraph("Siva Sai Deepank Manoj", s["meta"])],
        [Paragraph("<b>UIN</b>", s["meta"]), Paragraph("437005609", s["meta"])],
        [Paragraph("<b>Email</b>", s["meta"]), Paragraph("deeps45@tamu.edu", s["meta"])],
        [Paragraph("<b>Course</b>", s["meta"]), Paragraph("CSCE 703", s["meta"])],
        [
            Paragraph("<b>GitHub</b>", s["meta"]),
            Paragraph(f"<link href='{GITHUB}'><u>{GITHUB}</u></link>", s["meta"]),
        ],
    ]
    info_table = Table(info, colWidths=[0.9 * inch, 5.4 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(info_table)
    story.append(HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=8, spaceAfter=10))

    # ===================== PART 1 =====================
    story.append(Paragraph("Part 1 — Secure Feature Design", s["h1"]))
    story.append(
        Paragraph(
            "I explored the live Juice Shop at preview.owasp-juice.shop and used what I found "
            "to design a safer registration/login flow. Three challenges stood out. "
            "<b>Login Admin</b> (Injection) shows how a crafted email can break a string-built "
            "SQL login query. Mitigation: parameterized queries or an ORM, plus email "
            "validation before any database call—so input stays data, not query code. "
            "<b>DOM XSS</b> shows how HTML/JavaScript can run in another user’s browser. "
            "Mitigation: encode output, prefer textContent over innerHTML, and add a "
            "Content-Security-Policy. <b>Forged Signed JWT</b> / weak authentication shows "
            "token handling can be abused for account takeover. Mitigation: verify JWT "
            "signatures with a strong secret, short expiry, server-side authorization, and "
            "rate-limited login. For registration, passwords must be stored with bcrypt, "
            "never plaintext.",
            s["body0"],
        )
    )
    story.append(Paragraph("Learnings (~100 words)", s["h2"]))
    story.append(
        Paragraph(
            "What surprised me most is how “normal” the Juice Shop login screen looks while "
            "still being easy to abuse if the backend concatenates SQL. Looking up Login Admin "
            "and DOM XSS on the Score Board made the risks concrete instead of abstract. I also "
            "realized authentication bugs are not only about passwords—token handling matters "
            "just as much. My takeaway for a secure registration/login design is simple: treat "
            "every field as hostile, keep queries parameterized, never render raw HTML from "
            "users, and hash passwords with bcrypt before they touch storage. Those few habits "
            "would have blocked most of what I saw in the challenges.",
            s["body0"],
        )
    )
    story.append(Paragraph("Password hashing example", s["h2"]))
    story.append(
        Preformatted(
            "const hash = await bcrypt.hash(password, 12);\n"
            "const ok = await bcrypt.compare(submittedPassword, user.passwordHash);",
            s["code"],
        )
    )
    story.append(
        pair(
            SHOTS / "js-02-login.png",
            "Figure 1. Juice Shop login page I inspected.",
            SHOTS / "js-03b-login-admin.png",
            "Figure 2. Score Board — Login Admin (Injection).",
            s,
            max_h=2.0 * inch,
        )
    )
    story.append(
        fig(
            SHOTS / "js-03c-dom-xss.png",
            "Figure 3. Score Board — DOM XSS (JWT / broken-auth challenges were listed nearby as well).",
            s,
            max_h=2.0 * inch,
        )
    )

    # ===================== PART 2 =====================
    story.append(Paragraph("Part 2 — Front-End Login Form", s["h1"]))
    story.append(
        Paragraph(
            "I built a simple login page in HTML, CSS, and JavaScript with a small Express "
            "server behind it. The form has email and password fields. On the client, "
            "app.js blocks empty submissions, checks that the email contains “@”, and "
            "requires the password to be at least eight characters. On the server, those "
            "checks run again more strictly, passwords are verified with bcrypt, and login "
            "also requires a CSRF token from /api/csrf. Status messages use textContent so "
            "reflected text cannot turn into HTML. I kept demo credentials in the README "
            "only, not on the page.",
            s["body0"],
        )
    )
    story.append(Paragraph("Learnings (~100 words)", s["h2"]))
    story.append(
        Paragraph(
            "Building the form made the Juice Shop lessons feel practical. Client-side checks "
            "are nice for users—they catch empty fields quickly—but they are easy to skip, so "
            "I treated the server as the real gate. Adding CSRF forced me to think about "
            "forged requests, not only bad passwords. Hashing with bcrypt was straightforward "
            "once I stopped thinking of “encryption” and started thinking of one-way hashing. "
            "Overall I learned that a “basic” login page still needs several layers: validation, "
            "safe rendering, password hashing, and request authenticity. The public repo and "
            "README document how to run everything locally.",
            s["body0"],
        )
    )
    story.append(
        Paragraph(
            f"<b>Public GitHub repository:</b> "
            f"<link href='{GITHUB}'><u>{GITHUB}</u></link><br/>"
            "Run: <font face='Courier'>npm install && npm start</font> → "
            "http://127.0.0.1:3847<br/>"
            "Demo login (README only): demo@juice.shop / JuiceShop1!",
            s["link"],
        )
    )
    story.append(
        pair(
            SHOTS / "01-login-form.png",
            "Figure 4. My hardened login form.",
            SHOTS / "03-empty-validation.png",
            "Figure 5. Empty fields blocked on the client.",
            s,
            max_h=2.0 * inch,
        )
    )
    story.append(
        pair(
            SHOTS / "02-successful-login.png",
            "Figure 6. Successful login after validation + CSRF.",
            SHOTS / "04-short-password.png",
            "Figure 7. Short password rejected.",
            s,
            max_h=2.0 * inch,
        )
    )

    # ===================== PART 3 =====================
    story.append(Paragraph("Part 3 — Breaking My Own Form", s["h1"]))
    story.append(
        Paragraph(
            "I tried to break the same form that is in my GitHub repo. First I entered "
            "xss@test.com and the password &lt;script&gt;alert(1)&lt;/script&gt;. The "
            "client actually allowed the submit (it only checks “@” and length), and the "
            "browser sent POST /api/login—but the server rejected unsafe characters and no "
            "script ran. Next I bypassed the UI with fetch() and got the same server error. "
            "A login POST without an X-CSRF-Token returned 403. I also tried "
            "admin@test.com' OR '1'='1; that was blocked as an invalid email. So classic "
            "XSS/SQLi did not fully land, but I did expose a real weakness: the client is too "
            "trusting on its own.",
            s["body0"],
        )
    )
    story.append(Paragraph("Learnings (~100 words)", s["h2"]))
    story.append(
        Paragraph(
            "The biggest lesson was that “the attack failed” is not the whole story. My client "
            "validation let a script-shaped password through and still called the API. That is "
            "exactly how people get hurt when they assume the browser is enough. Calling the "
            "endpoint with fetch() made the same point louder. CSRF testing showed why a random "
            "token belongs on state-changing requests. I fixed the gaps by keeping strict server "
            "checks, requiring CSRF tokens, using textContent, and setting a CSP. If I build "
            "another auth form, I will design the server path first and treat client checks as "
            "UX only.",
            s["body0"],
        )
    )
    story.append(Paragraph("Steps and results", s["h2"]))
    story.append(
        Paragraph(
            "<b>XSS attempt:</b> open / → email xss@test.com → password "
            "&lt;script&gt;alert(1)&lt;/script&gt; → Log in. "
            "<i>Result:</i> client submitted the request; server returned an unsafe-character "
            "error; no alert.<br/><br/>"
            "<b>Client bypass:</b> fetch('/api/login') with the same password and a CSRF token. "
            "<i>Result:</i> HTTP 400 from the server.<br/><br/>"
            "<b>CSRF check:</b> POST valid credentials with no X-CSRF-Token. "
            "<i>Result:</i> HTTP 403.<br/><br/>"
            "<b>SQLi probe:</b> email admin@test.com' OR '1'='1. "
            "<i>Result:</i> rejected; no auth bypass.",
            s["body0"],
        )
    )
    story.append(
        pair(
            SHOTS / "05-xss-client-passed-server-blocked.png",
            "Figure 8. XSS payload passed the client, blocked by the server.",
            SHOTS / "06-sqli-blocked.png",
            "Figure 9. SQL injection–style email rejected.",
            s,
            max_h=2.05 * inch,
        )
    )
    story.append(
        fig(
            SHOTS / "07-api-weakness-evidence.png",
            "Figure 10. API results: CSRF forgery blocked (403); fetch bypass still stopped by server validation.",
            s,
            max_h=2.2 * inch,
        )
    )
    story.append(
        Paragraph(
            "One fix I applied on top of server validation was requiring CSRF tokens and a "
            "Content-Security-Policy, so forged requests and inline scripts are harder to abuse "
            "even if a UI bug shows up later.",
            s["body0"],
        )
    )

    # No footer callback, no "submission complete" line
    doc.build(story)
    print(f"Wrote {OUT}")

    # Quick word-count helper for the three learning sections
    learnings = [
        "What surprised me most is how “normal” the Juice Shop login screen looks while "
        "still being easy to abuse if the backend concatenates SQL. Looking up Login Admin "
        "and DOM XSS on the Score Board made the risks concrete instead of abstract. I also "
        "realized authentication bugs are not only about passwords—token handling matters "
        "just as much. My takeaway for a secure registration/login design is simple: treat "
        "every field as hostile, keep queries parameterized, never render raw HTML from "
        "users, and hash passwords with bcrypt before they touch storage. Those few habits "
        "would have blocked most of what I saw in the challenges.",
        "Building the form made the Juice Shop lessons feel practical. Client-side checks "
        "are nice for users—they catch empty fields quickly—but they are easy to skip, so "
        "I treated the server as the real gate. Adding CSRF forced me to think about "
        "forged requests, not only bad passwords. Hashing with bcrypt was straightforward "
        "once I stopped thinking of “encryption” and started thinking of one-way hashing. "
        "Overall I learned that a “basic” login page still needs several layers: validation, "
        "safe rendering, password hashing, and request authenticity. The public repo and "
        "README document how to run everything locally.",
        "The biggest lesson was that “the attack failed” is not the whole story. My client "
        "validation let a script-shaped password through and still called the API. That is "
        "exactly how people get hurt when they assume the browser is enough. Calling the "
        "endpoint with fetch() made the same point louder. CSRF testing showed why a random "
        "token belongs on state-changing requests. I fixed the gaps by keeping strict server "
        "checks, requiring CSRF tokens, using textContent, and setting a CSP. If I build "
        "another auth form, I will design the server path first and treat client checks as "
        "UX only.",
    ]
    for i, text in enumerate(learnings, 1):
        print(f"Part {i} learnings words: {len(text.split())}")


if __name__ == "__main__":
    build()
