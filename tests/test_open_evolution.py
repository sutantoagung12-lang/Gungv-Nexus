from core.organ_registry import OrganRegistry
from core.capability_evolution import CapabilityEvolution

def test_validated_organ_can_evolve():
    r=OrganRegistry(); r.propose('vision','Vision','perception'); r.validate('vision'); r.activate('vision'); assert r.organs['vision'].status=='ACTIVE'

def test_capability_evolution_is_evidence_gated():
    e=CapabilityEvolution(); p=e.propose('new-cap','gap'); e.validate(p,{'test':'pass'}); e.promote(p); assert p['status']=='ACTIVE'
