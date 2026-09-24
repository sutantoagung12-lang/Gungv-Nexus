from dataclasses import dataclass, field

@dataclass
class Goal:
    id: str
    title: str
    level: str = "GOAL"
    status: str = "ACTIVE"
    children: list[str] = field(default_factory=list)

class GoalManager:
    def __init__(self): self.goals={}
    def add(self, goal: Goal): self.goals[goal.id]=goal; return goal
    def active(self): return [g for g in self.goals.values() if g.status=="ACTIVE"]
