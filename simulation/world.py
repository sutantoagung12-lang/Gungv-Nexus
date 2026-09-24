"""Lightweight world-model simulation boundary."""
class WorldModel:
    def simulate(self,state,change):
        return {"state":state,"proposed_change":change,"risk":"UNKNOWN","requires_evaluation":True}
