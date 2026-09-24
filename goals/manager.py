from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

@dataclass
class Goal:
    id: str
    title: str
    level: str = "GOAL"
    status: str = "ACTIVE"
    children: list[str] = field(default_factory=list)

class GoalManager:
    def __init__(self):
        self.goals = {}

    def add(self, goal: Goal):
        self.goals[goal.id] = goal
        return goal

    def active(self):
        return [g for g in self.goals.values() if g.status == "ACTIVE"]

    def ensure(self, title: str, level="GOAL"):
        for goal in self.goals.values():
            if goal.title.strip().lower() == title.strip().lower():
                return goal
        return self.add(Goal(id=str(uuid.uuid4()), title=title, level=level))

    def snapshot(self):
        return [g.__dict__.copy() for g in self.goals.values()]
