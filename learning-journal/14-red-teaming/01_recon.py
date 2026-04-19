"""
RECON — passive information gathering

Goal: learn as much as possible WITHOUT triggering alarms.
Passive recon = no packets to the target, all publicly available info.

WHAT ATTACKERS LOOK FOR:
  HTTP headers     → server version, framework, debug mode left on
  Error messages   → stack traces leak file paths, DB type, library versions
  robots.txt       → tells crawlers what NOT to index → tells attacker what's interesting
  DNS records      → subdomains, mail servers, CDN info
  GitHub/npm       → accidentally committed secrets, .env files, internal URLs
  LinkedIn/Twitter → employee names → username patterns → password spray targets
  Job listings     → "requires AWS expertise" → you're on AWS
                   → "must know Kubernetes 1.27" → exact version to target

DEMO: simulate what an attacker learns from a single HTTP response
"""

import http.server, threading, urllib.request, json, socket

# ── 1. Vulnerable server: leaks server info in headers ───────────────────────
class LeakyHandler(http.server.BaseHTTPRequestHandler):
    def version_string(self): return "Apache/2.4.51 (Ubuntu)"   # ← overrides default Server header

    def do_GET(self):
        if self.path == "/error":
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.send_header("X-Powered-By", "PHP/7.4.3")             # ← leaks language + version
            self.send_header("X-Debug-Token", "abc123")                # ← Symfony debug mode ON
            self.end_headers()
            self.wfile.write(b"Error: SQLSTATE[HY000]: Can't connect to MySQL server "
                             b"at 'db.internal.corp:3306' (errno 111)")
        elif self.path == "/robots.txt":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Disallow: /admin\nDisallow: /backup\nDisallow: /api/internal")
        else:
            self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def log_message(self, *args): pass

# ── 2. Secure server: hides all internal details ────────────────────────────
class SecureHandler(http.server.BaseHTTPRequestHandler):
    def version_string(self): return "nginx"                          # ← generic, no version

    def do_GET(self):
        if self.path == "/error":
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "internal_error", "id": "e9f2a"}).encode())
        else:
            self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def log_message(self, *args): pass

def start(handler, port):
    s = http.server.HTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

# ── Demo ─────────────────────────────────────────────────────────────────────
leaky  = start(LeakyHandler, 9101)
secure = start(SecureHandler, 9102)

def recon(label, url):
    try:
        r = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        r = e   # HTTPError is readable
    headers = dict(r.headers)
    body    = r.read().decode()
    r.close()
    print(f"\n── {label} ──")
    for k, v in headers.items():
        if k.lower() in ("server","x-powered-by","x-debug-token","content-type"):
            print(f"  Header  {k}: {v}")
    if body:
        print(f"  Body:   {body[:120]}")

print("=== What an attacker learns from HTTP headers ===")
recon("Leaky server /error",  "http://127.0.0.1:9101/error")
recon("Secure server /error", "http://127.0.0.1:9102/error")

try:
    with urllib.request.urlopen("http://127.0.0.1:9101/robots.txt") as r:
        print(f"\n── robots.txt (tells attacker where NOT to look = where to look) ──")
        print(r.read().decode())
except: pass

leaky.shutdown(); secure.shutdown()

print("""
ATTACKER'S NOTES after passive recon:
  - Server: Apache 2.4.51 → CVE-2021-41773 (path traversal) affects ≤ 2.4.49
  - PHP 7.4 → end-of-life, no security patches since Nov 2022
  - Symfony debug mode ON → /_profiler exposes full request history
  - Internal DB host: db.internal.corp:3306 (MySQL)
  - Interesting paths from robots.txt: /admin, /backup, /api/internal

DEFENSE:
  - Generic "Server: nginx" header — never include version
  - Remove X-Powered-By entirely (framework default, configure to strip)
  - Error messages: log detail server-side, return only error ID to client
  - robots.txt: use authentication, not obscurity
""")
