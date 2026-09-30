from core.god_kernel import GodKernel

class StubNervous:
    def __init__(self): self.events=[]
    def emit(self,*args): self.events.append(args)
class StubNexus:
    def __init__(self): self.nervous_system=StubNervous()
    def capabilities(self): return {'capabilities': {}}
    def health(self): return {'status':'ok'}
    def contract(self): return {'architecture':'one-agent-composed-system'}
    def think(self,task):
        class C: pass
        c=C(); c.task=task; c.stage='PLAN'; return c
    def propose_capability(self,*args): return {}
    def propose_organ(self,*args): return {}

def test_kernel_unifies_lifecycle_and_signals():
    k=GodKernel(StubNexus()); r=k.run('learn AI'); assert r['verified']; assert k.status()['cycle']==1; assert k.signals.history

def test_kernel_pulse():
    k=GodKernel(StubNexus()); assert k.pulse().kind=='HEARTBEAT'
