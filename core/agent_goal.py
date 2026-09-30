"""Goal and priority management for the unified agent."""
from dataclasses import dataclass, field
from typing import Any
@dataclass
class Goal:
    goal_id:str; objective:str; priority:int=50; status:str='ACTIVE'; metrics:dict[str,Any]=field(default_factory=dict)
class GoalManager:
    def __init__(self): self.goals:dict[str,Goal]={}
    def add(self,goal_id,objective,priority=50,metrics=None):
        g=Goal(goal_id,objective,priority,'ACTIVE',metrics or {}); self.goals[goal_id]=g; return g
    def next(self):
        active=[g for g in self.goals.values() if g.status=='ACTIVE']; return max(active,key=lambda g:g.priority) if active else None
    def complete(self,goal_id): self.goals[goal_id].status='COMPLETE'
