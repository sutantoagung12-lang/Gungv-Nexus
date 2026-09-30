"""In-process event bus for the unified agent lifecycle."""
from __future__ import annotations
from collections import defaultdict
from typing import Any, Callable
class AgentEventBus:
    def __init__(self): self._listeners=defaultdict(list)
    def on(self,event:str,handler:Callable[[dict[str,Any]],None]): self._listeners[event].append(handler)
    def emit(self,event:str,payload:dict[str,Any]):
        for handler in tuple(self._listeners.get(event,())): handler(payload)
