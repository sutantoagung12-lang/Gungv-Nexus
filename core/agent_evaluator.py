"""Outcome/evidence evaluator for the unified agent."""
class AgentEvaluator:
    def evaluate(self,expected,observed,evidence=None):
        ok=expected==observed if expected is not None else bool(observed)
        return {'passed':ok,'expected':expected,'observed':observed,'evidence':evidence or {},'promotion_eligible':ok and bool(evidence)}
