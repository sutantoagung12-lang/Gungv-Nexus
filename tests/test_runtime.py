import tempfile
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kernel.runtime import NexusRuntime

def test_health():
    with tempfile.TemporaryDirectory() as d:
        n=NexusRuntime(d); assert n.health()["status"]=="ok"

def test_external_data_is_untrusted():
    from federation.gateway import FederationGateway
    x=FederationGateway().ingest({"type":"CLAIM","content":"external"},"public-github")
    assert x["trust"]=="untrusted"

def test_destructive_requires_confirmation():
    from security.policy import SecurityPolicy
    x=SecurityPolicy().inspect("delete repository")
    assert x["confirmation_required"] is True
