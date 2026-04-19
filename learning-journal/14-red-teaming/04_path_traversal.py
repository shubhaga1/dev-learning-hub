"""
PATH TRAVERSAL (LFI) — reading files outside the intended directory

Local File Inclusion (LFI): attacker controls a file path parameter.
App: serves /app/uploads/<filename>
Attack: /app/uploads/../../etc/passwd

../  means "go up one directory"
../../etc/passwd = up from uploads/, up from app/, then into /etc/passwd

IMPACT:
  - Read /etc/passwd → usernames for further attacks
  - Read app config files → DB credentials, API keys
  - Read private keys, .env files, session stores
  - Combined with log poisoning → Remote Code Execution
"""

import http.server, threading, urllib.request, urllib.parse, os, tempfile

# ── Setup: create a fake app directory with sensitive files ───────────────────
APP_DIR = tempfile.mkdtemp(prefix="app_")
UPLOAD_DIR = os.path.join(APP_DIR, "uploads")
os.makedirs(UPLOAD_DIR)

# public file (intended)
with open(os.path.join(UPLOAD_DIR, "photo.jpg"), "w") as f:
    f.write("fake image data")

# sensitive config one level up (should never be served)
with open(os.path.join(APP_DIR, "config.env"), "w") as f:
    f.write("DB_PASSWORD=supersecret\nAWS_SECRET_KEY=AKIAIOSFODNN7EXAMPLE\nJWT_SECRET=abc123")

# ── VULNERABLE file server ────────────────────────────────────────────────────
class VulnerableHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        filename = self.path.lstrip("/")
        filepath = os.path.join(UPLOAD_DIR, filename)   # ← no validation!
        try:
            with open(filepath, "r") as f:
                content = f.read()
            self.send_response(200); self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_response(404); self.end_headers()
    def log_message(self, *a): pass

# ── SECURE file server ────────────────────────────────────────────────────────
class SecureHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        raw      = self.path.lstrip("/")
        # resolve the real absolute path, then verify it's inside UPLOAD_DIR
        filepath = os.path.realpath(os.path.join(UPLOAD_DIR, raw))
        if not filepath.startswith(os.path.realpath(UPLOAD_DIR) + os.sep):
            self.send_response(403); self.end_headers()
            self.wfile.write(b"forbidden")
            return
        try:
            with open(filepath, "r") as f:
                content = f.read()
            self.send_response(200); self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_response(404); self.end_headers()
    def log_message(self, *a): pass

def start(handler, port):
    s = http.server.HTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

vuln   = start(VulnerableHandler, 9201)
secure = start(SecureHandler,     9202)

def get(port, path):
    try:
        url = f"http://127.0.0.1:{port}/{urllib.parse.quote(path)}"
        with urllib.request.urlopen(url) as r:
            return r.read().decode()
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"

print("=== ATTACK: path traversal on vulnerable server ===")
print(f"  Normal request /photo.jpg:       {get(9201, 'photo.jpg')[:30]}")

traversal = "../config.env"
result    = get(9201, traversal)
print(f"  Traversal /{traversal}:  {result}")
print("  ↑ attacker just read the DB password and AWS secret key!\n")

print("=== SECURE server blocks traversal ===")
print(f"  Normal request /photo.jpg:       {get(9202, 'photo.jpg')[:30]}")
print(f"  Traversal /{traversal}:  {get(9202, traversal)}")

print("""
HOW os.path.realpath() STOPS IT:
  UPLOAD_DIR = /tmp/app_xyz/uploads
  Request:    ../config.env
  Join:       /tmp/app_xyz/uploads/../config.env
  realpath(): /tmp/app_xyz/config.env          ← resolves ..
  Check:      does it start with /tmp/app_xyz/uploads/? NO → 403

COMMON BYPASSES ATTACKERS TRY (all blocked by realpath check):
  ../etc/passwd           standard
  ..%2Fetc%2Fpasswd       URL encoded /
  ....//etc/passwd        double dot slash
  %252e%252e/etc/passwd   double URL encoded
  All resolve to the same real path → same check blocks all.

DEFENSE:
  - os.path.realpath() + prefix check (as shown)
  - Serve files from a separate content delivery path entirely
  - Never pass user-controlled values to file system APIs
""")

vuln.shutdown(); secure.shutdown()
import shutil; shutil.rmtree(APP_DIR)
