"""
LEVEL 2 — Single Responsibility Principle
Function does ONE thing. If you can describe it with "and", split it.
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

def process_order(order):
    # validate
    if not order.get("items"):
        print("No items")
        return
    if not order.get("address"):
        print("No address")
        return

    # calculate total
    total = 0
    for item in order["items"]:
        total += item["price"] * item["qty"]

    # apply discount
    if total > 500:
        total = total * 0.9

    # save to DB
    print(f"Saving order to DB: total={total}")

    # send email
    print(f"Sending confirmation email to {order.get('email')}")

    return total


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] process_order does 5 things: validate, calculate, discount, save, email.
     A function named "process" is almost always an SRP violation.
[L2] Testing is painful — can't unit test discount logic without triggering DB + email.
[L3] If email service is down, the whole order fails including the save.
[L4] Each concern should change independently — email template, discount rules, DB schema.
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

def validate_order(order: dict) -> bool:
    return bool(order.get("items")) and bool(order.get("address"))

def calculate_total(items: list) -> float:
    return sum(item["price"] * item["qty"] for item in items)

def apply_bulk_discount(total: float, threshold: float = 500, rate: float = 0.1) -> float:
    return total * (1 - rate) if total > threshold else total

def save_order(order: dict, total: float):
    print(f"Saving order to DB: total={total}")  # replace with real DB call

def send_confirmation(email: str, total: float):
    print(f"Sending email to {email}: total={total}")  # replace with real email

def process_order(order: dict) -> float | None:
    if not validate_order(order):
        return None
    total = calculate_total(order["items"])
    total = apply_bulk_discount(total)
    save_order(order, total)
    send_confirmation(order.get("email", ""), total)
    return total


# ─────────────────────────────────────────────────────────
# 🧪 TEST
# ─────────────────────────────────────────────────────────

order = {
    "items":   [{"price": 300, "qty": 2}, {"price": 100, "qty": 1}],
    "address": "42 MG Road",
    "email":   "user@example.com"
}

print("Total:", process_order(order))
print("Discount only:", apply_bulk_discount(700))  # test in isolation ✓
