"""Runtime availability detection for Nexus integrations.

The detector is intentionally conservative: availability means only that a
local dependency or environment capability is present. It never installs,
executes, or grants permissions.
"""
from __future__ import annotations

import importlib.util
import os
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CapabilityStatus:
    name: str
    available: bool
    reason: str


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def detect() -> dict:
    statuses = [
        CapabilityStatus(
            "github_api",
            bool(os.getenv("GITHUB_TOKEN")) or True,
            "public GitHub API is usable; token enables authenticated access when present",
        ),
        CapabilityStatus(
            "github_actions",
            bool(os.getenv("GITHUB_ACTIONS")),
            "running inside GitHub Actions" if os.getenv("GITHUB_ACTIONS") else "not running inside GitHub Actions",
        ),
        CapabilityStatus(
            "browser_use",
            module_available("browser_use"),
            "browser-use package detected" if module_available("browser_use") else "package unavailable",
        ),
        CapabilityStatus(
            "playwright",
            module_available("playwright"),
            "Playwright package detected" if module_available("playwright") else "package unavailable",
        ),
        CapabilityStatus(
            "langgraph",
            module_available("langgraph"),
            "LangGraph package detected" if module_available("langgraph") else "package unavailable",
        ),
        CapabilityStatus(
            "r2r",
            module_available("r2r"),
            "R2R package detected" if module_available("r2r") else "package unavailable",
        ),
        CapabilityStatus(
            "khoj",
            module_available("khoj"),
            "Khoj package detected" if module_available("khoj") else "package unavailable",
        ),
    ]
    return {
        "mode": "adaptive",
        "statuses": [asdict(item) for item in statuses],
        "available": [item.name for item in statuses if item.available],
        "unavailable": [item.name for item in statuses if not item.available],
    }
