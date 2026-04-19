"""
Step 7: Live Market Data — Macro Signals for Better Decisions
==============================================================
Pulls real-time data to update your decision signals.

MIT: "Capital market assumptions change. Models must be updated with fresh data."

Data sources (free, no API key needed):
  - yfinance  : Sensex, Nifty, US markets, gold, USD/INR
  - RBI       : Repo rate (static — update from RBI.org.in)
  - News      : Headlines via RSS (no key needed)

Run: python3 07_news_fetch.py
"""

import yfinance as yf
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET

# ─────────────────────────────────────────────────────────
# 1. MARKET INDICATORS — live from yfinance
# ─────────────────────────────────────────────────────────

TICKERS = {
    "Nifty 50":          "^NSEI",
    "Sensex":            "^BSESN",
    "Nifty Realty":      "NIFTYREALTY.BO",   # RE sector index (BSE)
    "Gold (MCX)":        "GC=F",             # Gold futures
    "USD/INR":           "INR=X",
    "10Y Bond Yield":    "^TNX",             # US 10yr (proxy for global rates)
    "HDFC Bank":         "HDFCBANK.NS",      # proxy for home loan rates
    "Nifty Bank":        "^NSEBANK",
}

def fetch_market_data():
    print("\n📊 LIVE MARKET INDICATORS")
    print("-" * 55)
    print(f"  {'Index / Asset':<22} {'Price':>12} {'Change%':>10} {'Signal'}")
    print(f"  {'-'*22} {'-'*12} {'-'*10} {'-'*15}")

    for name, ticker in TICKERS.items():
        try:
            t    = yf.Ticker(ticker)
            info = t.fast_info
            price  = info.last_price
            prev   = info.previous_close
            chg    = ((price - prev) / prev * 100) if prev else 0
            arrow  = "▲" if chg >= 0 else "▼"
            signal = interpret_signal(name, chg)
            print(f"  {name:<22} {price:>12,.2f} {arrow}{abs(chg):>8.2f}%  {signal}")
        except Exception as e:
            print(f"  {name:<22} {'Error':>12}            {str(e)[:20]}")

def interpret_signal(name: str, chg_pct: float) -> str:
    if "Realty" in name:
        if chg_pct > 1:   return "✓ RE sector up"
        if chg_pct < -1:  return "✗ RE sector down"
        return "→ flat"
    if "Gold" in name:
        if chg_pct > 1:   return "⚠ fear in market"
        return "→ stable"
    if "USD" in name:
        if chg_pct > 0.5: return "⚠ INR weakening"
        return "→ stable"
    if "Bond" in name:
        if chg_pct > 0.1: return "⚠ global rates up → EMI risk"
        return "→ stable"
    return ""


# ─────────────────────────────────────────────────────────
# 2. REAL ESTATE PROXY — sector ETFs and REITs
# ─────────────────────────────────────────────────────────

REIT_TICKERS = {
    "Mindspace REIT":    "MINDSPACE.NS",
    "Embassy REIT":      "EMBASSY.NS",
    "Nexus REIT":        "NEXUSSELECT.BO",
    "Brookfield REIT":   "BIRET.NS",
}

def fetch_reit_data():
    print("\n🏢 INDIAN REITs — Listed RE (liquid alternative)")
    print("-" * 55)
    print(f"  {'REIT':<22} {'Price':>10} {'Change%':>10} {'Note'}")
    print(f"  {'-'*22} {'-'*10} {'-'*10} {'-'*15}")

    for name, ticker in REIT_TICKERS.items():
        try:
            t    = yf.Ticker(ticker)
            info = t.fast_info
            price  = info.last_price
            prev   = info.previous_close
            chg    = ((price - prev) / prev * 100) if prev else 0
            arrow  = "▲" if chg >= 0 else "▼"
            print(f"  {name:<22} {price:>10,.2f} {arrow}{abs(chg):>8.2f}%  7-8% yield, liquid")
        except Exception as e:
            print(f"  {name:<22} {'N/A':>10}            {str(e)[:20]}")


# ─────────────────────────────────────────────────────────
# 3. NEWS HEADLINES — real estate and macro via RSS
# ─────────────────────────────────────────────────────────

