from agents.registry import AGENTS
from integrations.capability_resolver import resolve
from execution.fallback import build_plan


class Orchestrator:
    def select(self, task: str):
        t = task.lower()
        if any(x in t for x in ("research", "search", "find")):
            return ["researcher", "reviewer"]
        if any(x in t for x in ("code", "implement", "build", "create")):
            return ["architect", "coder", "tester", "reviewer"]
        if any(x in t for x in ("bug", "error", "broken", "debug")):
            return ["debugger", "tester", "reviewer"]
        if any(x in t for x in ("security", "secret", "permission")):
            return ["security", "reviewer"]
        return ["planner", "reviewer"]

    def select_with_capabilities(self, task: str) -> dict:
        candidates = resolve(task)
        return {
            "agents": [name for name in self.select(task) if name in AGENTS],
            "capabilities": [item["capability"] for item in candidates],
            "capability_sources": candidates,
            "fallback_plan": build_plan(candidates),
            "external_execution": False,
            "approval_required_for_destructive_actions": True,
        }
