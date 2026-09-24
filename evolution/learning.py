from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import uuid
from memory.experience_store import Experience


@dataclass
class LearningResult:
    lesson_id: str
    passed: bool
    lesson: str
    recorded: bool
    experience_recorded: bool = False


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
        timestamp = datetime.now(timezone.utc).isoformat()

        self.runtime.memory.add({
            "id": lesson_id,
            "type": "lesson",
            "cycle_id": cycle_id,
            "content": lesson,
            "status": "ACTIVE",
            "timestamp": timestamp
        })

        quality = 1.0 if passed else 0.0
        reward = 1.0 if passed else 0.0
        confidence = 0.9 if passed else 0.2
        self.runtime.experiences.record(Experience(
            task=task,
            result="success" if passed else "adjustment_needed",
            quality=quality,
            reward=reward,
            lessons=[lesson],
            lesson_records=[{
                "lesson": lesson,
                "type": "strategic",
                "confidence": confidence,
                "evidence_count": 1
            }],
        ))

        self.runtime.telemetry.emit(
            "lesson_recorded",
            lesson_id=lesson_id,
            cycle_id=cycle_id,
            passed=passed,
            experience_recorded=True
        )
        return asdict(LearningResult(
            lesson_id, passed, lesson, True, True
        ))
