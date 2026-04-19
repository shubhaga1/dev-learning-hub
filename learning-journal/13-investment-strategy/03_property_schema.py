"""
Real Estate Investment Tracker — Schema Design
================================================
MIT Principle: "Portfolio management is about hard facts, not intuition."

This file defines WHAT to capture for every property.
Run this to see a sample property card + portfolio summary.

Sections:
  A. Property Facts        — what you bought
  B. Financial Mechanics   — how you're paying
  C. Yield & Returns       — is it making money
  D. Market Intelligence   — why this location
  E. MIT Risk Metrics      — concentration, liquidity, gain-loss
  F. Decision Signals      — hold / sell / buy more
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import date

# ─────────────────────────────────────────────────────────
# A. PROPERTY FACTS — the basics
# ─────────────────────────────────────────────────────────

@dataclass
class PropertyFacts:
    # Identity
    property_id:         str          # P001, P002 ...
    name:                str          # "Godrej Palm Retreat, Noida Sec 150"
    city:                str          # Noida | Bangalore | Gurgaon | Mumbai
    micro_market:        str          # Sector 150 | Whitefield | Golf Course Ext | Powai
    property_type:       str          # Apartment | Villa | Plot | Commercial | REIT

    # Size & Status
    size_sqft:           float        # carpet area in sqft
    bedrooms:            int          # 2BHK, 3BHK etc
    status:              str          # Under Construction | Ready | Rented | Self-use
    possession_date:     Optional[date] = None  # actual or expected

    # Purchase
    purchase_date:       date         = field(default_factory=date.today)
    purchase_price_lakh: float        = 0.0     # total cost paid (inclusive all charges)
    registration_cost:   float        = 0.0     # stamp duty + registration (lakh)
    builder:             str          = ""
    rera_id:             str          = ""      # RERA registration number


# ─────────────────────────────────────────────────────────
# B. FINANCIAL MECHANICS — how you're paying
# ─────────────────────────────────────────────────────────

@dataclass
class FinancialPlan:
    # Loan
    loan_amount_lakh:    float        # principal borrowed
    interest_rate_pct:   float        # current rate e.g. 8.75
    loan_tenure_years:   int          # 20, 25 years
    emi_monthly:         float        # actual EMI in ₹
    loan_start_date:     Optional[date] = None

    # Own contribution
    down_payment_lakh:   float        = 0.0
    other_costs_lakh:    float        = 0.0    # interiors, parking, maintenance corpus

    # Computed
    @property
    def total_invested_lakh(self):
        return self.down_payment_lakh + self.other_costs_lakh + self.registration_cost_lakh

    registration_cost_lakh: float    = 0.0

    # Payment progress
    emi_paid_count:      int         = 0       # how many EMIs paid so far
    principal_repaid_lakh: float     = 0.0     # how much principal paid down


# ─────────────────────────────────────────────────────────
# C. YIELD & RETURNS — is this property earning?
# ─────────────────────────────────────────────────────────

@dataclass
class YieldMetrics:
    # Current value
    current_value_lakh:  float        # market value today (from broker / PropTiger)
    last_valued_date:    Optional[date] = None

    # Rental
    monthly_rent:        float        = 0.0    # ₹ per month (0 if vacant/self-use)
    vacancy_months_ytd:  float        = 0.0    # months vacant this year

    # Computed metrics (all auto-calculated)
    @property
    def gross_rental_yield_pct(self):
        if self.current_value_lakh == 0: return 0
        return (self.monthly_rent * 12) / (self.current_value_lakh * 1_00_000) * 100

    @property
    def net_rental_yield_pct(self):
        # subtract maintenance ~1% and vacancy loss
        annual_rent = self.monthly_rent * (12 - self.vacancy_months_ytd)
        annual_cost = self.current_value_lakh * 1_00_000 * 0.01
        return (annual_rent - annual_cost) / (self.current_value_lakh * 1_00_000) * 100

    @property
    def emi_coverage_ratio(self):
        """Rent / EMI. >1 = rent covers EMI. <1 = you're topping up."""
        return 0  # computed in portfolio view (needs EMI from FinancialPlan)

    # Capital appreciation
    purchase_price_lakh: float       = 0.0

    @property
    def appreciation_pct(self):
        if self.purchase_price_lakh == 0: return 0
        return (self.current_value_lakh - self.purchase_price_lakh) / self.purchase_price_lakh * 100

    @property
    def unrealized_gain_lakh(self):
        return self.current_value_lakh - self.purchase_price_lakh


