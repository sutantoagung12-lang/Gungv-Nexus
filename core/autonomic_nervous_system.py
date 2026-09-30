"""Central autonomic nervous system for Nexus organs."""
from dataclasses import dataclass, field
from typing import Any, Callable
@dataclass
class Signal:
    kind:str
    payload:dict[str,Any]=field(default_factory=dict)
    source:str='system'
class AutonomicNervousSystem:
    def __init__(self): self.handlers:dict[str,list[Callable[[Signal],None]]]={}; self.history:list[Signal]=[]
    def connect(self,kind,handler): self.handlers.setdefault(kind,[]).append(handler)
    def emit(self,kind,payload=None,source='system'):
        s=Signal(kind,payload or {},source); self.history.append(s)
        for h in self.handlers.get(kind,[]): h(s)
        return s
    def pulse(self): return self.emit('HEARTBEAT',{'history':len(self.history)},'nervous-system')
