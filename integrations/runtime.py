"""Runtime inspection for optional AI integrations.

This module reports whether optional packages are installed. It never installs
packages, contacts external services, or executes external actions.
"""

from integrations.adapters.stack import status


def inspect_runtime() -> dict:
    adapters = status()
    available = [item["name"] for item in adapters if item["available"]]
    return {
        "adapter_count": len(adapters),
        "available_adapters": available,
        "external_execution": False,
        "installation_performed": False,
    }
