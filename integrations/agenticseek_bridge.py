"""Conceptual AgenticSeek capability bridge for Gungv-Nexus.

This module does not copy AgenticSeek source code. It captures the useful
architectural roles observed in Fosowl/agenticSeek and maps them onto Nexus'
existing planner, orchestrator, memory, research, execution, and security
layers.

The bridge is deliberately deterministic and dependency-free so it can run in
lightweight environments, including an Android-oriented deployment.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AgenticSeekRole:
    name: str
    purpose: str
    nexus_agent: str


ROLES = (
    AgenticSeekRole("planner", "decompose complex tasks before execution", "planner"),
    AgenticSeekRole("browser", "navigate, search, read and interact with web pages", "browser"),
    AgenticSeekRole("coder", "write, inspect, test and debug code", "coder"),
    AgenticSeekRole("file", "inspect and transform workspace files", "file"),
    AgenticSeekRole("tool", "invoke an approved external tool or connector", "tool"),
    AgenticSeekRole("model-router", "select an appropriate LLM/provider for the task", "model_router"),
    AgenticSeekRole("memory", "recover and persist useful session context", "recovery"),
)


KEYWORDS = {
    "browser": ("browse", "browser", "web page", "website", "navigate", "form", "click"),
    "coder": ("code", "program", "python", "javascript", "html", "debug", "implement", "build"),
    "file": ("file", "folder", "document", "pdf", "rename", "workspace", "read my"),
    "tool": ("tool", "connector", "mcp", "api", "integration", "execute"),
    "model-router": ("model", "llm", "ollama", "provider", "route", "local ai"),
    "memory": ("remember", "previous session", "session", "memory", "continue"),
    "planner": ("plan", "multi-step", "complex", "workflow", "automate"),
}


class AgenticSeekBridge:
    """Translate AgenticSeek-style task roles into Nexus-native roles."""

    source_repository = "Fosowl/agenticSeek"
    integration_mode = "architecture-adaptation"

    def profile(self, task: str) -> dict:
        text = task.lower()
        matched = []
        for role in ROLES:
            if any(keyword in text for keyword in KEYWORDS.get(role.name, ())):
                matched.append(role)

        # Complex tasks benefit from an explicit planner, while every profile
        # remains safe to consume by the existing Nexus orchestrator.
        if len(matched) > 1 and all(r.name != "planner" for r in matched):
            matched.insert(0, next(r for r in ROLES if r.name == "planner"))
        if not matched:
            matched = [next(r for r in ROLES if r.name == "planner")]

        return {
            "source": self.source_repository,
            "mode": self.integration_mode,
            "roles": [asdict(role) for role in matched],
            "execution": "delegated-to-nexus",
            "destructive_actions": "confirmation-gated",
        }

    def agent_names(self, task: str) -> list[str]:
        return [role["nexus_agent"] for role in self.profile(task)["roles"]]
