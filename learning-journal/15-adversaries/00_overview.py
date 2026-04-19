"""
ADVERSARIES — who attacks systems, why, and how to model them

This folder covers the HUMAN side of security:
  - Who are the threat actors
  - What motivates them
  - What techniques (TTPs) they use
  - How to score and simulate them (purple teaming)

FILES:
  01_threat_actors.py              profiles of 4 adversary types + threat model decision tree
  02_evaluation_basic_to_hero.py   adversary evaluation from basic to hero level
                                     L1: threat actor profiling
                                     L2: MITRE ATT&CK technique mapping
                                     L3: purple team exercise simulation
                                     L4: KPIs (MTTD, MTTR, detection coverage)

KEY CONCEPTS:
  Threat Actor    = who is attacking (script kiddie, ransomware gang, APT, insider)
  TTP             = Tactic / Technique / Procedure (MITRE ATT&CK language)
  Kill Chain      = the attacker's step-by-step path from recon to impact
  Purple Teaming  = red team attacks + blue team measures detection time
  MTTD            = Mean Time to Detect (target: < 1 hour)
  MTTR            = Mean Time to Respond (target: < 4 hours)
  Dwell Time      = how long attacker is inside before noticed (avg: 207 days)

MITRE ATT&CK MATRIX — the universal playbook:
  14 tactics  ×  200+ techniques
  Used by every serious red team, blue team, and compliance framework.
  Reference: https://attack.mitre.org

LEARNING ORDER:
  01 → understand who the adversaries are
  02 → learn to evaluate your defenses against them (basic → hero progression)
"""
