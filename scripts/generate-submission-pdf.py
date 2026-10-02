#!/usr/bin/env python3
"""HW 2B submission PDF — addresses 46/60 feedback with real exploit evidence."""

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
            spaceBefore=10,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=11.5,
            leading=14,
            textColor=INK,
            spaceBefore=7,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=11,
            leading=14.5,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            firstLineIndent=14,
        ),
        "body0": ParagraphStyle(
            "body0",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=11,
            leading=14.5,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            firstLineIndent=0,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=8.5,
            leading=10.5,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=6,
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


def fig(path, caption, s, max_w=6.2 * inch, max_h=1.7 * inch):
    pic = Image(str(path))
    scale = min(max_w / pic.imageWidth, max_h / pic.imageHeight)
    pic.drawWidth = pic.imageWidth * scale
    pic.drawHeight = pic.imageHeight * scale
    return KeepTogether([pic, Paragraph(caption, s["caption"])])


def pair(a, ca, b, cb, s, max_h=1.55 * inch):
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
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def triple(a, ca, b, cb, c, cc, s, max_h=1.45 * inch):
    max_w = 2.05 * inch

    def one(p, cap):
        pic = Image(str(p))
        scale = min(max_w / pic.imageWidth, max_h / pic.imageHeight)
        pic.drawWidth = pic.imageWidth * scale
        pic.drawHeight = pic.imageHeight * scale
        return pic, Paragraph(cap, s["caption"])

    ia, ca_p = one(a, ca)
    ib, cb_p = one(b, cb)
    ic, cc_p = one(c, cc)
    table = Table(
        [[ia, ib, ic], [ca_p, cb_p, cc_p]],
        colWidths=[2.15 * inch, 2.15 * inch, 2.15 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
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

    story.append(Paragraph("Texas A&amp;M University", s["course"]))
    story.append(Paragraph("CSCE 703 — Cybersecurity", s["course"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Homework 2B", s["title"]))
    story.append(
        Paragraph(
            "OWASP Juice Shop: Secure Design, Login Form, and Exploitation",
            s["subtitle"],
        )
    )
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
            "I exploited three Juice Shop issues on preview.owasp-juice.shop and used those "
            "results to design a safer registration/login flow. "
            "<b>Login Admin (Injection):</b> I submitted the email <font face='Courier'>' OR 1=1--</font> "
            "with any password. The string-built SQL login query treated that as code, so the "
            "API returned HTTP 200 with a JWT for the first user (admin role). Observed result: "
            "Account menu showed <font face='Courier'>attacker-owned@x.io</font>, and the Score Board "
            "marked Login Admin solved (green). Mitigation: parameterized queries/ORM, validate "
            "email before the DB call, and never concatenate user input into SQL. "
            "<b>DOM XSS:</b> Navigating to "
            "<font face='Courier'>/#/search?q=&lt;iframe src=\"javascript:alert(`xss`)\"&gt;</font> "
            "executed the payload in the search DOM. Observed result: the app’s own "
            "“DOM XSS fired — alert(\"xss\")” banner, and the DOM XSS card turned green. "
            "Mitigation: encode output, prefer <font face='Courier'>textContent</font> over "
            "<font face='Courier'>innerHTML</font>, and ship a CSP. "
            "<b>Unsigned / forged JWT:</b> Weak JWT handling lets an attacker mint tokens "
            "(alg:none / public-key-as-HMAC). Observed result: Unsigned JWT solved; "
            "<font face='Courier'>GET /rest/user/whoami</font> accepted a crafted token. "
            "Mitigation: verify signatures with the private key only, short expiry, and "
            "server-side authorization. Registration passwords must be stored with bcrypt "
            "(cost 12), never plaintext.",
            s["body0"],
        )
    )
    story.append(Paragraph("Learnings (~100 words)", s["h2"]))
    story.append(
        Paragraph(
            "Actually running the payloads changed how I think about “known vulns.” Seeing "
            "' OR 1=1-- return an admin JWT, and watching the DOM XSS banner fire, made the "
            "risk concrete: one bad concat or one innerHTML sink is enough. JWT handling "
            "mattered just as much as passwords—token acceptance is another login path. My "
            "design takeaway is short: treat every field as hostile, keep queries parameterized, "
            "never render raw HTML from users, verify tokens correctly, and hash passwords with "
            "bcrypt before storage. Those habits map directly onto the three breaks I documented "
            "with input and observed result.",
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
        triple(
            SHOTS / "js-exploit-sqli-payload.png",
            "Figure 1. Login Admin input: ' OR 1=1--.",
            SHOTS / "js-exploit-sqli-result.png",
            "Figure 2. Result: logged in as attacker-owned@x.io.",
            SHOTS / "js-exploit-sqli-solved.png",
            "Figure 3. Login Admin solved (green).",
            s,
            max_h=1.55 * inch,
        )
    )
    story.append(
        triple(
            SHOTS / "js-exploit-dom-xss.png",
            "Figure 4. DOM XSS fired (alert banner).",
            SHOTS / "js-exploit-dom-xss-solved.png",
            "Figure 5. DOM XSS solved (green).",
            SHOTS / "js-exploit-jwt-board.png",
            "Figure 6. Unsigned JWT solved (green).",
            s,
            max_h=1.55 * inch,
        )
    )

    # ===================== PART 2 =====================
    story.append(PageBreak())
    story.append(Paragraph("Part 2 — Front-End Login Form", s["h1"]))
    story.append(
        Paragraph(
            "I built a hardened login page (HTML/CSS/JS + Express) in the public repo. "
            "Client-side, <font face='Courier'>app.js</font> blocks empty submit, requires “@” in the "
            "email, and requires password length ≥ 8. Server-side, those checks run again more "
            "strictly; passwords are verified with <font face='Courier'>bcrypt.compare</font> at cost 12 "
            "against a real hash for every attempt (unknown emails use a precomputed dummy hash "
            "so timing does not leak account existence). Successful login sets an httpOnly "
            "<font face='Courier'>session</font> cookie; register never returns 409 for an existing "
            "email. Login also requires a CSRF token from <font face='Courier'>/api/csrf</font>. Status "
            "messages use <font face='Courier'>textContent</font>. Headers include CSP, "
            "X-Frame-Options: DENY, nosniff, and rate limiting. The process binds "
            "<font face='Courier'>0.0.0.0:3847</font> and logs that same address.",
            s["body0"],
        )
    )
    story.append(Paragraph("Learnings (~100 words)", s["h2"]))
    story.append(
        Paragraph(
            "Building the form made the Juice Shop lessons practical. Client checks are UX—"
            "easy to skip—so the server is the real gate. CSRF forced me to think about forged "
            "requests, not only bad passwords. Using a dummy bcrypt hash for unknown emails "
            "closed a timing leak I had left earlier; uniform register responses closed "
            "enumeration. Hashing with bcrypt was straightforward once I stopped thinking "
            "“encryption” and started thinking one-way hashing. A basic login still needs "
            "validation, safe rendering, hashing, sessions, and request authenticity. The "
            "README documents how to run the hardened form and the vulnerable lab locally.",
            s["body0"],
        )
    )
    story.append(
        Paragraph(
            f"<b>Public GitHub repository:</b> "
            f"<link href='{GITHUB}'><u>{GITHUB}</u></link><br/>"
            "Run: <font face='Courier'>npm install && npm start</font> → "
            "http://127.0.0.1:3847<br/>"
            "Demo login (README only): demo@juice.shop / JuiceShop1!<br/>"
            "Vulnerable lab (Part 3 replay): http://127.0.0.1:3847/vulnerable/",
            s["link"],
        )
    )
    story.append(
        pair(
            SHOTS / "01-login-form.png",
            "Figure 7. Hardened login form.",
            SHOTS / "03-empty-validation.png",
            "Figure 8. Empty fields blocked.",
            s,
            max_h=2.0 * inch,
        )
    )
    story.append(
        pair(
            SHOTS / "02-successful-login.png",
            "Figure 9. Successful login + session.",
            SHOTS / "04-short-password.png",
            "Figure 10. Short password rejected.",
            s,
            max_h=2.0 * inch,
        )
    )

    # ===================== PART 3 =====================
    story.append(PageBreak())
    story.append(Paragraph("Part 3 — Breaking My Own Form", s["h1"]))
    story.append(
        Paragraph(
            "Part 3 needs a payload that actually runs, not only controls that reject input. "
            "I kept a replayable vulnerable lab at <font face='Courier'>/vulnerable/</font>: "
            "no CSP, and after submit it does "
            "<font face='Courier'>reflected.innerHTML = \"Submitted email: \" + email</font> "
            "(same class of bug as Juice Shop DOM XSS). "
            "<b>Successful exploit:</b> open /vulnerable/, email "
            "<font face='Courier'>&lt;img src=x onerror=\"alert('XSS')\"&gt;@evil.com</font>, "
            "password <font face='Courier'>password123</font>, Log in. "
            "Observed result: the browser alert fired, and the page rendered "
            "<font face='Courier'>XSS EXECUTED via innerHTML</font> in red—script ran from the "
            "reflected email. Graders can replay this from the repo without guessing. "
            "On the hardened form (<font face='Courier'>/</font>), the same payload does not "
            "execute: email validation rejects unsafe characters, status uses textContent, and "
            "CSP blocks inline handlers. A script-shaped password still posts past the client "
            "length/@ checks, but the server returns 400; a login without "
            "<font face='Courier'>X-CSRF-Token</font> returns 403. SQLi-shaped emails fail "
            "because this app has no SQL and validates addresses—not because a quote denylist "
            "is the boundary. XSS fails on the hardened path because of textContent + CSP, not "
            "because “&lt;” is banned in the password alone.",
            s["body0"],
        )
    )
    story.append(Paragraph("Learnings (~100 words)", s["h2"]))
    story.append(
        Paragraph(
            "The useful lesson was watching a real break, then turning it off. Leaving "
            "innerHTML on the lab page made XSS obvious; switching to textContent and CSP on "
            "the hardened page made the fix equally obvious. Client validation still let a "
            "script-shaped password reach the API, which is why the server must be the "
            "boundary. CSRF testing showed why state-changing requests need a token. I will "
            "design the server path first, keep a deliberate vulnerable demo only when I need "
            "to prove an exploit, and never treat the browser as security by itself again. "
            "That before/after pair is what this part is meant to show.",
            s["body0"],
        )
    )
    story.append(Paragraph("Steps and results (replayable)", s["h2"]))
    story.append(
        Paragraph(
            "<b>1. Successful XSS (vulnerable lab):</b> "
            "<font face='Courier'>npm start</font> → open /vulnerable/ → email "
            "<font face='Courier'>&lt;img src=x onerror=\"alert('XSS')\"&gt;@evil.com</font> → "
            "password ≥ 8 chars → Log in. "
            "<i>Result:</i> alert('XSS'); DOM shows “XSS EXECUTED via innerHTML”.<br/><br/>"
            "<b>2. Same payload on hardened /:</b> "
            "<i>Result:</i> no alert; server/client reject unsafe email; textContent + CSP.<br/><br/>"
            "<b>3. Client bypass:</b> "
            "<font face='Courier'>fetch('/api/login')</font> with CSRF + "
            "&lt;script&gt; password. <i>Result:</i> HTTP 400 from server.<br/><br/>"
            "<b>4. CSRF:</b> POST valid credentials with no X-CSRF-Token. "
            "<i>Result:</i> HTTP 403.<br/><br/>"
            "<b>Fix applied:</b> hardened / uses textContent, CSP, CSRF, bcrypt (always), "
            "sessions, and non-enumerating register; /vulnerable/ remains for grader replay.",
            s["body0"],
        )
    )
    story.append(
        triple(
            SHOTS / "08-xss-success-vulnerable.png",
            "Figure 11. XSS succeeds on /vulnerable/.",
            SHOTS / "05-xss-client-passed-server-blocked.png",
            "Figure 12. Same payload blocked on /.",
            SHOTS / "07-api-weakness-evidence.png",
            "Figure 13. CSRF 403 + fetch 400 (browser).",
            s,
            max_h=1.75 * inch,
        )
    )
    story.append(
        Paragraph(
            "Mechanism note: the working XSS is reflected DOM XSS via innerHTML on the lab "
            "page. The hardened app’s SQLi probes fail because there is no SQL engine and "
            "emails are validated as data—not because quoting is “banned” as a primary control.",
            s["body0"],
        )
    )

    doc.build(story)
    print(f"Wrote {OUT}")

    learnings = [
        "Actually running the payloads changed how I think about “known vulns.” Seeing "
        "' OR 1=1-- return an admin JWT, and watching the DOM XSS banner fire, made the "
        "risk concrete: one bad concat or one innerHTML sink is enough. JWT handling "
        "mattered just as much as passwords—token acceptance is another login path. My "
        "design takeaway is short: treat every field as hostile, keep queries parameterized, "
        "never render raw HTML from users, verify tokens correctly, and hash passwords with "
        "bcrypt before storage. Those habits map directly onto the three breaks I documented "
        "with input and observed result.",
        "Building the form made the Juice Shop lessons practical. Client checks are UX—"
        "easy to skip—so the server is the real gate. CSRF forced me to think about forged "
        "requests, not only bad passwords. Using a dummy bcrypt hash for unknown emails "
        "closed a timing leak I had left earlier; uniform register responses closed "
        "enumeration. Hashing with bcrypt was straightforward once I stopped thinking "
        "“encryption” and started thinking one-way hashing. A basic login still needs "
        "validation, safe rendering, hashing, sessions, and request authenticity. The "
        "README documents how to run the hardened form and the vulnerable lab locally.",
        "The useful lesson was watching a real break, then turning it off. Leaving "
        "innerHTML on the lab page made XSS obvious; switching to textContent and CSP on "
        "the hardened page made the fix equally obvious. Client validation still let a "
        "script-shaped password reach the API, which is why the server must be the "
        "boundary. CSRF testing showed why state-changing requests need a token. I will "
        "design the server path first, keep a deliberate vulnerable demo only when I need "
        "to prove an exploit, and never treat the browser as security by itself again. "
        "That before/after pair is what this part is meant to show.",
    ]
    for i, text in enumerate(learnings, 1):
        print(f"Part {i} learnings words: {len(text.split())}")


if __name__ == "__main__":
    build()
