import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class CycleResult:
    cycle_id: str
    goal: str
    task: str
    agents: list
    context: dict
    status: str
    lesson: str = ""

class OrchestrationCycle:
    def __init__(self, runtime):
        self.runtime = runtime

    def run(self, goal: str, task: str):
        cycle_id = str(uuid.uuid4())
        selected = self.runtime.orchestrator.select(task)
        memories = self.runtime.memory.search(task)
        knowledge = self.runtime.knowledge.search(task)
        ctx = self.runtime.context.compile(task, memories=memories, knowledge=knowledge)

        self.runtime.telemetry.emit(
            "cycle_started", cycle_id=cycle_id, goal=goal,
            task=task, agents=selected
        )

        result = CycleResult(
            cycle_id=cycle_id,
            goal=goal,
            task=task,
            agents=selected,
            context=ctx.__dict__,
            status="READY_FOR_EXECUTION"
        )

        self.runtime.memory.add({
            "id": cycle_id,
            "type": "episode",
            "content": f"Goal: {goal}; Task: {task}",
            "status": result.status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        self.runtime.telemetry.emit("cycle_ready", cycle_id=cycle_id, status=result.status)
        return asdict(result)
