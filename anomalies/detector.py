"""Simple anomaly detector."""
class AnomalyDetector:
    def detect(self,events):
        return [{"type":"runtime-error","event":e} for e in events if e.get("status") in {"error","failed"}]
