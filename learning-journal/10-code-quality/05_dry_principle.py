"""
LEVEL 5 — DRY: Don't Repeat Yourself (Non-redundancy)
Duplicate code = duplicate bugs. If you change one, you must remember to change all.
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

def get_employee_bonus(salary, years):
    if years >= 10:
        bonus = salary * 0.20
    elif years >= 5:
        bonus = salary * 0.10
    else:
        bonus = salary * 0.05
    return round(bonus, 2)

def get_contractor_bonus(rate, years):
    if years >= 10:
        bonus = rate * 0.20
    elif years >= 5:
        bonus = rate * 0.10
    else:
        bonus = rate * 0.05
    return round(bonus, 2)

def get_intern_bonus(stipend, years):
    if years >= 10:
        bonus = stipend * 0.20
    elif years >= 5:
        bonus = stipend * 0.10
    else:
        bonus = stipend * 0.05
    return round(bonus, 2)


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] Same bonus logic copy-pasted 3 times. If the rate changes to 25%, you update 3 places.
[L2] Risk: you update employee and contractor but forget intern. Now they diverge silently.
[L3] The difference between the 3 functions is only the variable name (salary/rate/stipend).
     That means they're the same function — just extract it.
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

BONUS_RATES = {
    "senior": 0.20,   # 10+ years
    "mid":    0.10,   # 5-9 years
    "junior": 0.05,   # <5 years
}

def get_experience_tier(years: int) -> str:
    if years >= 10: return "senior"
    if years >= 5:  return "mid"
    return "junior"

def calculate_bonus(base_pay: float, years: int) -> float:
    tier = get_experience_tier(years)
    return round(base_pay * BONUS_RATES[tier], 2)

# All three types now use the same logic
employee_bonus   = calculate_bonus(salary=80000,   years=7)
contractor_bonus = calculate_bonus(base_pay=500,   years=12)
intern_bonus     = calculate_bonus(base_pay=15000, years=1)


# ─────────────────────────────────────────────────────────
# 🧪 TEST
# ─────────────────────────────────────────────────────────

print("Employee  bonus:", employee_bonus)    # 8000.0 (10%)
print("Contractor bonus:", contractor_bonus) # 100.0  (20%)
print("Intern    bonus:", intern_bonus)      # 750.0  (5%)
