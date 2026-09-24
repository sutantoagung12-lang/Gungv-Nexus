"""Research-source boundary. Sources are metadata only until validation."""
class ResearchSource:
    def __init__(self,uri,kind="external"):
        self.uri=uri; self.kind=kind
    def envelope(self,content):
        return {"source":self.uri,"kind":self.kind,"trust":"untrusted","content":content}
