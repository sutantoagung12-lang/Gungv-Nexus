"""Persistent-ready work queue."""
class WorkQueue:
    def __init__(self): self.items=[]
    def enqueue(self,objective,task):
        x={'id':f'task-{len(self.items)+1}','objective':objective,'task':task,'status':'QUEUED','attempts':0}; self.items.append(x); return x
    def next(self):
        for x in self.items:
            if x['status']=='QUEUED': x['status']='RUNNING'; x['attempts']+=1; return x
        return None
    def complete(self,item_id,success=True):
        for x in self.items:
            if x['id']==item_id: x['status']='COMPLETED' if success else 'FAILED'; return x
        return None
