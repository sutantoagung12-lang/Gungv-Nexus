"""Optional agent observability adapter boundary."""

import importlib.util


class OpenTelemetryAdapter:
    name = "OpenTelemetry"
    capability = "observability/tracing"
    package = "opentelemetry"

    def status(self) -> dict:
        return {
            "name": self.name,
            "capability": self.capability,
            "package": self.package,
            "installed": importlib.util.find_spec(self.package) is not None,
            "external_execution": False,
        }
