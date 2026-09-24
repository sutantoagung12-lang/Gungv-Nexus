from provenance.engine import attach
from epistemic.firewall import EpistemicFirewall

class FederationGateway:
    """External-source boundary. Data remains untrusted until validated."""
    def __init__(self): self.firewall=EpistemicFirewall()
    def ingest(self, data: dict, source: str, method="external"):
        data=dict(data); attach(data,source,method); data["trust"]="untrusted"; return self.firewall.classify(data)
