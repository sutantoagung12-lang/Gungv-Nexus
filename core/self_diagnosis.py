"""Self-diagnosis: convert homeostasis observations into repair candidates."""
class SelfDiagnosis:
    def diagnose(self, snapshot):
        return [{"target": alert, "action": "bounded_repair", "status": "CANDIDATE"} for alert in snapshot.alerts]
