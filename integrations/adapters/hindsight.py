"""Optional Hindsight long-term memory adapter boundary."""

import importlib.util


class HindsightAdapter:
    name = "Hindsight"
    capability = "memory/temporal-semantic"
    package = "hindsight_client"

    def status(self) -> dict:
        return {
            "name": self.name,
            "capability": self.capability,
            "package": self.package,
            "installed": importlib.util.find_spec(self.package) is not None,
            "external_execution": False,
        }
