from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import uuid

@dataclass
class LearningResult:
    lesson_id: str
    passed: bool
    lesson: str
    recorded: bool

class LearningLoop:
    def __init__(self, runtime):
        self.runtime = runtime

    def learn(self, *, cycle_id, goal, task, evaluation):
        passed = bool(evaluation.get("passed"))
        lesson = (
            f"Successful pattern for goal '{goal}' and task '{task}'"
            if passed else
            f"Adjustment needed for goal '{goal}' and task '{task}'"
        )
        lesson_id = str(uuid.uuid4())
        self.runtime.memory.add({
            "id": lesson_id,
            "type": "lesson",
            "cycle_id": cycle_id,
            "content": lesson,
            "status": "ACTIVE",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        self.runtime.telemetry.emit(
            "lesson_recorded", lesson_id=lesson_id,
            cycle_id=cycle_id, passed=passed
        )
        return asdict(LearningResult(lesson_id, passed, lesson, True))
