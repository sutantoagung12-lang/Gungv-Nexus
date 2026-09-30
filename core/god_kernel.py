"""GOD-CORE Kernel: single coordination surface for Nexus organs."""
from typing import Any
from core.god_core import GodCore
from core.god_lifecycle import GodLifecycle
from core.god_signal_router import GodSignalRouter
from core.body_system import NexusBody

class GodKernel:
    def __init__(self, nexus: Any):
        self.nexus=nexus
        self.god=GodCore(nexus)
        self.lifecycle=GodLifecycle(self.god)
        self.signals=GodSignalRouter(self.god)
        self.body=NexusBody()
        self._wire()
    def _wire(self):
        self.signals.on('HEARTBEAT', lambda s: self.nexus.nervous_system.emit('HEARTBEAT', s.payload, 'god-core'))
        self.signals.on('ERROR', lambda s: self.nexus.nervous_system.emit('ERROR', s.payload, s.source))
    def run(self, task: str):
        self.signals.emit('TASK_RECEIVED', {'task':task}, 'god-kernel')
        result=self.lifecycle.run(task)
        self.signals.emit('TASK_VERIFIED', {'task':task,'verified':result['verified']}, 'god-kernel')
        return result
    def pulse(self): return self.signals.pulse()
    def map_body(self): return self.body.map()
    def status(self):
        return {'mode':self.god.state.mode,'cycle':self.god.state.cycle,'organs':len(self.body.map()),'signals':len(self.signals.history)}
