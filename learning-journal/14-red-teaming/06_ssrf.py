"""
SSRF — Server-Side Request Forgery

The server makes HTTP requests on behalf of the user.
  "Fetch this URL for me" → attacker says "fetch http://169.254.169.254/..."

The server is INSIDE the network. Attacker is OUTSIDE.
SSRF lets the attacker use the server as a proxy to reach internal services.

TARGETS:
  http://169.254.169.254/latest/meta-data/  → AWS EC2 metadata (IAM credentials!)
  http://10.0.0.1/                           → internal admin panel
  http://localhost:6379/                     → Redis (no auth by default)
  http://internal-db:5432/                  → PostgreSQL
  file:///etc/passwd                         → local file read via file:// scheme

REAL INCIDENTS:
  Capital One breach (2019): SSRF → AWS metadata → IAM credentials → S3 bucket dump
  GitLab (2021): SSRF in import feature → internal services accessible
"""

import http.server, threading, urllib.request, urllib.parse, ipaddress, socket

# ── Simulate internal services that should never be publicly reachable ────────
class InternalMetadataHandler(http.server.BaseHTTPRequestHandler):
    """Simulates AWS EC2 metadata service (internal only)"""
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"IAM_SECRET_KEY=AKIAIOSFODNN7EXAMPLE\nROLE=ec2-admin")
    def log_message(self, *a): pass

class InternalAdminHandler(http.server.BaseHTTPRequestHandler):
    """Simulates internal admin panel"""
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"INTERNAL ADMIN - DB_PASSWORD=prod_secret_9f2a")
    def log_message(self, *a): pass

# ── VULNERABLE fetch service ───────────────────────────────────────────────────
class VulnerableFetchHandler(http.server.BaseHTTPRequestHandler):
    """App that fetches a URL for the user — no validation"""
    def do_GET(self):
        params  = urllib.parse.parse_qs(self.path.split("?",1)[-1])
        url     = params.get("url", [""])[0]
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                content = r.read()
            self.send_response(200); self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500); self.end_headers()
            self.wfile.write(str(e).encode())
    def log_message(self, *a): pass

# ── SECURE fetch service — validates URL before fetching ─────────────────────
PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),   # AWS metadata range
]

def is_ssrf_safe(url: str) -> tuple[bool, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, f"scheme {parsed.scheme!r} not allowed"
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    except Exception as e:
        return False, f"DNS resolution failed: {e}"
    for net in PRIVATE_RANGES:
        if ip in net:
            return False, f"private/internal IP {ip} blocked"
    return True, "ok"

class SecureFetchHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(self.path.split("?",1)[-1])
        url    = params.get("url", [""])[0]
        ok, reason = is_ssrf_safe(url)
        if not ok:
            self.send_response(403); self.end_headers()
            self.wfile.write(f"blocked: {reason}".encode())
            return
        with urllib.request.urlopen(url, timeout=3) as r:
            self.send_response(200); self.end_headers()
            self.wfile.write(r.read())
    def log_message(self, *a): pass

def start(handler, port):
    s = http.server.HTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

internal_meta  = start(InternalMetadataHandler,  9410)
internal_admin = start(InternalAdminHandler,      9411)
vuln_fetch     = start(VulnerableFetchHandler,    9412)
secure_fetch   = start(SecureFetchHandler,        9413)

def fetch(port, url):
    encoded = urllib.parse.quote(url, safe="")
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/?url={encoded}", timeout=5) as r:
        return r.read().decode()

print("=== ATTACK: SSRF to reach internal services ===")
print(f"  Fetch internal metadata:  {fetch(9412, 'http://127.0.0.1:9410/')}")
print(f"  Fetch internal admin:     {fetch(9412, 'http://127.0.0.1:9411/')}\n")

print("=== SECURE server blocks internal URLs ===")
for target in ["http://127.0.0.1:9410/", "http://169.254.169.254/latest/meta-data/"]:
    try:
        result = fetch(9413, target)
    except Exception as e:
        result = str(e)
    print(f"  {target[:45]} → {result}")

print("""
DEFENSE LAYERS:
  1. Allowlist: only fetch from known, approved domains (not a blocklist)
  2. DNS rebinding protection: resolve hostname ONCE, validate IP, use that IP
  3. Disable unnecessary URL-fetch features entirely
  4. Network segmentation: EC2 metadata service → IMDSv2 (requires session token)
  5. Egress filtering: servers in your VPC shouldn't reach 169.254.x.x from app tier
""")
for s in [internal_meta, internal_admin, vuln_fetch, secure_fetch]:
    s.shutdown()
