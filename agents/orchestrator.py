from agents.registry import AGENTS

class Orchestrator:
    def select(self, task: str):
        t=task.lower()
        if any(x in t for x in ("research","search","find")): return ["researcher","reviewer"]
        if any(x in t for x in ("code","implement","build","create")): return ["architect","coder","tester","reviewer"]
        if any(x in t for x in ("bug","error","broken","debug")): return ["debugger","tester","reviewer"]
        if any(x in t for x in ("security","secret","permission")): return ["security","reviewer"]
        return ["planner","reviewer"]