# ─────────────────────────────────────────────────────────
# D. MARKET INTELLIGENCE — why this location will grow
# ─────────────────────────────────────────────────────────

@dataclass
class MarketIntelligence:
    # Infrastructure (score each 1-5)
    metro_connectivity_score:   int = 0   # 5 = metro within 500m
    airport_proximity_score:    int = 0   # 5 = <30 min drive
    highway_score:              int = 0   # 5 = expressway direct access
    school_hospital_score:      int = 0   # 5 = top schools + hospitals nearby

    # Employment
    it_hub_proximity_score:     int = 0   # 5 = Whitefield, Hinjewadi, Cyber City nearby
    employment_diversity_score: int = 0   # 5 = multiple employer types (not 1 company town)

    # Supply-Demand
    new_supply_pressure:        str = ""  # Low | Medium | High (new projects coming up)
    demand_driver:              str = ""  # IT expansion | Gov project | Airport | Sports city

    # Seminar / Research Notes
    seminar_insights:           list = field(default_factory=list)  # add notes from talks
    # e.g. ["MIT: Power law — location with one dominant employer is single-point risk",
    #        "PropTiger 2024: Noida Sec 150 has 40% unsold inventory — oversupply risk"]

    @property
    def location_score(self):
        return (self.metro_connectivity_score +
                self.airport_proximity_score  +
                self.highway_score            +
                self.school_hospital_score    +
                self.it_hub_proximity_score   +
                self.employment_diversity_score) / 30 * 100  # out of 100


# ─────────────────────────────────────────────────────────
# E. MIT RISK METRICS — portfolio-level thinking
# ─────────────────────────────────────────────────────────

@dataclass
class RiskMetrics:
    # MIT: Liquidity is existential risk
    liquidity_score:     int  = 0   # 1-5: 5 = can sell in 30 days, 1 = locked for years

    # MIT: Concentration risk
    # (computed at portfolio level — see 04_portfolio_view.py)

    # MIT: Gain-Loss thinking (not just Sharpe)
    bull_case_value_lakh:  float = 0.0   # what it could be worth in 5 years (optimistic)
    base_case_value_lakh:  float = 0.0   # realistic 5-year value
    bear_case_value_lakh:  float = 0.0   # if market drops 30%

    # Exit planning
    target_sell_price_lakh: float = 0.0  # your exit price
    exit_trigger:            str  = ""   # "When rent yield > 4%" / "Metro opens 2026" / "Fund child education 2030"
    hold_until:              Optional[date] = None


# ─────────────────────────────────────────────────────────
# F. DECISION SIGNALS — should you hold, sell, or buy more
# ─────────────────────────────────────────────────────────

@dataclass
class DecisionSignals:
    # Macro triggers to watch (updated when you run news fetch)
    rbi_repo_rate_pct:       float = 0.0   # impacts EMI and buyer affordability
    home_loan_rate_pct:      float = 0.0   # your actual lending rate
    city_price_index_yoy:    float = 0.0   # % price change in your micro-market YoY
    rental_index_yoy:        float = 0.0   # % rental change YoY

    # Your decision
    current_decision:        str  = "HOLD"  # HOLD | SELL | BUY MORE | REFINANCE
    decision_reason:         str  = ""
    next_review_date:        Optional[date] = None


# ─────────────────────────────────────────────────────────
# COMBINED PROPERTY RECORD
# ─────────────────────────────────────────────────────────

