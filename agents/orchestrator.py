from agents.registry import AGENTS


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
        """Route a task to Nexus agents plus optional external capabilities."""
        agents = self.select(task)
        t = task.lower()
        capabilities = []

        if any(x in t for x in ("research", "search", "find", "knowledge")):
            capabilities.append("R2R")
        if any(x in t for x in ("memory", "remember", "recall")):
            capabilities.append("Khoj")
        if any(x in t for x in ("browser", "web", "navigate", "website")):
            capabilities.append("browser-use")
        if any(x in t for x in ("workflow", "graph", "orchestrate")):
            capabilities.append("LangGraph")

        return {
            "agents": agents,
            "capabilities": capabilities,
            "external_execution": False,
            "approval_required_for_destructive_actions": True,
        }
