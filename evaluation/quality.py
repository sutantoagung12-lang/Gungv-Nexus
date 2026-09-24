"""Quality evaluation for cognitive cycles."""
class QualityEvaluator:
    def evaluate(self, result):
        checks={
            "has_agents":bool(result.get("agents")),
            "has_context":"context" in result,
            "status_present":bool(result.get("status"))
        }
        return {"passed":all(checks.values()),"checks":checks}
