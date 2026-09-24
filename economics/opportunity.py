"""Opportunity scoring for sustainable, user-directed monetization."""
from dataclasses import dataclass, asdict

@dataclass
class Opportunity:
    name: str
    value: float
    cost: float
    risk: float
    confidence: float

    def score(self):
        benefit=max(0.0,self.value-self.cost)
        return round(benefit*self.confidence*(1.0-min(max(self.risk,0.0),1.0)),6)

class OpportunityEngine:
    def evaluate(self, opportunities):
        rows=[]
        for item in opportunities or []:
            if isinstance(item, Opportunity):
                obj=item
            else:
                obj=Opportunity(
                    name=str(item.get("name","")),
                    value=float(item.get("value",0)),
                    cost=float(item.get("cost",0)),
                    risk=float(item.get("risk",0)),
                    confidence=float(item.get("confidence",0.5)),
                )
            rows.append({**asdict(obj),"score":obj.score()})
        return sorted(rows,key=lambda x:x["score"],reverse=True)
