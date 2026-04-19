"""
ADVERSARY EVALUATION — basic to hero

How security teams measure, score, and simulate adversaries.
Three tools used by every serious red/blue team:

  MITRE ATT&CK    → universal dictionary of adversary behaviors
  Threat Modeling → structured way to identify what could go wrong
  Purple Teaming  → measuring how fast you detect each ATT&CK technique

LEVEL 1 — BASIC: "Who might attack me and how?"
LEVEL 2 — INTERMEDIATE: "What specific techniques will they use?"
LEVEL 3 — ADVANCED: "Can we detect each technique before damage?"
LEVEL 4 — HERO: "We run adversary simulations and measure mean time to detect"
"""

import time, random, json, datetime

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 1: Threat Actor Profiling
# ─────────────────────────────────────────────────────────────────────────────

THREAT_ACTORS = {
    "script_kiddie": {
        "motivation": "fame, fun",
        "capability": 1,          # 1–5 scale
        "persistence": 1,
        "resources": "low",
        "typical_ttps": ["T1190 exploit public app", "T1595 active scanning"],
        "example_tools": ["sqlmap", "nikto", "nmap"],
        "stopped_by": ["patch known CVEs", "WAF", "fail2ban"],
    },
    "ransomware_gang": {
        "motivation": "financial extortion",
        "capability": 3,
        "persistence": 4,
        "resources": "medium–high (buy 0-days)",
        "typical_ttps": ["T1566 phishing", "T1486 data encryption", "T1490 inhibit recovery"],
        "example_tools": ["Cobalt Strike", "Mimikatz", "custom ransomware"],
        "stopped_by": ["MFA", "offline backups", "EDR on endpoints", "network segmentation"],
    },
    "nation_state_apt": {
        "motivation": "espionage, sabotage",
        "capability": 5,
        "persistence": 5,
        "resources": "nation-level budget",
        "typical_ttps": ["T1199 supply chain", "T1195 compromise infrastructure",
                         "T1027 obfuscated files", "T1071 C2 over HTTP/S"],
        "example_tools": ["custom 0-days", "living-off-the-land (LOLBins)", "signed binaries"],
        "stopped_by": ["assume breach posture", "anomaly detection", "threat intel", "zero trust"],
    },
    "insider_threat": {
        "motivation": "revenge, money, coercion",
        "capability": 3,          # knows systems well
        "persistence": 3,
        "resources": "existing access",
        "typical_ttps": ["T1078 valid accounts", "T1048 exfiltration over web", "T1074 data staging"],
        "example_tools": ["USB drives", "personal cloud upload", "authorized tools abused"],
        "stopped_by": ["least privilege", "DLP", "UEBA (user behavior analytics)", "off-boarding process"],
    },
}

print("=== LEVEL 1: Threat Actor Profiles ===")
for name, actor in THREAT_ACTORS.items():
    cap = "█" * actor["capability"] + "░" * (5 - actor["capability"])
    per = "█" * actor["persistence"] + "░" * (5 - actor["persistence"])
    print(f"\n  {name.upper()}")
    print(f"    Capability : [{cap}]  Persistence: [{per}]")
    print(f"    Motivation : {actor['motivation']}")
    print(f"    Stopped by : {actor['stopped_by'][0]}, {actor['stopped_by'][1]}")

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 2: MITRE ATT&CK Technique Mapping
# ─────────────────────────────────────────────────────────────────────────────

ATT_AND_CK_TECHNIQUES = {
    "T1566": {"name": "Phishing",                  "tactic": "Initial Access",       "detection": "email gateway, user training"},
    "T1190": {"name": "Exploit Public App",        "tactic": "Initial Access",       "detection": "WAF, patch management"},
    "T1078": {"name": "Valid Accounts",            "tactic": "Defense Evasion",      "detection": "impossible travel alert, UEBA"},
    "T1059": {"name": "Command & Script Exec",     "tactic": "Execution",            "detection": "process creation logging"},
    "T1055": {"name": "Process Injection",         "tactic": "Defense Evasion",      "detection": "EDR memory scanning"},
    "T1003": {"name": "Credential Dumping",        "tactic": "Credential Access",    "detection": "LSASS access alert (Mimikatz sig)"},
    "T1021": {"name": "Remote Services (RDP/SSH)", "tactic": "Lateral Movement",     "detection": "new lateral connection alert"},
    "T1486": {"name": "Data Encryption (Ransom)",  "tactic": "Impact",               "detection": "mass file rename / entropy spike"},
}

print("\n\n=== LEVEL 2: ATT&CK Technique Mapping (Ransomware Gang kill chain) ===")
ransomware_chain = ["T1566", "T1059", "T1003", "T1021", "T1486"]
for tid in ransomware_chain:
    t = ATT_AND_CK_TECHNIQUES[tid]
    print(f"  {tid}  {t['name']:<30} [{t['tactic']:<22}]  detect: {t['detection']}")

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 3: Purple Team Exercise — measure detection time per technique
# ─────────────────────────────────────────────────────────────────────────────

print("\n\n=== LEVEL 3: Purple Team Exercise Simulation ===")
print("  Red team executes technique → blue team measures time to alert\n")

def simulate_purple_exercise(techniques: list) -> list[dict]:
    results = []
    for tid in techniques:
        t = ATT_AND_CK_TECHNIQUES[tid]
        # simulate detection: some detected fast, some missed entirely
        detected  = random.random() > 0.3           # 70% detection rate
        detect_s  = random.randint(30, 600) if detected else None
        results.append({
            "technique": tid,
            "name": t["name"],
            "detected": detected,
            "time_to_detect_s": detect_s,
            "coverage": t["detection"],
        })
    return results

random.seed(42)
results = simulate_purple_exercise(ransomware_chain)
detected_count = sum(1 for r in results if r["detected"])

print(f"  {'Technique':<35} {'Detected':>9}  {'Time to Alert':>14}")
print("  " + "─" * 65)
for r in results:
    status = f"{r['time_to_detect_s']}s" if r["detected"] else "MISSED"
    print(f"  {r['name']:<35} {'YES' if r['detected'] else 'NO':>9}  {status:>14}")

print(f"\n  Detection rate: {detected_count}/{len(results)} techniques caught")
missed = [r["name"] for r in results if not r["detected"]]
if missed:
    print(f"  Gaps to fix:    {', '.join(missed)}")

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 4: HERO — Adversary Simulation Metrics
# ─────────────────────────────────────────────────────────────────────────────
print("""

=== LEVEL 4 (HERO): Adversary Simulation KPIs ===

  Metric                  Target      What it means
  ──────────────────────────────────────────────────────────────────
  Mean Time to Detect     < 1 hour    how fast blue team sees an attack
  Mean Time to Respond    < 4 hours   how fast they contain it
  Detection Coverage      > 80%       % of ATT&CK techniques you can detect
  Dwell Time              < 24 hours  time attacker is inside before noticed
  False Positive Rate     < 5%        % of alerts that aren't real attacks

  Tools used at hero level:
    CALDERA (MITRE)    → automated adversary emulation, runs ATT&CK techniques
    Atomic Red Team    → open-source library of ATT&CK technique tests
    Cobalt Strike      → commercial C2 framework (red team use, authorized only)
    Vectr              → tracks purple team exercises, measures coverage over time

  The journey:
    Basic:    "we have a firewall and antivirus"
    Medium:   "we log everything and have a SIEM"
    Advanced: "we run monthly purple team exercises"
    Hero:     "we run automated adversary emulation daily, MTTD < 15 min"
""")
