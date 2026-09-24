"""Optional Cognee knowledge-engine adapter boundary."""

import importlib.util


class CogneeAdapter:
    name = "Cognee"
    capability = "knowledge/graph-memory"
    package = "cognee"

    def status(self) -> dict:
        return {
            "name": self.name,
            "capability": self.capability,
            "package": self.package,
            "installed": importlib.util.find_spec(self.package) is not None,
            "external_execution": False,
        }
