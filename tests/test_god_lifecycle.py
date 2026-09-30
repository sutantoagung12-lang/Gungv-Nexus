from core.god_core import GodCore
from core.god_lifecycle import GodLifecycle

class StubNexus:
    def capabilities(self): return {'capabilities': {}}
    def health(self): return {'status': 'ok'}
    def contract(self): return {'architecture': 'one-agent-composed-system'}
    def think(self, task):
        class C: pass
        c=C(); c.task=task; c.stage='PLAN'; return c
    def propose_capability(self, capability, reason): return {'capability': capability, 'reason': reason}
    def propose_organ(self, organ_id, name, function): return {'organ_id': organ_id}

def test_god_lifecycle_completes():
    god=GodCore(StubNexus()); result=GodLifecycle(god).run('expand AI knowledge')
    assert result['status']=='COMPLETED'; assert result['verified'] is True; assert result['phases'][0]=='WAKE'; assert result['phases'][-1]=='SLEEP'
