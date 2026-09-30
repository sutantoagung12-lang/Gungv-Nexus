from core.god_core import GodCore

class StubNexus:
    def capabilities(self): return {'capabilities': {}}
    def health(self): return {'status': 'ok'}
    def contract(self): return {'architecture': 'one-agent-composed-system'}
    def think(self, task):
        class C: pass
        c=C(); c.task=task; c.stage='PLAN'; return c
    def propose_capability(self, capability, reason): return {'capability': capability, 'reason': reason}
    def propose_organ(self, organ_id, name, function): return {'organ_id': organ_id, 'name': name, 'function': function}

def test_god_core_cycle():
    g=GodCore(StubNexus()); g.awaken('expand AI knowledge'); p=g.perceive('research agents'); assert p['task']=='research agents'; assert g.reason('test')['stage']=='PLAN'; assert g.sleep().mode=='SLEEP'

def test_god_core_expansion():
    g=GodCore(StubNexus()); assert g.propose_evolution('vision','missing perception')['capability']=='vision'; assert g.propose_organ('vision','Vision','perception')['organ_id']=='vision'
