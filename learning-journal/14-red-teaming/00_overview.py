"""
RED TEAMING — simulating an attacker to find weaknesses before real attackers do

Red team = attackers (offensive, find holes)
Blue team = defenders (defensive, detect + respond)
Purple team = both working together

WHY IT EXISTS:
  Security teams get comfortable with their own defenses.
  A red team thinks like an outsider — no assumptions, no blind spots.
  "If I were an attacker, how would I get in?"

THE KILL CHAIN (attacker's step-by-step playbook):
  1. RECON         → gather info without touching the target
                     DNS records, LinkedIn employees, GitHub leaks, error messages
  2. WEAPONIZE     → build an exploit for a discovered weakness
                     SQLi payload, phishing email, malicious file
  3. DELIVER       → get the weapon to the target
                     email attachment, URL in a message, compromised dependency
  4. EXPLOIT       → execute — trigger the vulnerability
                     SQL executes, XSS fires in victim's browser
  5. ESTABLISH     → get persistent access (foothold)
                     backdoor, reverse shell, stolen credentials
  6. MOVE LATERALLY → pivot to higher-value systems
                     use compromised machine to reach internal DB
  7. EXFILTRATE    → extract the data / achieve the goal
                     dump the DB, steal keys, encrypt for ransomware

THIS FOLDER — Web Attack POCs (local, no real targets):
  01_recon.py          passive info gathering: headers, DNS, error leakage
  02_sql_injection.py  attack + defense against a local SQLite DB
  03_jwt_attacks.py    JWT algorithm confusion, secret brute-force, token tampering
  04_path_traversal.py LFI / directory traversal on a local file server
  05_xss_csrf.py       XSS payload injection + CSRF token bypass concept
  06_ssrf.py           Server-Side Request Forgery — make the server fetch for you
  08_defense.py        mitigations, logging patterns, detection checklist
  09_owasp_top10.py    all 10 OWASP categories with runnable demos

RELATED FOLDERS:
  ../15-adversaries/       who attacks you, threat modeling, MITRE ATT&CK, purple teaming
  ../16-llm-jailbreaking/  LLM-specific attacks: prompt injection, roleplay, instruction hacking

TYPES OF RED TEAM ENGAGEMENTS:
  Black box   → zero knowledge, just a URL (realistic attacker simulation)
  Grey box    → some knowledge (credentials, architecture docs)
  White box   → full access to source code + infra (most thorough)
  Purple team → red + blue work together, focus on detection improvement

RULES OF ENGAGEMENT (always required for real work):
  - Written authorization from the asset owner
  - Defined scope (which systems are in/out)
  - Emergency contacts (in case you break something)
  - No production data exfiltration
  - Report all findings, even if not exploited

LEGAL:
  Unauthorized access = crime in every jurisdiction.
  Everything in this series runs against LOCAL resources you own.
"""
