from core.nexus_agent import GungvNexusAgent
from core.agent_cycle import AgentCycle

def test_internal_cycle_completes():
    a=GungvNexusAgent(); r=AgentCycle().run(a,'research AI agents','s1')
    assert r['status']=='COMPLETED'
    assert r['evaluation']['passed'] is True
    assert r['stages'][-1]=='SLEEP'
    assert r['state'].evidence
