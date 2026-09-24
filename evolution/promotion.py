"""Controlled promotion gate."""
class PromotionGate:
    def assess(self,experiment_passed,tests_passed): return {'eligible':bool(experiment_passed and tests_passed),'requires_review':True}
