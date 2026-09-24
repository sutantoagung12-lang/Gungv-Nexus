from agents.registry import AGENTS
from integrations.capability_index import resolve


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
        """Route a task to Nexus agents plus dynamically indexed capabilities."""
        agents = self.select(task)
        matched = resolve(task)
        return {
            "agents": agents,
            "capabilities": [item["capability"] for item in matched],
            "capability_sources": matched,
            "external_execution": False,
            "approval_required_for_destructive_actions": True,
        }
