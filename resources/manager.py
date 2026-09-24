"""Resource-aware planning without performing resource acquisition."""
from __future__ import annotations

import os
import shutil


def snapshot() -> dict:
    return {
        "cpu_count": os.cpu_count() or 1,
        "disk_free_bytes": shutil.disk_usage(".").free,
        "environment": {"github_actions": bool(os.getenv("GITHUB_ACTIONS")), "github_token_present": bool(os.getenv("GITHUB_TOKEN"))},
    }


def can_afford(requirements: dict, resources: dict | None = None) -> tuple[bool, list[str]]:
    resources = resources or snapshot()
    missing = []
    if requirements.get("github_token") and not resources["environment"]["github_token_present"]:
        missing.append("github_token")
    if requirements.get("min_cpu", 0) > resources["cpu_count"]:
        missing.append("min_cpu")
    if requirements.get("min_disk_free_bytes", 0) > resources["disk_free_bytes"]:
        missing.append("min_disk_free_bytes")
    return not missing, missing
