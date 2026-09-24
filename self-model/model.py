"""Explicit self-state model."""
from dataclasses import dataclass, field
@dataclass
class SelfState:
    version: str="1.1.0"
    capabilities: list=field(default_factory=list)
    limitations: list=field(default_factory=list)
    active_goals: list=field(default_factory=list)
    def snapshot(self):
        return {"version":self.version,"capabilities":list(self.capabilities),"limitations":list(self.limitations),"active_goals":list(self.active_goals)}
