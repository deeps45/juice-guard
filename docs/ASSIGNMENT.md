# HW 2B Write-ups (~100 words each)

**GitHub:** https://github.com/deeps45/juice-guard  
**PDF:** [`submission.pdf`](submission.pdf)

## Part 1 — Learnings

What surprised me most is how “normal” the Juice Shop login screen looks while still being easy to abuse if the backend concatenates SQL. Looking up Login Admin and DOM XSS on the Score Board made the risks concrete instead of abstract. I also realized authentication bugs are not only about passwords—token handling matters just as much. My takeaway for a secure registration/login design is simple: treat every field as hostile, keep queries parameterized, never render raw HTML from users, and hash passwords with bcrypt before they touch storage. Those few habits would have blocked most of what I saw in the challenges.

## Part 2 — Learnings

Building the form made the Juice Shop lessons feel practical. Client-side checks are nice for users—they catch empty fields quickly—but they are easy to skip, so I treated the server as the real gate. Adding CSRF forced me to think about forged requests, not only bad passwords. Hashing with bcrypt was straightforward once I stopped thinking of “encryption” and started thinking of one-way hashing. Overall I learned that a “basic” login page still needs several layers: validation, safe rendering, password hashing, and request authenticity. The public repo and README document how to run everything locally.

## Part 3 — Learnings

The biggest lesson was that “the attack failed” is not the whole story. My client validation let a script-shaped password through and still called the API. That is exactly how people get hurt when they assume the browser is enough. Calling the endpoint with fetch() made the same point louder. CSRF testing showed why a random token belongs on state-changing requests. I fixed the gaps by keeping strict server checks, requiring CSRF tokens, using textContent, and setting a CSP. If I build another auth form, I will design the server path first and treat client checks as UX only.
