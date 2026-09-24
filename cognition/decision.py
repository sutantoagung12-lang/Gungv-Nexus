"""Decision record requiring explicit evidence and uncertainty."""
class DecisionEngine:
    def prepare(self, question, options, evidence=None):
        return {"question":question,"options":list(options),"evidence":evidence or [],"status":"needs-human-decision"}
