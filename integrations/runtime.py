"""Unified runtime inspection for adaptive Nexus planning."""
from integrations.adapters.stack import status
from integrations.runtime_availability import detect

def inspect_runtime() -> dict:
    availability = detect()
    adapters = status()
    normalized = []
    for item in adapters:
        row = dict(item)
        row["available"] = bool(row.get("available", row.get("installed", False)))
        row["active"] = bool(row.get("active", False))
        normalized.append(row)
    available = {x["name"] for x in normalized if x["available"]}
    active = {x["name"] for x in normalized if x["active"]}
    return {
        "mode": "adaptive",
        "availability": availability,
        "adapter_count": len(normalized),
        "adapter_names": [x["name"] for x in normalized],
        "available_adapters": sorted(available),
        "active_adapters": sorted(active),
        "external_execution": False,
        "installation_performed": False,
    }
