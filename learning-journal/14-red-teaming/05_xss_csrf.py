"""
XSS & CSRF — two attacks that abuse user trust

XSS (Cross-Site Scripting):
  Attacker injects JavaScript into a page that other users visit.
  The script runs in THEIR browser, with THEIR session — not the attacker's.

  Stored XSS:   payload saved in DB, fires for everyone who views the page
  Reflected XSS: payload in URL, fires when victim clicks a crafted link
  DOM XSS:       payload processed by client-side JS (no server involved)

CSRF (Cross-Site Request Forgery):
  Victim's browser automatically sends cookies with every request.
  Attacker's page makes the victim's browser send a request to bank.com.
  Bank.com sees valid session cookie → thinks it's a real user action.

DIFFERENCE:
  XSS  = attacker runs code IN the victim's browser (reads their data)
  CSRF = attacker tricks the victim's browser into sending requests AS them
"""

import http.server, threading, urllib.request, urllib.parse, html

comments = []   # shared in-memory store

# ── VULNERABLE server ─────────────────────────────────────────────────────────
class VulnerableHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/post?"):
            params = urllib.parse.parse_qs(self.path.split("?",1)[1])
            comment = params.get("comment", [""])[0]
            comments.append(comment)           # ← stored as-is, no sanitization
        # render all comments raw into HTML — any <script> tag will execute
        body = "<html><body><h2>Comments</h2>"
        for c in comments:
            body += f"<p>{c}</p>"              # ← raw injection, not escaped!
        body += "</body></html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(body.encode())
    def log_message(self, *a): pass

# ── SECURE server: escapes all output ────────────────────────────────────────
safe_comments = []

class SecureHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/post?"):
            params  = urllib.parse.parse_qs(self.path.split("?",1)[1])
            comment = params.get("comment", [""])[0]
            safe_comments.append(comment)       # stored raw
        body = "<html><head>"
        # Content-Security-Policy: second line of defense
        body += "</head><body><h2>Comments</h2>"
        for c in safe_comments:
            safe = html.escape(c)              # ← <script> → &lt;script&gt;
            body += f"<p>{safe}</p>"
        body += "</body></html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Security-Policy", "default-src 'self'")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.end_headers()
        self.wfile.write(body.encode())
    def log_message(self, *a): pass

def start(handler, port):
    s = http.server.HTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

vuln   = start(VulnerableHandler, 9301)
secure = start(SecureHandler,     9302)

def post(port, comment):
    encoded = urllib.parse.quote(comment)
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/post?comment={encoded}") as r:
        return r.read().decode()

print("=== ATTACK: stored XSS — injecting a script tag ===")
xss_payload = '<script>alert("XSS: cookie=" + document.cookie)</script>'
result = post(9301, xss_payload)
if "<script>" in result:
    print(f"  Vulnerable: script tag rendered raw in HTML!")
    print(f"  Browser would execute: alert('XSS: cookie=session=abc123...')")
    print(f"  In a real attack: sends victim's session cookie to attacker's server\n")

print("=== SECURE server: same payload, escaped ===")
result = post(9302, xss_payload)
if "&lt;script&gt;" in result:
    print(f"  Secure: <script> → &lt;script&gt; (rendered as text, not executed)\n")

print("""
=== CSRF — how it works (conceptual) ===

1. Alice is logged into bank.com (session cookie set)
2. Alice visits evil.com (attacker's page)
3. evil.com has hidden HTML:
     <form action="https://bank.com/transfer" method="POST">
       <input name="to"     value="attacker_account">
       <input name="amount" value="10000">
     </form>
     <script>document.forms[0].submit()</script>
4. Alice's browser submits the form automatically
5. browser sends the request WITH Alice's bank.com session cookie
6. bank.com sees: valid session + transfer request → executes transfer

CSRF DEFENSE — the CSRF token:
  Server generates a random token per session, embeds it in every form.
  <input type="hidden" name="csrf_token" value="K9xPqR3...">
  Attacker on evil.com can't read this token (same-origin policy).
  Server rejects any POST without a matching CSRF token.

MODERN DEFENSE:
  SameSite=Strict cookie attribute:
    browser only sends cookie when request comes FROM the same site
    → evil.com form POST doesn't include the cookie → server rejects it
    This alone stops CSRF for most cases (all modern browsers support it).

WHEN CSRF STILL MATTERS:
  - Old browsers / SameSite not set
  - Subdomain-based attacks (sub.bank.com → bank.com still sends cookie)
  - API endpoints that accept cookies (use Authorization: Bearer instead)
""")
vuln.shutdown(); secure.shutdown()
