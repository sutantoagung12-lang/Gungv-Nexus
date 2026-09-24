"""Deterministic change-impact simulation."""
from dataclasses import dataclass
@dataclass
class SimulationResult:
    change: str
    risk: str
    affected_components: list
    reversible: bool
class DigitalTwin:
    def simulate(self,change,affected_components=None,destructive=False):
        affected_components=affected_components or []
        risk="high" if destructive else ("medium" if affected_components else "low")
        return SimulationResult(change,risk,affected_components,not destructive)
