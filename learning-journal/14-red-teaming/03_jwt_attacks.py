"""
JWT ATTACKS — tampering with authentication tokens

JWT = JSON Web Token.  Used to prove identity after login.
  Header.Payload.Signature  (each base64url encoded, separated by .)

  Header:   {"alg": "HS256", "typ": "JWT"}
  Payload:  {"user": "alice", "role": "user", "exp": 1234567890}
  Signature: HMAC-SHA256(header + "." + payload, secret_key)

THE SERVER TRUSTS the token if the signature is valid.
Attack = make a token the server accepts, with a payload YOU control.

ATTACK 1 — alg:none  (CVE-2015-9235, affected many libraries)
  Change alg to "none" → no signature needed → server skips verification
  Attacker sets role:"admin" and the server believes it

ATTACK 2 — weak secret brute-force
  HS256 uses a symmetric secret. If secret is weak ("secret", "password"),
  attacker can brute-force it offline → forge any token with full control

ATTACK 3 — algorithm confusion (HS256 vs RS256)
  Server uses RS256 (asymmetric). Public key is... public.
  Attacker switches alg to HS256, signs with the PUBLIC KEY as the HMAC secret.
  Vulnerable server: "HS256 signature, check with current key" → uses public key → valid!
"""

import base64, json, hmac, hashlib

SECRET = "supersecret"  # real apps use long random secrets

def b64enc(data: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(data, separators=(',',':')).encode()).rstrip(b'=').decode()

def b64dec(s: str) -> dict:
    pad = 4 - len(s) % 4
    return json.loads(base64.urlsafe_b64decode(s + '=' * pad))

def sign(header: dict, payload: dict, secret: str) -> str:
    msg = f"{b64enc(header)}.{b64enc(payload)}".encode()
    sig = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).rstrip(b'=').decode()

def make_token(payload: dict, secret=SECRET) -> str:
    h = {"alg": "HS256", "typ": "JWT"}
    return f"{b64enc(h)}.{b64enc(payload)}.{sign(h, payload, secret)}"

# ── Vulnerable verifier (accepts alg:none) ────────────────────────────────────
def verify_vulnerable(token: str) -> dict:
    parts = token.split('.')
    header  = b64dec(parts[0])
    payload = b64dec(parts[1])
    if header.get('alg') == 'none':
        return payload                  # ← BUG: no signature check!
    sig = parts[2]
    expected = sign(header, payload, SECRET)
    if not hmac.compare_digest(sig, expected):
        raise ValueError("invalid signature")
    return payload

# ── Secure verifier (whitelist algorithm, always verify) ─────────────────────
def verify_secure(token: str) -> dict:
    parts = token.split('.')
    header  = b64dec(parts[0])
    payload = b64dec(parts[1])
    if header.get('alg') != 'HS256':    # ← whitelist — reject 'none', 'RS256' etc.
        raise ValueError(f"rejected alg: {header.get('alg')}")
    expected = sign(header, payload, SECRET)
    if not hmac.compare_digest(parts[2], expected):
        raise ValueError("invalid signature")
    return payload

# ── Demo ──────────────────────────────────────────────────────────────────────
legit = make_token({"user": "alice", "role": "user"})
print(f"Legit token: {legit[:60]}...\n")

print("=== ATTACK 1: alg:none — forge admin token without knowing secret ===")
forged_header  = b64enc({"alg": "none", "typ": "JWT"})
forged_payload = b64enc({"user": "alice", "role": "admin"})   # ← elevated to admin
forged_token   = f"{forged_header}.{forged_payload}."         # ← empty signature
print(f"  Forged token: {forged_token[:60]}...")
try:
    result = verify_vulnerable(forged_token)
    print(f"  Vulnerable server: {result}  ← ATTACK SUCCEEDED, got admin role!")
except Exception as e:
    print(f"  {e}")
try:
    verify_secure(forged_token)
except ValueError as e:
    print(f"  Secure server:     REJECTED — {e}\n")

print("=== ATTACK 2: brute-force weak secret ===")
weak_secret_token = make_token({"user": "bob", "role": "user"}, secret="secret")
wordlist = ["password", "123456", "secret", "admin", "letmein"]
for guess in wordlist:
    parts   = weak_secret_token.split('.')
    header  = b64dec(parts[0])
    payload = b64dec(parts[1])
    attempt = sign(header, payload, guess)
    if attempt == parts[2]:
        print(f"  Secret cracked: {guess!r} — attacker can now forge ANY token!\n")
        break

print("=== ATTACK 3: tamper payload — change role without knowing secret ===")
parts   = legit.split('.')
payload = b64dec(parts[1])
payload["role"] = "admin"
tampered = f"{parts[0]}.{b64enc(payload)}.{parts[2]}"
try:
    verify_secure(tampered)
except ValueError as e:
    print(f"  Tampered token rejected: {e}")

print("""
DEFENSES:
  - Always whitelist allowed algorithms (HS256 only, or RS256 only)
  - Use long random secrets (32+ bytes from os.urandom)
  - Validate exp (expiry) and iat (issued-at) claims
  - Use a well-maintained library (PyJWT, jose) — don't roll your own
  - For sensitive ops (admin, payment), re-verify server-side, not just JWT
""")
