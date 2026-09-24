"""Controlled experiment registry."""
class ExperimentLab:
    def __init__(self): self.experiments=[]
    def create(self,question,hypothesis):
        item={"id":f"exp-{len(self.experiments)+1}","question":question,"hypothesis":hypothesis,"status":"DESIGN"}
        self.experiments.append(item); return item
    def result(self,experiment_id,outcome):
        for x in self.experiments:
            if x["id"]==experiment_id: x.update({"outcome":outcome,"status":"RESULT"}); return x
        return None
