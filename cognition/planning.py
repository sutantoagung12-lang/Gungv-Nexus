"""Deterministic plan decomposition."""
class PlanningEngine:
    def plan(self, goal, steps):
        return {"goal":goal,"steps":[{"id":i+1,"action":s,"status":"proposed"} for i,s in enumerate(steps)]}
