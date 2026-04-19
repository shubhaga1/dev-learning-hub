# ============================================================
# CLEAN CODE — Naming
#
# Rule: A good function name eliminates the need to
#       read its implementation.
#
# SECTIONS:
#   1. Functions should use verbs
#   2. Variables should use nouns
#   3. Avoid ambiguous / shortened names
#   4. Avoid overly verbose names
#   5. Natural language style
#   6. Consistency — same concept, same word
#   7. One function = one responsibility
#   8. Argument clarity
#   9. Misleading names (most dangerous)
#  10. Mental model: verb + object + qualifier
# ============================================================


# ============================================================
# 1. FUNCTIONS = VERBS  |  VARIABLES = NOUNS
# ============================================================
print("1. FUNCTIONS = VERBS | VARIABLES = NOUNS")
print("="*50)

# ❌ Bad — function named like a noun, unclear what it does
def total(items):
    return sum(item["price"] for item in items)

# ✅ Good — verb makes it obvious: this calculates something
def calculate_total(items):
    return sum(item["price"] for item in items)

# ❌ Bad — variable named like an action
process_data = [{"price": 10}, {"price": 20}]

# ✅ Good — noun, describes what the data is
orders = [{"price": 10}, {"price": 20}]

print(f"  calculate_total(orders) = {calculate_total(orders)}")
print()


# ============================================================
# 2. AMBIGUOUS / SHORTENED NAMES
# ============================================================
print("2. AMBIGUOUS NAMES")
print("="*50)

# ❌ Bad — what does inc mean? increment? increase? include?
def inc(x):
    return x + 1

# ✅ Good — no ambiguity
def increment_count(count):
    return count + 1

# ❌ Bad — d, m could mean anything
d = 30
m = 12

# ✅ Good — self-documenting
days_in_month   = 30
month_number    = 12

print(f"  increment_count(5) = {increment_count(5)}")
print()


# ============================================================
# 3. OVERLY VERBOSE NAMES
# ============================================================
print("3. OVERLY VERBOSE NAMES")
print("="*50)

# ❌ Bad — verbose, adds noise
def get_absolute_difference_of_two_numbers(a, b):
    return abs(a - b)

# ✅ Good — clear, nothing wasted
def absolute_difference(a, b):
    return abs(a - b)

print(f"  absolute_difference(10, 3) = {absolute_difference(10, 3)}")
print()


# ============================================================
# 4. NATURAL LANGUAGE STYLE
# Code should read like a sentence
# ============================================================
print("4. NATURAL LANGUAGE STYLE")
print("="*50)

class Order:
    def __init__(self):
        self.items = []

    # ❌ Bad — argument order unclear: what is 8? what is 1?
    def insert(self, value, index):
        self.items.insert(index, value)

    # ✅ Good — reads like a sentence
    def insert_item(self, item, at_index):
        self.items.insert(at_index, item)

    # ✅ Good — subject.verb(object) pattern
    def add_item(self, product):
        self.items.append(product)

order = Order()
order.add_item("MacBook")
order.insert_item("AirPods", at_index=0)
print(f"  order.items = {order.items}")
print()


# ============================================================
# 5. CONSISTENCY — same concept, same word everywhere
# ============================================================
print("5. CONSISTENCY")
print("="*50)

class ShoppingCart:

    def __init__(self):
        self.items = []

    # ❌ Bad — mixing add and append for the same operation
    def add(self, item):       # used here
        self.items.append(item)

    def append_item(self, item):  # also used elsewhere — confusing!
        self.items.append(item)

    # ✅ Good — pick ONE word and use it everywhere
    def append(self, item):
        self.items.append(item)

    def remove(self, item):      # consistent: append/remove (not add/delete)
        self.items.remove(item)

cart = ShoppingCart()
cart.append("iPhone")
cart.append("Case")
cart.remove("Case")
print(f"  cart.items = {cart.items}")
print()


