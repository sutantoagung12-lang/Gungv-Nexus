from core.autonomic_nervous_system import AutonomicNervousSystem

def test_autonomic_nervous_system_routes_signals():
    n=AutonomicNervousSystem(); seen=[]
    n.connect('HEARTBEAT',lambda s: seen.append(s.kind))
    n.pulse()
    assert seen==['HEARTBEAT']
    assert n.history[0].source=='nervous-system'
