from datetime import datetime, timezone

def attach(record: dict, source: str, method: str = "unknown") -> dict:
    record["provenance"] = {
        "source": source,
        "method": method,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }
    return record
