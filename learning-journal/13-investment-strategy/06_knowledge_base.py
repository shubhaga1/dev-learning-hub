"""
Step 6: Knowledge Base — Seminars, Market Facts, Research
===========================================================
Every insight you gather goes here. Code reads this to enrich decisions.

MIT Lecture: "Capital market assumptions are inherently uncertain.
              Models must be robust. Feed in the best data you have."

Add entries to SEMINARS, MARKET_FACTS, and RBI_WATCH anytime.
Run: python3 06_knowledge_base.py

Structure:
  SEMINARS      — notes from talks, courses, books
  MARKET_FACTS  — city/sector level static research data
  RBI_WATCH     — macro events that affect all properties
  RULES         — your personal investment rules (your "investment policy statement")
"""

from datetime import date

# ─────────────────────────────────────────────────────────
# SEMINARS — add any talk, book, course insight here
# ─────────────────────────────────────────────────────────

SEMINARS = [
    {
        "source":   "MIT OCW — Jake Xia, Portfolio Management 2013",
        "date":     date(2024, 1, 1),
        "category": "Framework",
        "insights": [
            "Portfolio = sizing problem. Allocate proportional to conviction and loss tolerance.",
            "Volatility treats upside and downside equally — bad metric. Use Gain-Loss ratio.",
            "Gain-Loss ratio > 2x = good trade. <1x = reject regardless of upside story.",
            "Endowment model: target 8% real return = 5% spending + inflation.",
            "Rebalancing is mandatory. Drift without rebalancing destroys diversification.",
            "Crowding: when everyone is buying same asset class, exit or reduce.",
            "Power law: top 20% of investments generate 80% of returns — size winners bigger.",
            "Liquidity is existential risk. Illiquid portfolio = can't rebalance in a crisis.",
            "2008 lesson: endowments with 70%+ illiquid assets had to cut spending by 30%.",
        ]
    },
    {
        "source":   "Add: Next seminar / book / podcast",
        "date":     date(2025, 1, 1),
        "category": "Real Estate",
        "insights": [
            "Add insight here",
        ]
    },
]

# ─────────────────────────────────────────────────────────
# MARKET FACTS — city + micro-market level static research
# ─────────────────────────────────────────────────────────

MARKET_FACTS = {
    "Noida": {
        "overall_outlook":  "Positive — expressway, Jewar airport, Film City pipeline",
        "best_micro_markets": ["Sec 150", "Sec 62", "Sec 137"],
        "risk_factors":     ["40% unsold inventory in some pockets", "Builder delays historical"],
        "avg_appreciation_5yr_pct": 8.5,
        "avg_rental_yield_pct":     2.5,
        "liquidity_score":          3,   # 1-5
        "catalysts": [
            "Jewar International Airport — operational 2025",
            "Noida International Film City — 20,000+ jobs expected",
            "Aqua Line Metro extension to Sec 142, 143",
        ],
        "sources": ["PropTiger Q4 2024", "NHB Residex", "TOI Infrastructure Beat"]
    },
    "Bangalore": {
        "overall_outlook":  "Strong — India's IT capital, consistent demand from MNCs",
        "best_micro_markets": ["Whitefield", "Sarjapur", "Hebbal", "Electronic City Ph2"],
        "risk_factors":     ["Water scarcity", "Traffic congestion limits peripheral growth", "Oversupply in luxury segment"],
        "avg_appreciation_5yr_pct": 10.2,
        "avg_rental_yield_pct":     3.2,
        "liquidity_score":          4,
        "catalysts": [
            "Global Capability Centers — 50+ new GCCs planned by 2026",
            "Purple Line Metro extension to Whitefield",
            "STRR (Steel Flyover Ring Road) improving connectivity",
        ],
        "sources": ["JLL India 2024", "Knight Frank Residential 2024"]
    },
    "Gurgaon": {
        "overall_outlook":  "Premium — luxury market, strong NRI and HNI demand",
        "best_micro_markets": ["Golf Course Ext Road", "Dwarka Expressway", "Sohna Road"],
        "risk_factors":     ["Premium pricing limits rental yield", "Sector 99+ still developing"],
        "avg_appreciation_5yr_pct": 11.5,
        "avg_rental_yield_pct":     2.8,
        "liquidity_score":          4,
        "catalysts": [
            "Dwarka Expressway — fully operational 2024",
            "IMT Manesar — industrial and IT expansion",
            "Delhi-Mumbai Expressway connectivity",
        ],
        "sources": ["Anarock Q1 2025", "99acres Gurgaon Market Report"]
    },
    "Mumbai": {
        "overall_outlook":  "Stable premium — highest prices, lowest yield, capital preservation play",
        "best_micro_markets": ["Powai", "Thane", "Navi Mumbai", "Chembur", "Bandra East"],
        "risk_factors":     ["Highest entry cost in India", "Rental yield 1.5-2.5% — lowest in India", "Stamp duty 5-6%"],
        "avg_appreciation_5yr_pct": 7.2,
        "avg_rental_yield_pct":     2.0,
        "liquidity_score":          5,
        "catalysts": [
            "Trans Harbour Link — Navi Mumbai connectivity",
            "Navi Mumbai International Airport — operational 2025",
            "BKC Dharavi Redevelopment — massive supply shift",
        ],
        "sources": ["Liases Foras", "Anarock Residential Monitor"]
    },
}

