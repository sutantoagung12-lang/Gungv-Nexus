"""Change lifecycle gate."""
class ChangeGate:
    stages=("PROPOSE","IMPACT_ANALYSIS","ISOLATE","TEST","EVALUATE","REVIEW","PROMOTE","RECORD")
    def next(self,current): 
        try: return self.stages[self.stages.index(current)+1]
        except (ValueError,IndexError): return None
