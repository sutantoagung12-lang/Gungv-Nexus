"""Structured runtime readiness detection.

Detection is side-effect free: it inspects environment/package presence only.
No network calls, installs, or permission changes are performed.
"""
from __future__ import annotations

import importlib.util
import os
from dataclasses import asdict, dataclass


STATES = ("missing", "installed", "configured", "reachable", "validated", "active")


@dataclass(frozen=True)
class CapabilityStatus:
    name: str
    state: str
    available: bool
    reason: str


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _module_status(name: str, package: str) -> CapabilityStatus:
    present = module_available(package)
    return CapabilityStatus(name, "installed" if present else "missing", present,
                            f"{package} package detected" if present else f"{package} package unavailable")


def detect() -> dict:
    in_actions = bool(os.getenv("GITHUB_ACTIONS"))
    token = bool(os.getenv("GITHUB_TOKEN"))
    statuses = [
        CapabilityStatus("github_api", "configured" if token else "reachable", True,
                         "authenticated token present" if token else "public API path assumed reachable; authenticated features unavailable"),
        CapabilityStatus("github_actions", "reachable" if in_actions else "missing", in_actions,
                         "running inside GitHub Actions" if in_actions else "not running inside GitHub Actions"),
        _module_status("browser_use", "browser_use"),
        _module_status("playwright", "playwright"),
        _module_status("langgraph", "langgraph"),
        _module_status("r2r", "r2r"),
        _module_status("khoj", "khoj"),
    ]
    return {
        "mode": "adaptive",
        "states": list(STATES),
        "statuses": [asdict(item) for item in statuses],
        "available": [item.name for item in statuses if item.available],
        "unavailable": [item.name for item in statuses if not item.available],
        "summary": {item.name: item.state for item in statuses},
    }
