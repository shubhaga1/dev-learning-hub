"""
Step 4: Your Properties — Fill Real Data Here
===============================================
Add one Property block per property you own.
Run: python3 04_my_properties.py
"""

from datetime import date
from property_schema import (
    Property, PropertyFacts, FinancialPlan,
    YieldMetrics, MarketIntelligence, RiskMetrics, DecisionSignals
)

# ─────────────────────────────────────────────────────────
# ADD YOUR PROPERTIES BELOW
# Copy a block, change the values, add to MY_PROPERTIES list
# ─────────────────────────────────────────────────────────

P001 = Property(
    facts=PropertyFacts(
        property_id="P001", name="Property 1 — Noida",
        city="Noida", micro_market="Sector ???", property_type="Apartment",
        size_sqft=0, bedrooms=0, status="Rented | Under Construction | Self-use",
        purchase_date=date(2020, 1, 1), purchase_price_lakh=0.0,
        registration_cost=0.0, builder="", rera_id=""
    ),
    finance=FinancialPlan(
        loan_amount_lakh=0.0, interest_rate_pct=0.0,
        loan_tenure_years=0, emi_monthly=0,
        down_payment_lakh=0.0, emi_paid_count=0, principal_repaid_lakh=0.0
    ),
    yield_data=YieldMetrics(
        current_value_lakh=0.0, last_valued_date=date(2025, 1, 1),
        monthly_rent=0, vacancy_months_ytd=0,
        purchase_price_lakh=0.0
    ),
    market=MarketIntelligence(
        metro_connectivity_score=0, airport_proximity_score=0,
        highway_score=0, school_hospital_score=0,
        it_hub_proximity_score=0, employment_diversity_score=0,
        new_supply_pressure="Medium", demand_driver="",
        seminar_insights=[]
    ),
    risk=RiskMetrics(
        liquidity_score=0,
        bull_case_value_lakh=0.0, base_case_value_lakh=0.0, bear_case_value_lakh=0.0,
        target_sell_price_lakh=0.0, exit_trigger="", hold_until=None
    ),
    signals=DecisionSignals(
        rbi_repo_rate_pct=6.5, home_loan_rate_pct=8.75,
        city_price_index_yoy=0.0, rental_index_yoy=0.0,
        current_decision="HOLD", decision_reason="", next_review_date=None
    )
)

P002 = Property(
    facts=PropertyFacts(
        property_id="P002", name="Property 2 — Bangalore",
        city="Bangalore", micro_market="", property_type="Apartment",
        size_sqft=0, bedrooms=0, status="",
        purchase_date=date(2020, 1, 1), purchase_price_lakh=0.0,
        registration_cost=0.0, builder="", rera_id=""
    ),
    finance=FinancialPlan(
        loan_amount_lakh=0.0, interest_rate_pct=0.0,
        loan_tenure_years=0, emi_monthly=0,
        down_payment_lakh=0.0, emi_paid_count=0, principal_repaid_lakh=0.0
    ),
    yield_data=YieldMetrics(
        current_value_lakh=0.0, last_valued_date=date(2025, 1, 1),
        monthly_rent=0, vacancy_months_ytd=0,
        purchase_price_lakh=0.0
    ),
    market=MarketIntelligence(
        metro_connectivity_score=0, airport_proximity_score=0,
        highway_score=0, school_hospital_score=0,
        it_hub_proximity_score=0, employment_diversity_score=0,
        new_supply_pressure="", demand_driver="",
        seminar_insights=[]
    ),
    risk=RiskMetrics(
        liquidity_score=0,
        bull_case_value_lakh=0.0, base_case_value_lakh=0.0, bear_case_value_lakh=0.0,
        target_sell_price_lakh=0.0, exit_trigger="", hold_until=None
    ),
    signals=DecisionSignals(
        rbi_repo_rate_pct=6.5, home_loan_rate_pct=8.75,
        city_price_index_yoy=0.0, rental_index_yoy=0.0,
        current_decision="HOLD", decision_reason="", next_review_date=None
    )
)

