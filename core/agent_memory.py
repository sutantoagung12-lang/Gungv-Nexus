"""Unified agent memory coordinator."""
from __future__ import annotations
from typing import Any
from memory.skill_store import SkillStore

class AgentMemory:
    def __init__(self) -> None:
        self.skills = SkillStore()
        self.episodes: list[dict[str, Any]] = []
    def remember(self, episode: dict[str, Any]) -> None:
        self.episodes.append(dict(episode))
    def recall(self, task: str) -> list[dict[str, Any]]:
        terms={x.lower() for x in task.split() if len(x)>2}
        return [e for e in self.episodes if terms.intersection({x.lower() for x in str(e.get('task','')).split()})][-20:]
    def learn(self, task: str, outcome: str, evidence: dict[str, Any] | None=None) -> None:
        self.remember({'task':task,'outcome':outcome,'evidence':evidence or {}})
