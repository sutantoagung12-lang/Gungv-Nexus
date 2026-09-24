"""LangGraph adapter boundary for Nexus orchestration."""

from typing import Any


class LangGraphAdapter:
    name = "LangGraph"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def status(self) -> dict[str, Any]:
        try:
            import langgraph  # type: ignore
        except ImportError:
            return {"name": self.name, "available": False, "active": False}
        return {
            "name": self.name,
            "available": True,
            "active": bool(self.enabled),
            "version": getattr(langgraph, "__version__", "unknown"),
        }

    def build_plan(self, task: str, nodes: list[str]) -> dict[str, Any]:
        """Return a portable plan; execution remains owned by Nexus."""
        if not task.strip():
            raise ValueError("task must not be empty")
        return {
            "adapter": self.name,
            "task": task,
            "nodes": list(nodes),
            "execution_owner": "Gungv-Nexus",
        }