# ─────────────────────────────────────────────────────────
# RBI WATCH — macro events that affect all your properties
# ─────────────────────────────────────────────────────────

RBI_WATCH = [
    {
        "date":   date(2025, 2, 1),
        "event":  "RBI MPC — Repo Rate Cut",
        "detail": "Repo rate cut 25bps to 6.25%. First cut since 2020.",
        "impact": "Home loan rates expected to drop by 0.25%. Buyer affordability improves. Demand may increase in mid-segment.",
        "action": "Hold all properties. Rate cuts boost prices. Do NOT sell in falling rate environment.",
    },
    {
        "date":   date(2024, 10, 1),
        "event":  "SEBI REIT Regulation Update",
        "detail": "SEBI allows fractional ownership of commercial RE. Min ticket ₹10L.",
        "impact": "Alternative to direct property. Liquid, yielding 7-8%. Good for diversification.",
        "action": "Consider allocating 10% of RE budget to REITs for liquidity.",
    },
    {
        "date":   date(2024, 1, 1),
        "event":  "India Budget 2024 — Real Estate",
        "detail": "LTCG indexation benefit removed for RE. Flat 12.5% LTCG now.",
        "impact": "Selling property now more tax-efficient for high-appreciation properties (vs old 20% with indexation for some cases). Recalculate exit tax for each property.",
        "action": "Review exit tax calculation for each property before deciding to sell.",
    },
]

# ─────────────────────────────────────────────────────────
# YOUR PERSONAL INVESTMENT RULES (Investment Policy Statement)
# MIT: Every serious investor writes these down
# ─────────────────────────────────────────────────────────

MY_RULES = [
    "Never buy a property where EMI > 2x the rental income (negative carry kills cash flow)",
    "Never have > 50% of total net worth in real estate (illiquidity risk)",
    "No single city > 40% of RE portfolio value",
    "Every property must have a written exit trigger before buying",
    "Gain-Loss must be > 2x: upside (base - cost) must be 2x the downside (cost - bear case)",
    "Review every property every 6 months — update current value, rent, and decision",
    "Never buy in a location with > 30% unsold inventory (oversupply = price pressure)",
    "Always check RERA registration before any booking — no RERA = no deal",
]

# ─────────────────────────────────────────────────────────
# PRINT KNOWLEDGE BASE SUMMARY
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 65)
    print("  KNOWLEDGE BASE SUMMARY")
    print("=" * 65)

    print(f"\n📚 SEMINARS ({len(SEMINARS)} sources)")
    for s in SEMINARS:
        print(f"\n  [{s['date']}] {s['source']}")
        for insight in s["insights"][:3]:  # show first 3
            print(f"    → {insight}")
        if len(s["insights"]) > 3:
            print(f"    ... +{len(s['insights'])-3} more insights")

    print(f"\n🏙  MARKET FACTS ({len(MARKET_FACTS)} cities)")
    for city, data in MARKET_FACTS.items():
        print(f"\n  {city}")
        print(f"    Outlook        : {data['overall_outlook'][:60]}")
        print(f"    5yr CAGR       : {data['avg_appreciation_5yr_pct']}%")
        print(f"    Rental yield   : {data['avg_rental_yield_pct']}%")
        print(f"    Liquidity      : {data['liquidity_score']}/5")
        print(f"    Top catalyst   : {data['catalysts'][0]}")
        if data["risk_factors"]:
            print(f"    Watch out      : {data['risk_factors'][0]}")

    print(f"\n📰 RBI WATCH ({len(RBI_WATCH)} events)")
    for event in RBI_WATCH:
        print(f"\n  [{event['date']}] {event['event']}")
        print(f"    Impact : {event['impact'][:80]}")
        print(f"    Action : {event['action'][:80]}")

    print(f"\n📋 MY INVESTMENT RULES ({len(MY_RULES)} rules)")
    for i, rule in enumerate(MY_RULES, 1):
        print(f"  {i}. {rule}")

    print("\n" + "=" * 65)
    print("  To add a seminar: add a dict to SEMINARS[]")
    print("  To add market data: add a key to MARKET_FACTS{}")
    print("  To log an RBI event: add a dict to RBI_WATCH[]")
    print("=" * 65)
