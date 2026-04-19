# Encryption Concepts — Cheatsheet

---

## 1. Block Cipher Basics

AES doesn't encrypt a whole message at once.
It splits data into **16-byte blocks** and encrypts each one.
The MODE decides how those blocks relate to each other.

---

## 2. AES Modes — What Changed Each Time

| Mode | Idea | IV needed? | Auth? | Use today? |
|------|------|-----------|-------|-----------|
| **ECB** | Each block encrypted independently | No | No | NEVER |
| **CBC** | Each block XORed with previous ciphertext before encrypting | Yes | No | Legacy only |
| **CTR** | Turns AES into stream cipher using counter | Yes (nonce) | No | Acceptable |
| **GCM** | CTR + built-in HMAC-like authentication tag | Yes (nonce) | YES | Default choice |

### ECB — Why it's broken
```
"ATTACK AT DAWN!!" → same block → same ciphertext every time
```
Patterns in plaintext survive into ciphertext.
Famous proof: encrypt a bitmap image with ECB — the outline is still visible.

### CBC — Fixed ECB, introduced new problem
- XORs each block with the previous ciphertext → different output even for same block
- BUT: needs padding, vulnerable to padding oracle attacks, no authentication
- Without authentication, attacker can flip bits in ciphertext and corrupt decryption silently

### GCM — Modern standard
- Encrypts with CTR mode (no padding needed)
- Produces an **authentication tag** (like HMAC built in)
- One operation = confidentiality + integrity
- Used in: TLS 1.3, HTTPS, AWS, GCP, SSH

---

## 3. IV / Nonce

**Purpose:** Make every encryption unique even with the same key and plaintext.

```
Same plaintext + Same key + Same IV  → Same ciphertext  ← BAD
Same plaintext + Same key + New IV   → Different ciphertext  ← GOOD
```

- IV is **not secret** — stored alongside ciphertext
- IV must be **unique per encryption** — never reuse
- `os.urandom(16)` — always use this, never hardcode

**Nonce reuse in GCM/CTR is catastrophic:**
```
ct1 XOR ct2 = pt1 XOR pt2   ← key cancels out entirely
Attacker learns both plaintexts
```

---

## 4. HMAC

**Purpose:** Detect if ciphertext was tampered with.

```
SHA256(message)       → anyone can forge (no key)
HMAC(key, message)    → requires secret key → tamper-proof
```

**Rule:** Never use `==` to compare HMACs — use `hmac.compare_digest()`
- `==` short-circuits → timing leak → attacker guesses byte by byte

**Real use:** Stripe webhooks, JWT signatures, cookie signing, API auth

---

## 5. KEK and DEK — Envelope Encryption

Used in: AWS KMS, GCP KMS, disk encryption (VeraCrypt), key wrapping (RFC 5649)

```
DEK  = Data Encryption Key  → actually encrypts your data  (random, strong)
KEK  = Key Encryption Key   → encrypts the DEK             (from password or HSM)
```

**Why two keys?**
- DEK is random and strong (not limited by password entropy)
- Changing password = just re-wrap the DEK, no need to re-encrypt all data
- Multiple users = each user's KEK wraps the same DEK

**Flow:**
```
SETUP:
  disk_key  = random 256-bit key
  salt      = random 16 bytes
  KEK       = scrypt(password, salt)
  wrapped   = AES_wrap(disk_key, KEK)   ← RFC 5649
  store     → salt + wrapped            ← safe to store publicly

UNLOCK:
  KEK       = scrypt(password, stored_salt)
  disk_key  = AES_unwrap(stored_wrapped, KEK)
  decrypt data with disk_key
```

---

## 6. Key Wrapping — RFC 5649

AES-ECB used in a controlled way (Feistel structure, 6 rounds).
ECB is safe here because:
- Counter XOR added each round → no two AES inputs are ever the same
- The algorithm was specifically designed to be safe with ECB

**Not** the same as raw ECB — this is a structured protocol, not just "encrypt each block".

---

## 7. KDFs — Turning Passwords into Keys

Passwords are weak. KDFs add intentional slowness to defeat brute force.

| KDF | Resistant to | Cost param | Use |
|-----|-------------|-----------|-----|
| PBKDF2 | — | iterations | Widely supported, 600k+ iterations |
| bcrypt | GPU | cost factor | Password hashing |
| scrypt | GPU + ASIC | N, r, p | Best for KEK derivation |

Salt = random bytes stored with wrapped key. Not secret. Ensures same password → different KEK on different devices.

---

## 8. Fernet vs hazmat

| | Fernet | hazmat |
|---|---|---|
| What | Pre-configured safe recipe | Raw primitives |
| Choices | None — locked in (AES-128-CBC + HMAC-SHA256) | You pick everything |
| Who | Most developers | Protocol implementors |
| Risk | Hard to misuse | Easy to misuse silently |

---

## One-Line Rules

- ECB: never use in real code
- IV: `os.urandom(16)` every single time, never reuse
- HMAC: always use `compare_digest`, never `==`
- GCM: default choice for symmetric encryption today
- DEK+KEK: always separate "what encrypts data" from "what protects the key"
- scrypt > bcrypt > PBKDF2 for password-based key derivation
