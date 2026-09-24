"""Minimal knowledge graph over claims."""
class KnowledgeGraph:
    def __init__(self): self.edges=[]
    def add(self,subject,predicate,object_,source=None):
        self.edges.append({"subject":subject,"predicate":predicate,"object":object_,"source":source})
    def related(self,node):
        return [e for e in self.edges if e["subject"]==node or e["object"]==node]
