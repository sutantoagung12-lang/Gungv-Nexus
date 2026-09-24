"""Persistent-safe work queue."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
@dataclass
class WorkItem:
    id:str
    objective:str
    task:str
    status:str="QUEUED"
    attempts:int=0
    created_at:str=""
class WorkQueue:
    def __init__(self): self.items=[]
    def enqueue(self,objective,task):
        x=WorkItem(f"task-{len(self.items)+1}",objective,task,created_at=datetime.now(timezone.utc).isoformat())
        self.items.append(x); return asdict(x)
    def next(self):
        for x in self.items:
            if x.status=="QUEUED": x.status="RUNNING"; x.attempts+=1; return asdict(x)
        return None
    def complete(self,item_id,success=True):
        for x in self.items:
            if x.id==item_id: x.status="COMPLETED" if success else "FAILED"; return asdict(x)
        return None
