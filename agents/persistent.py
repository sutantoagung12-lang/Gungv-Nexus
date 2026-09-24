"""Bounded persistent-agent adapter."""
class PersistentAgent:
    def __init__(self,runtime): self.runtime=runtime
    def run_once(self,objective,task): return self.runtime.cognitive_cycle(objective,task)
