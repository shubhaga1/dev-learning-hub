"""
Step 5: Portfolio View — Full Picture Across All Properties
============================================================
MIT Principle: Never look at one property in isolation.
Portfolio-level risk is what kills you — not a single bad property.

Run: python3 05_portfolio_view.py
"""

from my_properties import MY_PROPERTIES

def portfolio_view(properties: list):
    print("\n" + "=" * 65)
    print("  REAL ESTATE PORTFOLIO DASHBOARD")
    print("=" * 65)

    # ── Totals ────────────────────────────────────────────────────────
    total_invested       = sum(p.facts.purchase_price_lakh + p.facts.registration_cost for p in properties)
    total_current_value  = sum(p.yield_data.current_value_lakh for p in properties)
    total_unrealized_gain= total_current_value - total_invested
    total_monthly_emi    = sum(p.finance.emi_monthly for p in properties) / 100_000  # in lakh
    total_monthly_rent   = sum(p.yield_data.monthly_rent for p in properties) / 100_000
    total_loan           = sum(p.finance.loan_amount_lakh - p.finance.principal_repaid_lakh for p in properties)

    print(f"""
  PORTFOLIO SNAPSHOT
  ──────────────────────────────────────────────────────
  Total Invested (cost)     : ₹{total_invested:.1f}L
  Total Current Value       : ₹{total_current_value:.1f}L
  Unrealized Gain           : ₹{total_unrealized_gain:.1f}L  ({total_unrealized_gain/total_invested*100:.1f}% overall)
  Outstanding Loan           : ₹{total_loan:.1f}L
  Net Equity (value - loan) : ₹{total_current_value - total_loan:.1f}L

  MONTHLY CASH FLOW
  ──────────────────────────────────────────────────────
  Total EMI outflow         : ₹{total_monthly_emi:.2f}L / month
  Total Rental income       : ₹{total_monthly_rent:.2f}L / month
  Net monthly RE burn       : ₹{total_monthly_emi - total_monthly_rent:.2f}L / month  {"✓ positive carry" if total_monthly_rent >= total_monthly_emi else "✗ you top up every month"}
    """)

    # ── Concentration Risk (MIT core concept) ─────────────────────────
    print("  CONCENTRATION RISK  (MIT: diversification = free lunch)")
    print("  ──────────────────────────────────────────────────────")
    city_exposure = {}
    for p in properties:
        city = p.facts.city
        city_exposure[city] = city_exposure.get(city, 0) + p.yield_data.current_value_lakh

    for city, val in sorted(city_exposure.items(), key=lambda x: -x[1]):
        pct = val / total_current_value * 100 if total_current_value else 0
        bar = "█" * int(pct / 5)
        flag = "⚠ concentrated" if pct > 40 else "✓"
        print(f"  {city:<12} ₹{val:>6.1f}L  {pct:>5.1f}%  {bar} {flag}")

    # ── Property Ranking — best to worst ──────────────────────────────
    print("\n  PROPERTY RANKING  (by gross rental yield)")
    print("  ──────────────────────────────────────────────────────")
    print(f"  {'#':<3} {'Property':<30} {'Yield':>7} {'Cover':>7} {'Gain%':>7} {'Decision'}")
    print(f"  {'-'*3} {'-'*30} {'-'*7} {'-'*7} {'-'*7} {'-'*10}")

    ranked = sorted(properties, key=lambda p: p.yield_data.gross_rental_yield_pct, reverse=True)
    for i, p in enumerate(ranked, 1):
        emi_cover = p.yield_data.monthly_rent / p.finance.emi_monthly if p.finance.emi_monthly else 0
        name_short = p.facts.name[:28]
        print(f"  {i:<3} {name_short:<30} {p.yield_data.gross_rental_yield_pct:>6.2f}%"
              f" {emi_cover:>6.2f}x {p.yield_data.appreciation_pct:>6.1f}%  {p.signals.current_decision}")

    # ── MIT Gain-Loss Analysis ─────────────────────────────────────────
    print("\n  MIT GAIN-LOSS ANALYSIS  (bull / base / bear across portfolio)")
    print("  ──────────────────────────────────────────────────────")
    port_bull = sum(p.risk.bull_case_value_lakh for p in properties)
    port_base = sum(p.risk.base_case_value_lakh for p in properties)
    port_bear = sum(p.risk.bear_case_value_lakh for p in properties)
    print(f"  Bull case (5yr)   : ₹{port_bull:.1f}L  (+{(port_bull-total_invested)/total_invested*100:.0f}%)")
    print(f"  Base case (5yr)   : ₹{port_base:.1f}L  (+{(port_base-total_invested)/total_invested*100:.0f}%)")
    print(f"  Bear case (5yr)   : ₹{port_bear:.1f}L  ({(port_bear-total_invested)/total_invested*100:.0f}%)")
    if port_base > 0:
        gain = port_base - total_invested
        loss = total_invested - port_bear
        gl_ratio = gain / loss if loss > 0 else 99
        print(f"  Gain-Loss ratio   : {gl_ratio:.1f}x  {'✓ good (>2x)' if gl_ratio >= 2 else '✗ asymmetry too low'}")

    # ── Action Items ──────────────────────────────────────────────────
    print("\n  ACTION ITEMS")
    print("  ──────────────────────────────────────────────────────")
    for p in properties:
        if p.signals.current_decision == "SELL":
            print(f"  🔴 SELL  : {p.facts.name} — {p.signals.decision_reason}")
        elif p.signals.current_decision == "REFINANCE":
            print(f"  🔵 REFI  : {p.facts.name} — {p.signals.decision_reason}")
        elif p.yield_data.gross_rental_yield_pct < 2 and p.yield_data.monthly_rent > 0:
            print(f"  🟡 WATCH : {p.facts.name} — yield {p.yield_data.gross_rental_yield_pct:.1f}% < 2%, consider selling")
        else:
            print(f"  🟢 HOLD  : {p.facts.name}")

    # ── MIT Rebalancing Alert ─────────────────────────────────────────
    print("\n  MIT REBALANCING CHECK")
    print("  ──────────────────────────────────────────────────────")
    re_concentration = 100  # 100% RE since this is the RE portfolio
    print(f"  Real Estate as % of total net worth: fill in 01_my_profile.py")
    print(f"  MIT rule: No single asset class > 30-40% of total portfolio")
    print(f"  If RE > 50% of net worth → stop buying, start investing in equity")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    portfolio_view(MY_PROPERTIES)
