"""
LEVEL 7 — Maintainability: Dependency Injection
Don't hardcode dependencies inside a class. Inject them from outside.
Makes code swappable, testable, and maintainable.
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()      # hardcoded — can't swap to Postgres
        self.emailer = GmailSender()   # hardcoded — can't swap to SendGrid
        self.logger = FileLogger()     # hardcoded — can't swap to CloudWatch

    def place_order(self, order):
        self.db.save(order)
        self.emailer.send(order["email"], "Order confirmed")
        self.logger.log(f"Order placed: {order}")

# Testing this requires a real MySQL DB + Gmail + filesystem — painful


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] OrderService creates its own dependencies — tightly coupled to specific implementations.
[L2] To test, you need real MySQL running. Unit test becomes integration test.
[L3] Switching from Gmail to SendGrid means editing OrderService — a class that should
     not care about email implementation details.
[L4] If DB constructor changes, OrderService breaks even though it didn't change.
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data: dict): pass

class EmailSender(ABC):
    @abstractmethod
    def send(self, to: str, message: str): pass

class Logger(ABC):
    @abstractmethod
    def log(self, message: str): pass

# Inject dependencies — OrderService doesn't care which DB, emailer, or logger is used
class OrderService:
    def __init__(self, db: Database, emailer: EmailSender, logger: Logger):
        self.db = db
        self.emailer = emailer
        self.logger = logger

    def place_order(self, order: dict):
        self.db.save(order)
        self.emailer.send(order["email"], "Order confirmed")
        self.logger.log(f"Order placed: {order}")

# ── Fake implementations for testing (no real DB, email, or files needed) ──

class InMemoryDatabase(Database):
    def __init__(self): self.store = []
    def save(self, data): self.store.append(data); print(f"[DB] Saved: {data}")

class ConsoleEmailSender(EmailSender):
    def send(self, to, message): print(f"[Email] To: {to} | {message}")

class ConsoleLogger(Logger):
    def log(self, message): print(f"[Log] {message}")


# ─────────────────────────────────────────────────────────
# 🧪 TEST — swap any component without touching OrderService
# ─────────────────────────────────────────────────────────

service = OrderService(
    db=InMemoryDatabase(),
    emailer=ConsoleEmailSender(),
    logger=ConsoleLogger()
)
service.place_order({"id": "ORD001", "email": "user@example.com", "total": 450})
