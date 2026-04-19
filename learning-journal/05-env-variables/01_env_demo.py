import os
from dotenv import load_dotenv

# ============================================================
# PRINT ORDER:
#   1. STEP 1 — os.environ (crashes on missing key)
#   2. STEP 2 — os.getenv (safe, returns None)
#   3. STEP 3 — os.getenv with default value
#   4. STEP 4 — load from .env file using python-dotenv
#   5. STEP 5 — best practice (validate after loading)
# ============================================================


# ============================================================
# STEP 1: os.environ — crashes if key missing
# ============================================================
print("\n" + "="*50)
print("STEP 1: os.environ")
print("="*50)

# Reading a key that EXISTS in the system
path = os.environ["PATH"]  # PATH always exists on any machine
print(f"[os.environ] PATH = {path[:100]}...")  # first 50 chars

# Reading a MISSING key → KeyError crash
print("\n[os.environ] Trying to read MISSING_KEY...")
try:
    value = os.environ["MISSING_KEY"]
except KeyError as e:
    print(f"[os.environ] ❌ KeyError: {e} — crashes if key doesn't exist!")

input("\nPress Enter to go to STEP 2...\n")


# ============================================================
# STEP 2: os.getenv — safe, returns None if missing
# ============================================================
print("="*50)
print("STEP 2: os.getenv — no crash")
print("="*50)

# Key exists
path = os.getenv("PATH")
print(f"[os.getenv] PATH = {path[:50]}...")

# Key missing → returns None instead of crashing
missing = os.getenv("MISSING_KEY")
print(f"[os.getenv] MISSING_KEY = {missing}")  # prints None
print(f"[os.getenv] ✅ No crash! Returns None")

input("\nPress Enter to go to STEP 3...\n")


# ============================================================
# STEP 3: os.getenv with default value
# ============================================================
print("="*50)
print("STEP 3: os.getenv with default")
print("="*50)

# Key missing → returns your default instead of None
app_env = os.getenv("APP_ENV", "production")
print(f"[os.getenv] APP_ENV (not set yet) = '{app_env}'")
print(f"[os.getenv] ✅ Returns 'production' as default")

debug = os.getenv("DEBUG", "false")
print(f"[os.getenv] DEBUG (not set yet) = '{debug}'")

input("\nPress Enter to go to STEP 4...\n")


# ============================================================
# STEP 4: load .env file using python-dotenv
# .env file contains your secrets — never commit to GitHub!
# ============================================================
print("="*50)
print("STEP 4: Loading .env file")
print("="*50)

print("[dotenv] Before load_dotenv():")
print(f"  PINECONE_API_KEY = {os.getenv('PINECONE_API_KEY')}")  # None

load_dotenv()  # reads .env file → sets all vars in os.environ

print("\n[dotenv] After load_dotenv():")
print(f"  PINECONE_API_KEY = {os.getenv('PINECONE_API_KEY')}")  # now has value
print(f"  HF_TOKEN         = {os.getenv('HF_TOKEN')}")
print(f"  DB_PASSWORD      = {os.getenv('DB_PASSWORD')}")
print(f"  APP_ENV          = {os.getenv('APP_ENV')}")

input("\nPress Enter to go to STEP 5...\n")


# ============================================================
# STEP 5: Best practice — validate all required keys at startup
# Fail fast with a clear error instead of crashing later
# ============================================================
print("="*50)
print("STEP 5: Best practice — validate on startup")
print("="*50)

REQUIRED_KEYS = ["PINECONE_API_KEY", "HF_TOKEN", "DB_PASSWORD"]

def load_config():
    """
    Load and validate all required environment variables.
    Called once at app startup — fails fast if anything missing.
    """
    print("[load_config] Checking required environment variables...")
    config = {}
    missing = []

    for key in REQUIRED_KEYS:
        value = os.getenv(key)
        if not value:
            missing.append(key)
        else:
            config[key] = value
            print(f"  ✅ {key} = loaded")

    if missing:
        raise EnvironmentError(
            f"❌ Missing required environment variables: {', '.join(missing)}\n"
            f"   Add them to your .env file"
        )

    print("\n[load_config] ✅ All required keys loaded!")
    return config

try:
    config = load_config()
    print(f"\n[main] App starting with config: {list(config.keys())}")
except EnvironmentError as e:
    print(f"\n[main] {e}")

print("\n✅ Done!")
