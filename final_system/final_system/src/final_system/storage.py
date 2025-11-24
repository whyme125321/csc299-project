import json
from pathlib import Path

# Get path to the data directory (one level above src)
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def load(name: str):
    """Load JSON file (tasks.json or pkms.json)."""
    file = DATA_DIR / name
    if not file.exists():
        return {}
    with open(file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save(name: str, data: dict):
    """Save Python dict to JSON file."""
    file = DATA_DIR / name
    with open(file, "w") as f:
        json.dump(data, f, indent=2)
