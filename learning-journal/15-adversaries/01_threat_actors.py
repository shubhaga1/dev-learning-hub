"""
ADVERSARIES — who attacks systems and why

Understanding the attacker helps you prioritize defenses correctly.
Different adversaries have different tools, time, money, and goals.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THREAT MODEL: Motivation × Capability × Persistence
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. SCRIPT KIDDIE
   Motivation:   fun, reputation, curiosity
   Capability:   low — uses pre-built tools (Metasploit, SQLmap, Nmap)
   Persistence:  low — moves on if first attempt fails
   Targets:      opportunistic, mass scan for known CVEs
   Defense:      patch known CVEs quickly, fail fast (no useful error messages)

2. CYBERCRIMINAL / RANSOMWARE GANG
   Motivation:   money — extortion, credit card theft, crypto theft
   Capability:   medium to high — organized groups, buy 0-days on darkweb
   Persistence:  high — will spend weeks if the payout is large enough
   Targets:      hospitals, supply chains, financial firms, e-commerce
   TTPs:         phishing email → RCE → lateral movement → encrypt + ransom
   Defense:      MFA everywhere, endpoint detection, offline backups, segment network

3. HACKTIVIST
   Motivation:   ideology, political statement, embarrassment
   Capability:   low to medium — LOIC DDoS tool, SQLi, data dumps
   Persistence:  medium — motivated but not well-resourced
   Targets:      governments, corporations they oppose
   TTPs:         DDoS, deface website, dump & leak data (doxing)
   Defense:      DDoS mitigation (Cloudflare), restrict public data exposure

4. INSIDER THREAT
   Motivation:   revenge, financial gain, coercion, negligence
   Capability:   high — already has access, knows the systems
   Persistence:  varies — disgruntled employee acts quickly; spy acts slowly
   Targets:      your own employer
   TTPs:         exfiltrate data before leaving, plant backdoor, abuse privileges
   Defense:      least-privilege, data loss prevention (DLP), anomaly detection on access logs

5. NATION-STATE / APT (Advanced Persistent Threat)
   Motivation:   espionage, sabotage, geopolitical advantage
   Capability:   very high — 0-day exploits, custom malware, huge teams, years of patience
   Persistence:  very high — will stay hidden for months/years (avg dwell time: 200 days)
   Targets:      critical infrastructure, defence, tech companies, governments
   Examples:     APT29 (Cozy Bear, Russia), APT41 (China), Lazarus (North Korea)
   TTPs:         spearphishing → C2 implant → living-off-the-land → exfiltrate slowly
   Defense:      assume breach, network segmentation, anomaly detection, threat intel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TTP = Tactics, Techniques, Procedures  (MITRE ATT&CK framework)
  Tactic:     high-level goal (e.g. Initial Access, Privilege Escalation)
  Technique:  HOW to achieve it (e.g. Phishing, Exploit Public-Facing App)
  Procedure:  specific implementation used by a particular group
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MITRE ATT&CK MATRIX (the universal adversary playbook):
  14 tactics, 200+ techniques.  Used by red teams AND blue teams.

  Tactic               Example Techniques
  ─────────────────────────────────────────────────────────────────
  Reconnaissance       Active scanning, OSINT, gather credentials
  Resource Development Buy infrastructure, stage capabilities
  Initial Access       Phishing, exploit public app, supply chain
  Execution            PowerShell, command-line, scheduled tasks
  Persistence          Registry run keys, cron jobs, new accounts
  Privilege Escalation Sudo abuse, SUID binaries, token impersonation
  Defense Evasion      Obfuscation, timestomping, disable logging
  Credential Access    Credential dumping (Mimikatz), keylogging
  Discovery            Network scan, file enumeration, whoami/ipconfig
  Lateral Movement     Pass-the-hash, RDP, SSH, shared drives
  Collection           Screen capture, keylogger, clipboard data
  C2                   HTTP/S beaconing, DNS tunneling, WebSocket
  Exfiltration         Cloud storage upload, HTTPS to external, USB
  Impact               Ransomware, wiper, defacement, DDoS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO: simulate adversary decision tree
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

def threat_model(target_value: str, security_level: str):
    """
    Given target value (low/medium/high) and security posture,
    show which adversaries are likely and their entry points.
    """
    print(f"\nTarget value: {target_value}  |  Security: {security_level}")
    print("─" * 60)

    likely = []
    if target_value in ("low", "medium"):
        likely.append(("Script Kiddie",   "automated mass scan, known CVEs"))
        likely.append(("Hacktivist",       "DDoS, SQLi, website defacement"))
    if target_value in ("medium", "high"):
        likely.append(("Cybercriminal",    "phishing → ransomware, card theft"))
        likely.append(("Insider Threat",   "data exfiltration, sabotage"))
    if target_value == "high":
        likely.append(("Nation-State APT", "spearphish → implant → long dwell"))

    for adv, tactic in likely:
        print(f"  [{adv:<20}] via: {tactic}")

    if security_level == "low":
        print(f"\n  Priority fixes: patch CVEs, add MFA, enable logging")
    elif security_level == "medium":
        print(f"\n  Priority fixes: network segmentation, DLP, anomaly detection")
    else:
        print(f"\n  Priority fixes: threat intel feeds, assume-breach drills")

# Run the threat model
threat_model("low",    "low")
threat_model("high",   "medium")
threat_model("high",   "high")

print("""
HOW TO USE THIS FOR RED TEAMING:
  1. Identify your most likely adversary type
  2. Look up their TTPs in MITRE ATT&CK
  3. Red team simulates those specific TTPs
  4. Blue team measures detection + response time
  5. Gap = your real risk exposure

REFERENCE: https://attack.mitre.org — free, comprehensive, used by every serious security team
""")
