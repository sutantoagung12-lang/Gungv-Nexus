"""Checkpoint coordinator for reversible agent state."""
class CheckpointManager:
    def __init__(self): self.items=[]
    def create(self,state_id,state):
        item={'id':state_id,'state':dict(state)}; self.items.append(item); return item
    def latest(self): return self.items[-1] if self.items else None
