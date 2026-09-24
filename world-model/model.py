"""Explicit world-state model."""
from dataclasses import dataclass, field
@dataclass
class WorldState:
    facts: dict = field(default_factory=dict)
    observations: list = field(default_factory=list)
    unknowns: list = field(default_factory=list)
    def observe(self,key,value,source=None):
        self.facts[key]={"value":value,"source":source}; self.observations.append({"key":key,"value":value,"source":source})
    def mark_unknown(self,item):
        if item not in self.unknowns: self.unknowns.append(item)
