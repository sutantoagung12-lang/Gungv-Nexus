from agents.registry import AGENTS
from integrations.agenticseek_bridge import AgenticSeekBridge
from integrations.capability_resolver import resolve
from execution.fallback import build_plan


class Orchestrator:
    def __init__(self):
        self.agenticseek = AgenticSeekBridge()

    def select(self, task: str):
        t = task.lower()
        if any(x in t for x in ("research", "search", "find")):
            selected = ["researcher", "reviewer"]
        elif any(x in t for x in ("code", "implement", "build", "create")):
            selected = ["architect", "coder", "tester", "reviewer"]
        elif any(x in t for x in ("bug", "error", "broken", "debug")):
            selected = ["debugger", "tester", "reviewer"]
        elif any(x in t for x in ("security", "secret", "permission")):
            selected = ["security", "reviewer"]
        else:
            selected = ["planner", "reviewer"]

        # AgenticSeek-inspired roles are additive. Nexus remains authoritative
        # for execution, safety gates, memory and provider resolution.
        for name in self.agenticseek.agent_names(task):
            if name in AGENTS and name not in selected:
                selected.append(name)
        return selected

    def select_with_capabilities(self, task: str) -> dict:
        candidates = resolve(task)
        return {
            "agents": [name for name in self.select(task) if name in AGENTS],
            "capabilities": [item["capability"] for item in candidates],
            "capability_sources": candidates,
            "agenticseek_profile": self.agenticseek.profile(task),
            "fallback_plan": build_plan(candidates),
            "external_execution": False,
            "approval_required_for_destructive_actions": True,
        }
