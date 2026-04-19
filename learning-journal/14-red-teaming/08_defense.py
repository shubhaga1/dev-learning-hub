"""
DEFENSE — what the blue team does and how to measure security posture

Red team finds the holes. Blue team closes them and detects intrusions.
Purple team: both working together — red attacks, blue measures detection time.

DEFENSE IN DEPTH:
  No single control stops everything. Layer multiple controls so
  an attacker who bypasses one still hits another.

  Layer 1:  Perimeter (firewall, WAF, DDoS protection)
  Layer 2:  Authentication (MFA, strong passwords, SSO)
  Layer 3:  Authorization (RBAC, least privilege)
  Layer 4:  Input validation (parameterized SQL, output encoding)
  Layer 5:  Secrets management (no hardcoded keys, rotate regularly)
  Layer 6:  Logging & monitoring (detect anomalies, alert on suspicious behavior)
  Layer 7:  Incident response (know what to do WHEN, not IF)
"""

import logging, json, datetime, hashlib, secrets, os

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("security")

# ── 1. Structured security logging ────────────────────────────────────────────
def security_event(event_type: str, user: str, ip: str, detail: dict):
    """Every security event logged as structured JSON for SIEM ingestion."""
    entry = {
        "ts":         datetime.datetime.utcnow().isoformat() + "Z",
        "event":      event_type,
        "user":       user,
        "ip":         ip,
        "detail":     detail,
        "severity":   "HIGH" if "fail" in event_type or "attack" in event_type else "INFO",
    }
    log.info(json.dumps(entry))
    return entry

print("=== Structured security logging ===")
security_event("login_success",       "alice",   "10.0.1.5",  {"method": "MFA"})
security_event("login_fail",          "admin",   "185.1.2.3", {"reason": "wrong_password", "attempt": 5})
security_event("sqli_attack_blocked", "unknown", "185.1.2.3", {"payload": "' OR 1=1--", "endpoint": "/login"})
security_event("file_read_blocked",   "bob",     "10.0.1.9",  {"path": "../../etc/passwd"})
print()

# ── 2. Password hashing (bcrypt-like with PBKDF2) ─────────────────────────────
def hash_password(password: str) -> str:
    """PBKDF2 with 600,000 iterations — the OWASP recommended minimum (2023)."""
    salt = secrets.token_bytes(16)
    dk   = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
    return salt.hex() + ":" + dk.hex()

def verify_password(password: str, stored: str) -> bool:
    salt_hex, dk_hex = stored.split(":")
    salt = bytes.fromhex(salt_hex)
    dk   = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
    return secrets.compare_digest(dk.hex(), dk_hex)   # constant-time compare

print("=== Secure password hashing (PBKDF2, 600k iterations) ===")
stored = hash_password("hunter2")
print(f"  Stored hash: {stored[:40]}...")
print(f"  Verify correct:   {verify_password('hunter2', stored)}")
print(f"  Verify wrong:     {verify_password('password', stored)}\n")

# ── 3. Rate limiting (brute-force protection) ─────────────────────────────────
login_attempts: dict[str, list] = {}
MAX_ATTEMPTS = 5
WINDOW_SECONDS = 300

def check_rate_limit(ip: str) -> tuple[bool, str]:
    now = datetime.datetime.utcnow().timestamp()
    attempts = [t for t in login_attempts.get(ip, []) if now - t < WINDOW_SECONDS]
    login_attempts[ip] = attempts
    if len(attempts) >= MAX_ATTEMPTS:
        return False, f"rate limited: {len(attempts)} attempts in {WINDOW_SECONDS}s"
    login_attempts[ip].append(now)
    return True, "ok"

print("=== Rate limiting (brute-force protection) ===")
attacker_ip = "185.1.2.3"
for i in range(7):
    ok, reason = check_rate_limit(attacker_ip)
    print(f"  Attempt {i+1}: {'ALLOWED' if ok else 'BLOCKED'} — {reason}")
print()

# ── 4. Security checklist ─────────────────────────────────────────────────────
print("""
=== SECURITY CHECKLIST (OWASP / NIST baseline) ===

AUTHENTICATION:
  [ ] MFA required for all privileged accounts
  [ ] Passwords hashed with bcrypt/PBKDF2/Argon2 (not MD5/SHA1)
  [ ] Account lockout after N failed attempts (+ rate limiting by IP)
  [ ] Session tokens: random, 128+ bits, HttpOnly + Secure + SameSite=Strict

INPUT VALIDATION:
  [ ] Parameterized queries everywhere (no string-concat SQL)
  [ ] Output HTML-escaped before rendering (prevent XSS)
  [ ] File path inputs validated with realpath() + prefix check
  [ ] URL fetch inputs validated against allowlist (prevent SSRF)

SECRETS:
  [ ] No credentials in source code or git history
  [ ] Secrets in env vars or a secrets manager (AWS Secrets Manager, Vault)
  [ ] JWT secret: 256-bit random, rotated quarterly
  [ ] API keys scoped to minimum permissions, rotated on staff change

LOGGING:
  [ ] All authentication events logged (success + failure)
  [ ] All input validation failures logged with IP and payload
  [ ] Logs shipped off-machine (attacker can't delete them after compromise)
  [ ] Alerts on: 5+ failed logins, new admin account, data export > 10MB

NETWORK:
  [ ] HTTPS everywhere (TLS 1.2 minimum, 1.3 preferred)
  [ ] HSTS header set (forces HTTPS even if user types http://)
  [ ] Internal services not reachable from internet (VPC, security groups)
  [ ] Egress filtering: app servers shouldn't reach 169.254.x.x

PATCHING:
  [ ] Dependency scanning (Dependabot, Snyk) in CI
  [ ] Critical CVE patches within 24–48h
  [ ] Container base images rebuilt weekly (pick up OS patches)
""")
