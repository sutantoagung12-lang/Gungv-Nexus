"""Real-time signal routing into GOD-CORE."""
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass
class GodSignal:
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = 'unknown'
    priority: int = 50

class GodSignalRouter:
    def __init__(self, god: Any):
        self.god=god; self.handlers: dict[str,list[Callable[[GodSignal],Any]]]={}; self.history:list[GodSignal]=[]
    def on(self, kind: str, handler: Callable[[GodSignal],Any]): self.handlers.setdefault(kind,[]).append(handler)
    def emit(self, kind: str, payload: dict[str,Any]|None=None, source: str='unknown', priority: int=50):
        signal=GodSignal(kind,payload or {},source,priority); self.history.append(signal)
        for h in self.handlers.get(kind,[]): h(signal)
        for h in self.handlers.get('*',[]): h(signal)
        return signal
    def pulse(self): return self.emit('HEARTBEAT',{'cycle':getattr(self.god.state,'cycle',0)},'god-core')
