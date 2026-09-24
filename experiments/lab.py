class ExperimentLab:
    def __init__(self): self.items=[]
    def create(self,question,hypothesis):
        x={'id':f'exp-{len(self.items)+1}','question':question,'hypothesis':hypothesis,'status':'DESIGN'}; self.items.append(x); return x
    def result(self,experiment_id,outcome):
        for x in self.items:
            if x['id']==experiment_id: x.update(outcome=outcome,status='RESULT'); return x
        return None
