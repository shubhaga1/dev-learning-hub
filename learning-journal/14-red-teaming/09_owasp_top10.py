"""
OWASP TOP 10 — the 10 most critical web application security risks (2021 edition)

OWASP = Open Web Application Security Project
  Free, non-profit foundation. The Top 10 is the industry-standard baseline
  for web app security. Every audit, pentest, and compliance framework references it.

WHERE EACH IS COVERED IN THIS SERIES:
  A01 → 02_sql_injection.py  (Injection)
  A02 → 03_jwt_attacks.py    (Cryptographic Failures)
  A03 → 02_sql_injection.py + 05_xss_csrf.py  (Injection + XSS)
  A05 → 03_jwt_attacks.py    (Security Misconfiguration)
  A07 → 08_defense.py        (Identification & Auth Failures)
  A10 → 06_ssrf.py           (SSRF)
  NEW → This file covers A04, A06, A08, A09 with demos
"""

import os, json, pickle, subprocess, hashlib, secrets

# ─────────────────────────────────────────────────────────────────────────────
# A01: BROKEN ACCESS CONTROL  (moved to #1 in 2021 — most common finding)
# ─────────────────────────────────────────────────────────────────────────────
print("=== A01: Broken Access Control ===")

user_db = {
    "alice": {"role": "user",  "account_id": 101},
    "bob":   {"role": "user",  "account_id": 102},
    "admin": {"role": "admin", "account_id": 999},
}

def get_account_vulnerable(requesting_user: str, account_id: int) -> dict:
    """IDOR — Insecure Direct Object Reference. No ownership check."""
    # attacker is alice (id=101), requests account_id=999 (admin)
    return {"account_id": account_id, "balance": 50000, "secret_notes": "very sensitive"}

def get_account_secure(requesting_user: str, account_id: int) -> dict:
    """Checks that the requesting user OWNS the account they're asking for."""
    user = user_db[requesting_user]
    if user["role"] != "admin" and user["account_id"] != account_id:
        raise PermissionError(f"{requesting_user} cannot access account {account_id}")
    return {"account_id": account_id, "balance": 50000}

print(f"  Vulnerable: alice requests admin account → {get_account_vulnerable('alice', 999)}")
try:
    get_account_secure("alice", 999)
except PermissionError as e:
    print(f"  Secure: {e}\n")

# ─────────────────────────────────────────────────────────────────────────────
# A04: INSECURE DESIGN  (new in 2021 — architecture-level flaws)
# ─────────────────────────────────────────────────────────────────────────────
print("=== A04: Insecure Design ===")
print("""
  NOT a coding bug — a design flaw that can't be patched away.

  Example: password reset via security question
    "What is your mother's maiden name?" → findable on Facebook/Ancestry
    No matter how well you code it, the design is insecure.

  Secure design: time-limited reset token sent to verified email only.

  Example: no rate limiting in the design
    Login page allows unlimited attempts → brute-forceable by design
    Fix must be in the design (rate limit + lockout), not just the code.

  Principle: Threat Model BEFORE you write code, not after.\n""")

# ─────────────────────────────────────────────────────────────────────────────
# A06: VULNERABLE & OUTDATED COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────
print("=== A06: Vulnerable & Outdated Components ===")

fake_deps = {
    "log4j":    "2.14.1",   # CVE-2021-44228  Log4Shell — RCE, CVSS 10.0
    "requests": "2.18.0",   # CVE-2018-18074  credential leak
    "django":   "2.1.0",    # CVE-2019-6975   memory exhaustion
    "flask":    "1.0.2",    # CVE-2018-1000656 DoS
}
# up-to-date versions
safe_versions = {"log4j": "2.17.1", "requests": "2.31.0", "django": "4.2.7", "flask": "3.0.0"}

print("  Dependency scan results:")
for pkg, ver in fake_deps.items():
    status = "VULNERABLE" if ver < safe_versions[pkg] else "ok"
    print(f"    {pkg:<12} {ver:<10} → {status}  (safe: {safe_versions[pkg]})")
print("  Fix: Dependabot / Snyk / pip-audit in CI pipeline\n")

# ─────────────────────────────────────────────────────────────────────────────
# A08: SOFTWARE & DATA INTEGRITY FAILURES  (insecure deserialization)
# ─────────────────────────────────────────────────────────────────────────────
print("=== A08: Insecure Deserialization (pickle) ===")

class Exploit:
    """A malicious object that runs OS commands when unpickled."""
    def __reduce__(self):
        return (os.system, ("echo 'PWNED: attacker ran code on your server'",))

malicious_data = pickle.dumps(Exploit())   # attacker sends this as a cookie/API body

print("  Vulnerable: deserializing untrusted pickle data...")
pickle.loads(malicious_data)               # ← executes the OS command above!

print("  Secure: NEVER unpickle untrusted data. Use JSON instead.")
safe_data   = json.dumps({"user": "alice", "role": "user"})
safe_parsed = json.loads(safe_data)        # JSON can't execute code
print(f"  JSON parsed safely: {safe_parsed}\n")

# ─────────────────────────────────────────────────────────────────────────────
# A09: SECURITY LOGGING & MONITORING FAILURES
# ─────────────────────────────────────────────────────────────────────────────
print("=== A09: Security Logging Failures ===")
print("""
  Average time to detect a breach: 207 days (IBM 2023 report)
  Average time to contain:          73 days
  Total: 280 days of attacker dwell time — because no one was watching.

  What must be logged (with timestamp + IP + user):
    ✓ Every login attempt (success AND failure)
    ✓ Every privilege escalation (user → admin)
    ✓ Every data export > threshold (10 MB, 1000 records)
    ✓ Every change to security config (MFA disabled, new admin created)
    ✓ Every input validation failure (potential attack in progress)

  What most apps log:
    ✗ Errors only
    ✗ No IP addresses
    ✗ Logs stored on same server (attacker deletes after compromise)

  Detection example: 5 failed logins from same IP in 60s → alert + block IP
  See: 08_defense.py for implementation.\n""")

print("""
OWASP TOP 10 — 2021 QUICK REFERENCE:
  A01  Broken Access Control        IDOR, missing auth checks, privilege escalation
  A02  Cryptographic Failures       MD5/SHA1 passwords, HTTP, hardcoded keys
  A03  Injection                    SQL, command, LDAP, XSS (now includes injection broadly)
  A04  Insecure Design              No threat model, no rate limit by design
  A05  Security Misconfiguration    Default passwords, debug mode on, open S3 buckets
  A06  Vulnerable Components        Log4Shell, unpatched libraries
  A07  Auth & Identification Fail   Weak passwords, no MFA, bad session tokens
  A08  Software Integrity Failures  Insecure deserialization, unsigned updates
  A09  Logging & Monitoring Fail    No alerts, no audit log, long dwell time
  A10  SSRF                         Server fetches attacker-controlled URL

Full detail: https://owasp.org/Top10/
""")
