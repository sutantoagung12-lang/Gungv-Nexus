"""Read-only registry helpers for the Nexus GitHub operating layer."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "github" / "registry" / "repositories.json"
def load_registry():
    with REGISTRY.open(encoding="utf-8") as f: return json.load(f)
def repositories(): return load_registry()["repositories"]
def by_name(name): return next((r for r in repositories() if r["name"] == name), None)
