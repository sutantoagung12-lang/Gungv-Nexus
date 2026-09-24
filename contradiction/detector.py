"""Detect conflicting values for the same subject/predicate."""
class ContradictionDetector:
    def find(self,claims):
        groups={}
        for c in claims: groups.setdefault((c.get("subject"),c.get("predicate")),set()).add(str(c.get("object")))
        return [{"key":k,"values":sorted(v)} for k,v in groups.items() if len(v)>1]
