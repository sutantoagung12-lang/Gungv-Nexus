"""Safe runtime inspection for optional AI integrations."""

from integrations.adapters.stack import status


def inspect_runtime() -> dict:
    adapters = status()
    return {
        "adapter_count": len(adapters),
        "adapter_names": [item["name"] for item in adapters],
        "available_adapters": [item["name"] for item in adapters if item["available"]],
        "active_adapters": [item["name"] for item in adapters if item["active"]],
        "external_execution": False,
        "installation_performed": False,
    }
