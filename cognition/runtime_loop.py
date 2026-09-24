"""Integrated cognitive runtime loop."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class CognitiveCycle:
    cycle_id: str
    objective: str
    task: str
    status: str
    plan: dict
    evaluation: dict
    lesson: dict
    generated_at: str

class CognitiveRuntimeLoop:
    def __init__(self, runtime):
        self.runtime = runtime

    def run(self, objective: str, task: str):
        cycle_id = "cognitive-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        plan = self.runtime.power_plan(objective, task)
        gate = self.runtime.change_gate(task)
        execution = {
            "status": "READY_FOR_APPROVAL" if gate["confirmation_required"] else "SAFE_TO_EXECUTE",
            "gate": gate,
            "actions": [],
        }
        result = {
            "cycle_id": cycle_id,
            "objective": objective,
            "task": task,
            "status": "READY_FOR_EXECUTION",
            "agents": plan["agents"],
            "context": plan["focus"],
            "plan": plan,
            "execution": execution,
        }
        quality = self.runtime.quality_evaluate(result)
        lesson = self.runtime.learning.learn(
            cycle_id=cycle_id, goal=objective, task=task,
            evaluation={"passed": quality["passed"]}
        )
        return asdict(CognitiveCycle(
            cycle_id=cycle_id, objective=objective, task=task,
            status="EVALUATED", plan=plan, evaluation=quality,
            lesson=lesson, generated_at=datetime.now(timezone.utc).isoformat()
        ))
