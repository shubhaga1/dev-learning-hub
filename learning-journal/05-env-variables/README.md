# 05 — Environment Variables

## What you learn here
- `os.environ` — reads env vars, crashes if missing
- `os.getenv` — reads env vars safely, returns None or default
- `.env` file — store secrets locally, never commit to GitHub
- `python-dotenv` — loads `.env` file into `os.environ`
- Best practice — validate all required keys at startup

## Prerequisites
```bash
pip install python-dotenv
```

## Run order
```bash
python 01_env_demo.py
```

## Key concepts

### os.environ vs os.getenv
```python
os.environ["KEY"]              # crashes if missing ❌
os.getenv("KEY")               # returns None if missing ✅
os.getenv("KEY", "default")    # returns default if missing ✅
```

### .env file
```
PINECONE_API_KEY=your-key
HF_TOKEN=your-token
```
```python
from dotenv import load_dotenv
load_dotenv()  # loads .env → available via os.getenv()
```

### IMPORTANT — never commit .env to GitHub
Add to `.gitignore`:
```
.env
```
