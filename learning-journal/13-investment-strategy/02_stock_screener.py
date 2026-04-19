"""
Step 2: Stock Screener — Pick Right Stocks
===========================================
MIT Lecture principles applied:
- Edge: only buy when you have a reason (not just gut)
- Sizing: allocate proportional to conviction and risk
- Gain-Loss thinking: upside must be 2x the downside

Scoring rubric: 10 criteria, max 100 points.
Buy if score >= 65. Strong buy if >= 80.

Run: python3 02_stock_screener.py
Requires: pip install yfinance
"""

import yfinance as yf

# ─────────────────────────────────────────────────────────
# SCORING CRITERIA (MIT: "ability to pick winners = your edge")
# ─────────────────────────────────────────────────────────

def score_stock(ticker: str) -> dict:
    print(f"\nFetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    info  = stock.info
    score = 0
    notes = []

    # 1. VALUATION — P/E ratio
    pe = info.get("trailingPE")
    if pe and pe < 20:
        score += 15; notes.append(f"✓ P/E {pe:.1f} < 20 (undervalued)")
    elif pe and pe < 35:
        score += 8;  notes.append(f"~ P/E {pe:.1f} fair valued")
    else:
        notes.append(f"✗ P/E {pe} high or unavailable")

    # 2. REVENUE GROWTH — last year
    rev_growth = info.get("revenueGrowth")
    if rev_growth and rev_growth > 0.15:
        score += 15; notes.append(f"✓ Revenue growth {rev_growth*100:.1f}% > 15%")
    elif rev_growth and rev_growth > 0.05:
        score += 8;  notes.append(f"~ Revenue growth {rev_growth*100:.1f}%")
    else:
        notes.append(f"✗ Revenue growth {rev_growth} low")

    # 3. PROFITABILITY — profit margin
    margin = info.get("profitMargins")
    if margin and margin > 0.15:
        score += 10; notes.append(f"✓ Profit margin {margin*100:.1f}% > 15%")
    elif margin and margin > 0.05:
        score += 5;  notes.append(f"~ Margin {margin*100:.1f}%")
    else:
        notes.append(f"✗ Thin margin {margin}")

    # 4. DEBT — debt to equity
    de = info.get("debtToEquity")
    if de is not None and de < 50:
        score += 10; notes.append(f"✓ Low debt D/E {de:.1f}")
    elif de is not None and de < 150:
        score += 5;  notes.append(f"~ Moderate debt D/E {de:.1f}")
    else:
        notes.append(f"✗ High debt D/E {de}")

    # 5. RETURN ON EQUITY — management quality
    roe = info.get("returnOnEquity")
    if roe and roe > 0.20:
        score += 10; notes.append(f"✓ ROE {roe*100:.1f}% > 20% (great management)")
    elif roe and roe > 0.10:
        score += 5;  notes.append(f"~ ROE {roe*100:.1f}%")
    else:
        notes.append(f"✗ Low ROE {roe}")

    # 6. FREE CASH FLOW — real earnings
    fcf = info.get("freeCashflow")
    if fcf and fcf > 0:
        score += 10; notes.append(f"✓ Positive FCF ₹{fcf/1e9:.1f}B")
    else:
        notes.append(f"✗ Negative or no FCF {fcf}")

    # 7. DIVIDEND — passive income bonus
    div_yield = info.get("dividendYield")
    if div_yield and div_yield > 0.02:
        score += 5; notes.append(f"✓ Dividend yield {div_yield*100:.1f}%")
    else:
        notes.append(f"  No/low dividend")

    # 8. MARKET CAP — stability
    mkt_cap = info.get("marketCap", 0)
    if mkt_cap > 1e11:
        score += 10; notes.append(f"✓ Large cap ₹{mkt_cap/1e9:.0f}B (stable)")
    elif mkt_cap > 1e10:
        score += 7;  notes.append(f"~ Mid cap")
    else:
        notes.append(f"~ Small cap (higher risk/reward)")

    # 9. SECTOR MOAT — simple check (manual input needed for deep analysis)
    sector = info.get("sector", "Unknown")
    moat_sectors = ["Technology", "Healthcare", "Consumer Defensive", "Financial Services"]
    if sector in moat_sectors:
        score += 10; notes.append(f"✓ Sector '{sector}' has moat potential")
    else:
        score += 5;  notes.append(f"~ Sector: {sector}")

    # 10. 52-WEEK POSITION — entry point
    current = info.get("currentPrice", 0)
    low_52  = info.get("fiftyTwoWeekLow", 0)
    high_52 = info.get("fiftyTwoWeekHigh", 1)
    position = (current - low_52) / (high_52 - low_52) if high_52 > low_52 else 0.5
    if position < 0.4:
        score += 5; notes.append(f"✓ Near 52W low ({position*100:.0f}% from low) — good entry")
    elif position < 0.7:
        notes.append(f"~ Mid range ({position*100:.0f}% from low)")
    else:
        notes.append(f"✗ Near 52W high ({position*100:.0f}% from low) — wait for dip")

    return {"ticker": ticker, "score": score, "notes": notes, "name": info.get("longName", ticker)}


def verdict(score: int) -> str:
    if score >= 80: return "STRONG BUY  ★★★"
    if score >= 65: return "BUY         ★★"
    if score >= 50: return "WATCH       ★"
    return            "SKIP        ✗"


# ─────────────────────────────────────────────────────────
# STOCKS TO SCREEN — edit this list
# ─────────────────────────────────────────────────────────

WATCHLIST = [
    "RELIANCE.NS",    # Reliance Industries
    "TCS.NS",         # TCS
    "INFY.NS",        # Infosys
    "HDFCBANK.NS",    # HDFC Bank
    "ASIANPAINT.NS",  # Asian Paints
    "AAPL",           # Apple (US)
    "MSFT",           # Microsoft (US)
    "GOOGL",          # Google (US)
]

if __name__ == "__main__":
    results = []
    for ticker in WATCHLIST:
        result = score_stock(ticker)
        results.append(result)

    print("\n" + "=" * 60)
    print("STOCK SCREENING RESULTS")
    print("=" * 60)
    results.sort(key=lambda x: x["score"], reverse=True)

    for r in results:
        print(f"\n{r['name']} ({r['ticker']})")
        print(f"Score: {r['score']}/100  →  {verdict(r['score'])}")
        for note in r["notes"]:
            print(f"  {note}")

    print("\n" + "=" * 60)
    print("MIT SIZING RULE: Allocate more to higher scores.")
    print("Never put >10% in a single stock (concentration risk).")
    print("Rebalance every 6 months or when allocation drifts >5%.")