P003 = Property(
    facts=PropertyFacts(
        property_id="P003", name="Property 3 — Gurgaon",
        city="Gurgaon", micro_market="", property_type="Apartment",
        size_sqft=0, bedrooms=0, status="",
        purchase_date=date(2020, 1, 1), purchase_price_lakh=0.0,
        registration_cost=0.0, builder="", rera_id=""
    ),
    finance=FinancialPlan(
        loan_amount_lakh=0.0, interest_rate_pct=0.0,
        loan_tenure_years=0, emi_monthly=0,
        down_payment_lakh=0.0, emi_paid_count=0, principal_repaid_lakh=0.0
    ),
    yield_data=YieldMetrics(
        current_value_lakh=0.0, last_valued_date=date(2025, 1, 1),
        monthly_rent=0, vacancy_months_ytd=0,
        purchase_price_lakh=0.0
    ),
    market=MarketIntelligence(
        metro_connectivity_score=0, airport_proximity_score=0,
        highway_score=0, school_hospital_score=0,
        it_hub_proximity_score=0, employment_diversity_score=0,
        new_supply_pressure="", demand_driver="",
        seminar_insights=[]
    ),
    risk=RiskMetrics(
        liquidity_score=0,
        bull_case_value_lakh=0.0, base_case_value_lakh=0.0, bear_case_value_lakh=0.0,
        target_sell_price_lakh=0.0, exit_trigger="", hold_until=None
    ),
    signals=DecisionSignals(
        rbi_repo_rate_pct=6.5, home_loan_rate_pct=8.75,
        city_price_index_yoy=0.0, rental_index_yoy=0.0,
        current_decision="HOLD", decision_reason="", next_review_date=None
    )
)

P004 = Property(
    facts=PropertyFacts(
        property_id="P004", name="Property 4 — Mumbai",
        city="Mumbai", micro_market="", property_type="Apartment",
        size_sqft=0, bedrooms=0, status="",
        purchase_date=date(2020, 1, 1), purchase_price_lakh=0.0,
        registration_cost=0.0, builder="", rera_id=""
    ),
    finance=FinancialPlan(
        loan_amount_lakh=0.0, interest_rate_pct=0.0,
        loan_tenure_years=0, emi_monthly=0,
        down_payment_lakh=0.0, emi_paid_count=0, principal_repaid_lakh=0.0
    ),
    yield_data=YieldMetrics(
        current_value_lakh=0.0, last_valued_date=date(2025, 1, 1),
        monthly_rent=0, vacancy_months_ytd=0,
        purchase_price_lakh=0.0
    ),
    market=MarketIntelligence(
        metro_connectivity_score=0, airport_proximity_score=0,
        highway_score=0, school_hospital_score=0,
        it_hub_proximity_score=0, employment_diversity_score=0,
        new_supply_pressure="", demand_driver="",
        seminar_insights=[]
    ),
    risk=RiskMetrics(
        liquidity_score=0,
        bull_case_value_lakh=0.0, base_case_value_lakh=0.0, bear_case_value_lakh=0.0,
        target_sell_price_lakh=0.0, exit_trigger="", hold_until=None
    ),
    signals=DecisionSignals(
        rbi_repo_rate_pct=6.5, home_loan_rate_pct=8.75,
        city_price_index_yoy=0.0, rental_index_yoy=0.0,
        current_decision="HOLD", decision_reason="", next_review_date=None
    )
)

# ─────────────────────────────────────────────────────────
# REGISTER ALL YOUR PROPERTIES HERE
# ─────────────────────────────────────────────────────────

MY_PROPERTIES = [P001, P002, P003, P004]

if __name__ == "__main__":
    print(f"Portfolio: {len(MY_PROPERTIES)} properties loaded\n")
    for p in MY_PROPERTIES:
        p.summary()
