"""
LEVEL 3 — Magic Numbers & Hard-coded Values
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

def get_user_tier(points: int) -> str:
    if points >= 10000:
        return "platinum"
    elif points >= 5000:
        return "gold"
    elif points >= 1000:
        return "silver"
    return "bronze"

def calculate_reward(points: int) -> float:
    return points * 0.05

def is_session_expired(last_active_seconds: int) -> bool:
    return last_active_seconds > 1800


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] 10000, 5000, 1000 — what are these? If product changes tiers, you hunt every number.
[L2] 0.05 — is this 5%? A tax rate? A conversion factor? Name it.
[L3] 1800 — seconds? minutes? 1800 seconds = 30 min. Reader must calculate in head.
[L4] Magic numbers make diffs unreadable: -    if points >= 10000 / +    if points >= 8000
     WHY was this changed? Named constants force a decision at the definition site.
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

PLATINUM_THRESHOLD = 10_000
GOLD_THRESHOLD     = 5_000
SILVER_THRESHOLD   = 1_000

REWARD_RATE_PER_POINT = 0.05  # 5 paise per point

SESSION_TIMEOUT_SECONDS = 30 * 60  # 30 minutes

def get_user_tier(points: int) -> str:
    if points >= PLATINUM_THRESHOLD: return "platinum"
    if points >= GOLD_THRESHOLD:     return "gold"
    if points >= SILVER_THRESHOLD:   return "silver"
    return "bronze"

def calculate_reward(points: int) -> float:
    return points * REWARD_RATE_PER_POINT

def is_session_expired(last_active_seconds: int) -> bool:
    return last_active_seconds > SESSION_TIMEOUT_SECONDS


# ─────────────────────────────────────────────────────────
# 🧪 TEST
# ─────────────────────────────────────────────────────────

print(get_user_tier(7500))              # gold
print(calculate_reward(200))            # 10.0
print(is_session_expired(2000))         # True (2000 > 1800)
