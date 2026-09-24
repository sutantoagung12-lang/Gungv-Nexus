"""Knowledge intelligence: confidence and contradiction summaries."""
class KnowledgeIntelligence:
    def __init__(self, runtime):
        self.runtime=runtime

    def analyze(self):
        rows=self.runtime.knowledge.all()
        low=[r for r in rows if float(r.get("confidence",0.5) or 0.5)<0.5]
        return {"records":len(rows),"low_confidence":len(low),"high_confidence":len(rows)-len(low)}
