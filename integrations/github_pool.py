"""GitHub capability-pool loader for Nexus composition."""
from __future__ import annotations

import json
from pathlib import Path


POOL = Path(__file__).resolve().parent / "github-capability-pool.json"


def load_pool() -> dict:
    with POOL.open(encoding="utf-8") as fh:
        return json.load(fh)


def capabilities() -> list[dict]:
    return load_pool().get("repositories", [])
