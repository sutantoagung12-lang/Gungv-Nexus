"""Daily frontier engine: discover new opportunity nodes and generate skills.

The engine produces proposals and node records. It never claims that an
external site was conquered, accessed, or executed without a real adapter.
"""
from __future__ import annotations

import re
from datetime import date
from typing import Any


class DailySkillFrontier:
    def __init__(self, today: str | None = None) -> None:
        self.today = today or date.today().isoformat()

    @staticmethod
    def _slug(value: str) -> str:
        value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
        return value or "frontier"

    def generate_skill(self, candidate: dict[str, Any]) -> dict[str, Any]:
        source = str(candidate.get("id") or candidate.get("problem") or "frontier")
        skill_id = f"generated-{self._slug(source)}"
        return {
            "status": "proposed",
            "skill": {
                "id": skill_id,
                "name": f"Generated skill: {source}",
                "source": source,
                "problem": candidate.get("problem", ""),
                "created_on": self.today,
                "policy": "review-before-activation",
            },
        }

    def create_node(self, candidate: dict[str, Any]) -> dict[str, Any]:
        node_id = self._slug(str(candidate.get("id") or candidate.get("title") or "frontier"))
        return {
            "id": node_id,
            "title": candidate.get("title") or str(candidate.get("id") or "Frontier"),
            "type": "frontier-node",
            "status": "discovered",
            "discovered_on": self.today,
            "source": candidate.get("source", "daily-frontier"),
        }

    def daily_cycle(self, candidates: list[dict[str, Any]]) -> dict[str, Any]:
        skills = [self.generate_skill(candidate)["skill"] for candidate in candidates]
        nodes = [self.create_node(candidate) for candidate in candidates]
        return {
            "policy": "daily-frontier",
            "date": self.today,
            "candidates": len(candidates),
            "generated_skills": skills,
            "nodes": nodes,
            "executed": [],
            "requires_external_adapters": True,
        }
