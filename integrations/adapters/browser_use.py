"""Browser-use adapter boundary.

This module deliberately does not execute browser actions. A worker runtime
must perform actions only after Nexus policy checks and human confirmation
where required.
"""

from typing import Any


class BrowserUseAdapter:
    name = "browser-use"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def status(self) -> dict[str, Any]:
        try:
            import browser_use  # type: ignore
        except ImportError:
            return {"name": self.name, "available": False, "active": False}
        return {
            "name": self.name,
            "available": True,
            "active": bool(self.enabled),
            "version": getattr(browser_use, "__version__", "unknown"),
        }

    def action_request(self, goal: str, requires_confirmation: bool = True) -> dict[str, Any]:
        if not goal.strip():
            raise ValueError("goal must not be empty")
        return {
            "adapter": self.name,
            "goal": goal,
            "requires_confirmation": bool(requires_confirmation),
            "execution_owner": "Gungv-Workers",
            "executed": False,
        }
