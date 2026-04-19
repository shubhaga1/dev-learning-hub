# 01 — Python Basics

## What you learn here
- Running Python scripts
- Lists — ordered, mutable, allows duplicates
- Dicts — key-value pairs, fast lookup
- Loops — iterate over data
- Search — find items by value

## Run order
```bash
python 01_hello_world.py      # start here
python 02_lists_and_dicts.py  # then this
```

## Key concepts

### List vs Dict
```python
# List — access by index
names = ["shubham", "rahul", "priya"]
names[0]  # "shubham"

# Dict — access by key
person = {"name": "shubham", "sal": 1000}
person["name"]  # "shubham"
```

### When to use which
| | List | Dict |
|--|--|--|
| Order matters | ✅ | ❌ |
| Fast lookup by key | ❌ | ✅ |
| Duplicates allowed | ✅ | ❌ (keys unique) |
