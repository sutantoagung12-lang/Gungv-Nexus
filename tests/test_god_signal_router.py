from core.god_core import GodCore
from core.god_signal_router import GodSignalRouter

class StubNexus:
    def capabilities(self): return {'capabilities': {}}
    def health(self): return {'status': 'ok'}
    def contract(self): return {'architecture': 'one-agent-composed-system'}
    def think(self, task):
        class C: pass
        c=C(); c.task=task; c.stage='PLAN'; return c
    def propose_capability(self, capability, reason): return {'capability': capability}
    def propose_organ(self, organ_id, name, function): return {'organ_id': organ_id}

def test_signal_router_routes_to_handler():
    router=GodSignalRouter(GodCore(StubNexus())); seen=[]; router.on('ERROR', lambda s: seen.append(s.payload['code']))
    router.emit('ERROR',{'code':'x'},'immune'); assert seen==['x']

def test_heartbeat():
    router=GodSignalRouter(GodCore(StubNexus())); assert router.pulse().kind=='HEARTBEAT'