RSS_FEEDS = {
    "Economic Times — Real Estate": "https://economictimes.indiatimes.com/industry/services/property-/-cstruction/rssfeeds/13357270.cms",
    "Livemint — Property":          "https://www.livemint.com/rss/real-estate",
    "Moneycontrol — RE":            "https://www.moneycontrol.com/rss/realestate.xml",
}

def fetch_news(max_per_feed: int = 3):
    print("\n📰 REAL ESTATE NEWS HEADLINES")
    print("-" * 65)

    for source, url in RSS_FEEDS.items():
        print(f"\n  [{source}]")
        try:
            req  = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                tree = ET.parse(response)
            root  = tree.getroot()
            items = root.findall(".//item")[:max_per_feed]
            for item in items:
                title = item.findtext("title", "No title")
                pub   = item.findtext("pubDate", "")[:16]
                print(f"    [{pub}] {title[:80]}")
        except Exception as e:
            print(f"    Could not fetch: {str(e)[:50]}")


# ─────────────────────────────────────────────────────────
# 4. RBI RATES — static (update manually from rbi.org.in)
# ─────────────────────────────────────────────────────────

RBI_RATES = {
    "repo_rate_pct":       6.25,   # Last updated: Feb 2025
    "reverse_repo_pct":    3.35,
    "inflation_cpi_pct":   4.3,    # CPI Feb 2025
    "gdp_growth_pct":      6.8,    # FY2025 forecast
    "home_loan_rate_range": "8.35% - 9.25%",  # SBI to HDFC range
}

def show_rbi_rates():
    print("\n🏦 RBI MACRO RATES  (update from rbi.org.in after each MPC)")
    print("-" * 55)
    print(f"  Repo Rate             : {RBI_RATES['repo_rate_pct']}%")
    print(f"  Home Loan Rate Range  : {RBI_RATES['home_loan_rate_range']}")
    print(f"  CPI Inflation         : {RBI_RATES['inflation_cpi_pct']}%")
    print(f"  GDP Growth Forecast   : {RBI_RATES['gdp_growth_pct']}%")
    real_rate = RBI_RATES["repo_rate_pct"] - RBI_RATES["inflation_cpi_pct"]
    print(f"  Real Rate (repo-CPI)  : {real_rate:.2f}%  {'✓ positive — stable env' if real_rate > 0 else '⚠ negative — inflationary'}")


# ─────────────────────────────────────────────────────────
# 5. DECISION SUMMARY — what all data means for you
# ─────────────────────────────────────────────────────────

def decision_summary():
    print("\n🎯 WHAT THIS MEANS FOR YOUR PORTFOLIO")
    print("-" * 65)
    print("""
  MIT CROWDING CHECK:
    If everyone is buying RE in the same city → reduce or stop buying there.
    Check: Are your friends/colleagues also buying in same location? If yes — crowding risk.

  RATE CYCLE POSITIONING:
    Falling repo rate  → hold properties, prices will rise as EMI burden reduces for buyers
    Rising repo rate   → be cautious, buyer demand softens, prices stagnate

  REALTY INDEX SIGNAL:
    Nifty Realty up >10% YTD → RE sector in favour, good to hold
    Nifty Realty down >10%   → consider exiting low-yield properties

  REIT vs DIRECT:
    REIT yield 7-8% vs direct rental yield 2-3% → REITs win on income
    Direct RE wins on leverage + appreciation    → buy direct only in high-growth locations

  RULE TO FOLLOW (MIT sizing):
    High conviction city (BLR) + falling rates + strong employment → size up (buy more)
    Low conviction city + rising inventory + flat appreciation    → size down (sell)
    """)


# ─────────────────────────────────────────────────────────
# RUN ALL
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 65)
    print(f"  MARKET INTELLIGENCE REPORT — {datetime.now().strftime('%d %b %Y %H:%M')}")
    print("=" * 65)

    show_rbi_rates()
    fetch_market_data()
    fetch_reit_data()
    fetch_news()
    decision_summary()

    print("\n" + "=" * 65)
    print("  Run 05_portfolio_view.py next to see how these signals")
    print("  affect your specific properties.")
    print("=" * 65)
