"""
LEVEL 6 — Scalability: Open/Closed Principle
Open for extension, closed for modification.
New features should not require editing existing working code.
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

def calculate_shipping(order_type: str, weight: float) -> float:
    if order_type == "standard":
        return weight * 5
    elif order_type == "express":
        return weight * 10
    elif order_type == "overnight":
        return weight * 20
    # Adding drone delivery requires editing THIS function — risky


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] Every new delivery type requires modifying calculate_shipping.
     You risk breaking existing types with every edit.
[L2] if/elif chains grow unboundedly. At 10 types it becomes a wall of conditions.
[L3] Can't test new types independently — must go through the same function.
[L4] Violates Open/Closed: class should be open for extension, closed for modification.
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

from abc import ABC, abstractmethod

class ShippingMethod(ABC):
    @abstractmethod
    def calculate(self, weight: float) -> float:
        pass

class StandardShipping(ShippingMethod):
    def calculate(self, weight: float) -> float:
        return weight * 5

class ExpressShipping(ShippingMethod):
    def calculate(self, weight: float) -> float:
        return weight * 10

class OvernightShipping(ShippingMethod):
    def calculate(self, weight: float) -> float:
        return weight * 20

# Adding drone delivery = new class, zero changes to existing code ✓
class DroneShipping(ShippingMethod):
    def calculate(self, weight: float) -> float:
        return weight * 2 + 50  # base fee + weight

def calculate_shipping(method: ShippingMethod, weight: float) -> float:
    return method.calculate(weight)


# ─────────────────────────────────────────────────────────
# 🧪 TEST
# ─────────────────────────────────────────────────────────

print(calculate_shipping(StandardShipping(), 3))   # 15.0
print(calculate_shipping(ExpressShipping(),  3))   # 30.0
print(calculate_shipping(DroneShipping(),    3))   # 56.0
