"""Persistent skill-governance and routing layer for Nexus.

This layer does not pretend to execute ChatGPT host skills. It records the
skills Nexus knows about, considers the complete registry for every task, and
selects the relevant capabilities for runtime execution. Actual host/plugin
execution remains the responsibility of the connected agent environment.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_SKILLS = [
    {
        "id": "adaptive-task-routing",
        "category": "orchestration",
        "keywords": ["route", "plan", "architecture", "multi-step", "phase"],
    },
    {
        "id": "agent-routekit",
        "category": "orchestration",
        "keywords": ["route", "agent", "model", "provider"],
    },
    {
        "id": "qodo-codebase-wisdom",
        "category": "codebase",
        "keywords": ["repository", "repo", "history", "regression", "codebase"],
    },
    {
        "id": "test-driven-development",
        "category": "testing",
        "keywords": ["test", "bug", "fix", "change", "behavior", "validate"],
    },
    {
        "id": "github",
        "category": "source-control",
        "keywords": ["github", "repository", "repo", "commit", "pull request"],
    },
    {
        "id": "verification",
        "category": "verification",
        "keywords": ["verify", "validation", "e2e", "runtime", "deploy"],
    },
    {
        "id": "browser-automation",
        "category": "browser",
        "keywords": ["browser", "web", "page", "click", "navigate", "chrome"],
    },
    {
        "id": "security",
        "category": "security",
        "keywords": ["security", "secret", "token", "credential", "permission"],
    },
    {
        "id": "deployment",
        "category": "delivery",
        "keywords": ["deploy", "publish", "hosting", "server", "runtime"],
    },
    {
        "id": "database",
        "category": "data",
        "keywords": ["database", "sql", "postgres", "supabase", "storage"],
    },
    {
        "id": "web-development",
        "category": "application",
        "keywords": ["web", "frontend", "backend", "html", "css", "react", "api"],
    },
    {
        "id": "ai-llm",
        "category": "ai",
        "keywords": ["ai", "llm", "model", "agent", "inference", "embedding"],
    },
    {
        "id": "local-ai",
        "category": "ai",
        "keywords": ["local", "offline", "on-device", "private", "ollama"],
    },
    {
        "id": "product-design",
        "category": "design",
        "keywords": ["design", "ux", "ui", "prototype", "flow", "accessibility"],
    },
    {
        "id": "network-operations",
        "category": "infrastructure",
        "keywords": ["network", "server", "linux", "device", "diagnose"],
    },
]


class SkillOrchestrator:
    """Plan skill usage deterministically without fabricating execution."""

    def __init__(self, manifest_path: str | None = None) -> None:
        self.manifest_path = manifest_path or os.getenv("NEXUS_SKILL_MANIFEST")
        self.skills = self._load_skills()

    def _load_skills(self) -> list[dict[str, Any]]:
        if self.manifest_path:
            path = Path(self.manifest_path)
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
        return list(DEFAULT_SKILLS)

    def plan(self, task: str) -> dict[str, Any]:
        normalized = task.lower()
        selected: list[str] = []

        for skill in self.skills:
            keywords = [str(k).lower() for k in skill.get("keywords", [])]
            if any(keyword in normalized for keyword in keywords):
                selected.append(str(skill["id"]))

        # Every task gets the orchestration and verification gates.
        for required in ("adaptive-task-routing", "verification"):
            if required in {str(s["id"]) for s in self.skills} and required not in selected:
                selected.append(required)

        return {
            "policy": "all-relevant",
            "registered_count": len(self.skills),
            "considered_count": len(self.skills),
            "selected": selected,
            "executed": [],
            "requires_host_or_connector_execution": True,
            "note": (
                "Nexus plans against the complete registered skill catalog. "
                "It does not claim ChatGPT-host skills were executed unless an "
                "actual adapter reports execution."
            ),
        }
