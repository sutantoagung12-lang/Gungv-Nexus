"""Resource catalog for runtime dependencies and capabilities."""
class ResourceCatalog:
    def __init__(self): self.items={}
    def register(self,name,kind,available=False,metadata=None):
        self.items[name]={"kind":kind,"available":available,"metadata":metadata or {}}
    def get(self,name): return self.items.get(name)
    def available(self): return {k:v for k,v in self.items.items() if v["available"]}
