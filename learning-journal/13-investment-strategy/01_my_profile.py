"""
Step 1: Define Your Investor Profile
======================================
Before picking any stock or property, answer these 5 questions.
MIT Lecture: "Portfolio management is about sizing relative to YOUR objectives and loss tolerance."

Fill in YOUR numbers below.
"""

# ─────────────────────────────────────────────────────────
# YOUR PROFILE — edit these
# ─────────────────────────────────────────────────────────

PROFILE = {
    "monthly_income_inr":   300_000,       # your take-home
    "monthly_expenses_inr": 120_000,       # rent + food + EMI + lifestyle
    "emergency_fund_months": 6,            # how many months of expenses kept in FD/cash
    "investment_horizon_years": 15,        # how long you can stay invested
    "max_loss_tolerance_pct": 30,          # max % loss you can sleep through (30 = 30%)
    "target_corpus_inr": 5_00_00_000,     # ₹5 Cr target
    "current_portfolio_inr": 50_00_000,   # what you have today
}

# ─────────────────────────────────────────────────────────
# ALLOCATION FRAMEWORK (Endowment Model adapted for India)
# ─────────────────────────────────────────────────────────
# MIT: Endowments target ~8% real return = 5% spending + inflation
# For India: target 12-15% CAGR to beat 6-7% inflation + generate wealth

ALLOCATION = {
    # Growth (high risk, high return)
    "Indian Equities — Large Cap Index (Nifty50)":    20,   # passive, low cost
    "Indian Equities — Mid/Small Cap":                15,   # higher return, higher vol
    "US Equities — S&P500 ETF (Motilal/Mirae)":      10,   # USD hedge + global exposure

    # Real Assets
    "Real Estate (1 property or REITs)":              20,   # inflation hedge, rental yield

    # Alternatives
    "Gold / Silver ETF":                               5,   # crisis hedge, negative correlation

    # Stable
    "Debt — Corporate Bonds / Nifty 100 Bonds ETF":  15,   # 7-8% steady, lower risk
    "PPF / EPF / NPS":                                10,   # tax-free, long lock-in

    # Liquid Buffer
    "Liquid Fund / FD (emergency + opportunity)":      5,   # redeploy on market crashes
}

# ─────────────────────────────────────────────────────────
# MONTHLY INVESTMENT PLAN
# ─────────────────────────────────────────────────────────

monthly_surplus = PROFILE["monthly_income_inr"] - PROFILE["monthly_expenses_inr"]
investable      = monthly_surplus * 0.80   # keep 20% as monthly buffer

print("=" * 50)
print("YOUR INVESTOR PROFILE SUMMARY")
print("=" * 50)
print(f"Monthly surplus    : ₹{monthly_surplus:,.0f}")
print(f"Investable/month   : ₹{investable:,.0f} (80% of surplus)")
print(f"Time horizon       : {PROFILE['investment_horizon_years']} years")
print(f"Max loss tolerated : {PROFILE['max_loss_tolerance_pct']}%")
print(f"Target corpus      : ₹{PROFILE['target_corpus_inr']:,.0f}")
print()
print("MONTHLY ALLOCATION PLAN:")
print("-" * 50)
for asset, pct in ALLOCATION.items():
    amount = investable * pct / 100
    print(f"  {pct:3}%  ₹{amount:>9,.0f}  →  {asset}")
print("-" * 50)
print(f"  100%  ₹{investable:>9,.0f}  TOTAL")