@dataclass
class Property:
    facts:      PropertyFacts
    finance:    FinancialPlan
    yield_data: YieldMetrics
    market:     MarketIntelligence
    risk:       RiskMetrics
    signals:    DecisionSignals

    def summary(self):
        emi_coverage = self.yield_data.monthly_rent / self.finance.emi_monthly if self.finance.emi_monthly else 0
        print(f"""
┌─────────────────────────────────────────────────────┐
  {self.facts.name}
  {self.facts.city} | {self.facts.micro_market} | {self.facts.property_type}
├─────────────────────────────────────────────────────┤
  Purchase     : ₹{self.facts.purchase_price_lakh:.1f}L   Current: ₹{self.yield_data.current_value_lakh:.1f}L
  Gain         : ₹{self.yield_data.unrealized_gain_lakh:.1f}L  ({self.yield_data.appreciation_pct:.1f}%)
  Monthly EMI  : ₹{self.finance.emi_monthly:,.0f}   Rent: ₹{self.yield_data.monthly_rent:,.0f}
  EMI Coverage : {emi_coverage:.2f}x  {"✓ rent covers EMI" if emi_coverage >= 1 else "✗ you top up every month"}
  Gross Yield  : {self.yield_data.gross_rental_yield_pct:.2f}%  {"✓ good" if self.yield_data.gross_rental_yield_pct >= 3 else "✗ below 3% — appreciation play only"}
  Location Score: {self.market.location_score:.0f}/100
  Decision     : {self.signals.current_decision} — {self.signals.decision_reason}
└─────────────────────────────────────────────────────┘""")


# ─────────────────────────────────────────────────────────
# SAMPLE PROPERTY — fill yours in 04_my_properties.py
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample = Property(
        facts=PropertyFacts(
            property_id="P001", name="Sample Flat, Noida Sec 150",
            city="Noida", micro_market="Sector 150", property_type="Apartment",
            size_sqft=1450, bedrooms=3, status="Rented",
            purchase_date=date(2020, 6, 1), purchase_price_lakh=85.0,
            registration_cost=5.5, builder="Godrej", rera_id="UPRERAPRJ12345"
        ),
        finance=FinancialPlan(
            loan_amount_lakh=60.0, interest_rate_pct=8.75,
            loan_tenure_years=20, emi_monthly=52_800,
            down_payment_lakh=25.0, emi_paid_count=58,
            principal_repaid_lakh=8.2
        ),
        yield_data=YieldMetrics(
            current_value_lakh=115.0, last_valued_date=date(2025, 1, 1),
            monthly_rent=22_000, vacancy_months_ytd=1.0,
            purchase_price_lakh=85.0
        ),
        market=MarketIntelligence(
            metro_connectivity_score=3, airport_proximity_score=2,
            highway_score=5, school_hospital_score=4,
            it_hub_proximity_score=2, employment_diversity_score=2,
            new_supply_pressure="High",
            demand_driver="Expressway + Sports City development",
            seminar_insights=[
                "MIT: Power law — dominant employer concentration = single point risk",
                "PropTiger 2024: Noida Sec 150 has 40% unsold inventory — oversupply pressure",
                "RBI 2024: Rate cut cycle expected — good for property demand"
            ]
        ),
        risk=RiskMetrics(
            liquidity_score=2,
            bull_case_value_lakh=160.0,
            base_case_value_lakh=130.0,
            bear_case_value_lakh=95.0,
            target_sell_price_lakh=150.0,
            exit_trigger="Metro line operational + appreciation > 75%",
            hold_until=date(2027, 6, 1)
        ),
        signals=DecisionSignals(
            rbi_repo_rate_pct=6.5, home_loan_rate_pct=8.75,
            city_price_index_yoy=8.2, rental_index_yoy=5.1,
            current_decision="HOLD",
            decision_reason="Appreciate to 130L target, review when metro opens",
            next_review_date=date(2025, 12, 1)
        )
    )
    sample.summary()

    print("\nCOLUMNS SUMMARY — what to fill for each property:")
    print("""
  FACTS      : id, name, city, micro-market, type, size, BHK, status,
               possession date, purchase date, price, reg cost, builder, RERA

  FINANCE    : loan amount, rate, tenure, EMI, down payment, other costs,
               EMIs paid, principal repaid

  YIELD      : current value, valuation date, monthly rent, vacancy months
               → auto-computes: gross yield, net yield, appreciation %, gain

  MARKET     : metro/airport/highway/school scores, IT hub score, supply pressure,
               demand driver, seminar notes (add any insight here)

  RISK       : liquidity score, bull/base/bear case values, exit price, exit trigger

  SIGNALS    : RBI rate, loan rate, city price index YoY, decision + reason
    """)
