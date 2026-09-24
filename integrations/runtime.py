"""Unified runtime inspection for adaptive Nexus planning."""
from integrations.adapters.stack import status
from integrations.runtime_availability import detect


def inspect_runtime() -> dict:
    availability = detect()
    adapters = status()
    available = {x["name"] for x in adapters if x["available"]}
    active = {x["name"] for x in adapters if x["active"]}
    return {
        "mode": "adaptive",
        "availability": availability,
        "adapter_count": len(adapters),
        "adapter_names": [x["name"] for x in adapters],
        "available_adapters": sorted(available),
        "active_adapters": sorted(active),
        "external_execution": False,
        "installation_performed": False,
    }
