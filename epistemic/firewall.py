ALLOWED_TYPES = {"FACT","OBSERVATION","SOURCE","CLAIM","INFERENCE","HYPOTHESIS","EXPERIMENT","RESULT","DECISION","UNKNOWN"}

class EpistemicFirewall:
    def classify(self, record: dict) -> dict:
        kind = str(record.get("type", "UNKNOWN")).upper()
        if kind not in ALLOWED_TYPES:
            kind = "UNKNOWN"
        record["type"] = kind
        if kind in {"FACT","CLAIM","INFERENCE","HYPOTHESIS"} and not record.get("provenance"):
            record["validation"] = "blocked_without_provenance"
        else:
            record.setdefault("validation", "pending")
        return record

    def is_trusted(self, record: dict) -> bool:
        return record.get("validation") in {"validated", "confirmed"} and bool(record.get("provenance"))