# ============================================================
# 6. ONE FUNCTION = ONE RESPONSIBILITY
# Don't mix: validation + state change + return result
# ============================================================
print("6. ONE RESPONSIBILITY PER FUNCTION")
print("="*50)

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items    = []

    # ❌ Bad — does three things: checks capacity, adds item, returns bool
    # The name "add" implies mutation — returning bool is unexpected
    def add(self, item):
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    # ✅ Good — split into clear, single-purpose functions
    def is_full(self):
        return len(self.items) >= self.capacity

    def add_item(self, item):
        self.items.append(item)

    def add_if_possible(self, item):
        if not self.is_full():
            self.add_item(item)
            return True
        return False

inv = Inventory(capacity=2)
print(f"  is_full = {inv.is_full()}")
print(f"  add_if_possible('TV')     = {inv.add_if_possible('TV')}")
print(f"  add_if_possible('Fridge') = {inv.add_if_possible('Fridge')}")
print(f"  add_if_possible('Laptop') = {inv.add_if_possible('Laptop')}  (full)")
print()


# ============================================================
# 7. MISLEADING NAMES — most dangerous in production
# ============================================================
print("7. MISLEADING NAMES (most dangerous)")
print("="*50)

# ❌ Bad — "add" sounds like it always mutates the list
#         but it actually returns True/False → misleading!
def add_payment(payments, payment):
    if payment["amount"] > 0:
        payments.append(payment)
        return True
    return False

# ✅ Good — name signals the conditional nature
def try_add_payment(payments, payment):
    if payment["amount"] > 0:
        payments.append(payment)
        return True
    return False

# ✅ Also good — separate the check from the action
def is_valid_payment(payment):
    return payment["amount"] > 0

def record_payment(payments, payment):
    payments.append(payment)

payments = []
payment  = {"amount": 500, "method": "card"}

if is_valid_payment(payment):
    record_payment(payments, payment)

print(f"  payments = {payments}")
print()


# ============================================================
# 8. MENTAL MODEL — before naming any function, ask:
#
#   1. What does it do?    → verb
#   2. What exactly?       → object
#   3. Any condition?      → qualifier
#
#   verb + object + qualifier
#   fetch + User  + ById    → fetch_user_by_id(id)
#   is   + Order + Eligible → is_order_eligible(order)
#   add  + Item  + IfPossible → add_item_if_possible(item)
# ============================================================
print("8. MENTAL MODEL: verb + object + qualifier")
print("="*50)

def fetch_user_by_id(user_id):
    return {"id": user_id, "name": "Shubham"}

def is_order_eligible(order):
    return order.get("amount", 0) > 100

def send_notification_if_pending(user, notification):
    if notification.get("status") == "pending":
        print(f"  [notify] Sending to {user['name']}: {notification['message']}")

user         = fetch_user_by_id(42)
order        = {"amount": 250}
notification = {"status": "pending", "message": "Your order shipped!"}

print(f"  fetch_user_by_id(42)          = {user}")
print(f"  is_order_eligible(order)      = {is_order_eligible(order)}")
send_notification_if_pending(user, notification)

print("""
─────────────────────────────────────────────
✅ SUMMARY — Clean Naming Rules

  ✅ Functions = verbs    (calculate, fetch, is, send)
  ✅ Variables = nouns    (orders, user, payment)
  ✅ Natural language     (order.add_item(product))
  ✅ One responsibility   (is_full / add_item, not add)
  ✅ Consistent vocab     (append/remove, not add+append+insert)
  ✅ No misleading names  (try_add vs add when it can fail)
  ✅ Argument clarity     (at_index=0, not just 0)

  ❌ Avoid: inc, foo, doStuff, get (everywhere), d, m
  ❌ Avoid: mixing add+append for the same concept
  ❌ Avoid: functions that validate + mutate + return bool
─────────────────────────────────────────────
""")
