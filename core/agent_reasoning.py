"""Explicit reasoning stages without exposing private chain-of-thought."""
class ReasoningEngine:
    STAGES=('frame','decompose','compare','select','verify')
    def analyze(self,task,context=None):
        return {'task':task,'stages':list(self.STAGES),'context_keys':sorted((context or {}).keys()),'decision_status':'structured'}
