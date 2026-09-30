"""Priority scheduler for autonomous agent work."""
import heapq
class AgentScheduler:
    def __init__(self): self.queue=[]; self.seq=0
    def submit(self,task,priority=50): self.seq+=1; heapq.heappush(self.queue,(-priority,self.seq,task)); return self.seq
    def next(self): return heapq.heappop(self.queue)[2] if self.queue else None
