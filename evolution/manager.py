"""Controlled evolution manager."""
class EvolutionManager:
    stages=("WEAKNESS","HYPOTHESIS","EXPERIMENT","EVALUATION","PROMOTION")
    def propose(self,weakness,hypothesis):
        return {"stage":"WEAKNESS","weakness":weakness,"hypothesis":hypothesis,"promotion_allowed":False}
    def promote(self,record,evaluation_passed=False,reviewed=False):
        record=dict(record)
        record["promotion_allowed"]=bool(evaluation_passed and reviewed)
        record["stage"]="PROMOTION" if record["promotion_allowed"] else "EVALUATION"
        return record
