"""Capability graph for runtime-aware provider selection."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from integrations.github_pool import capabilities
from integrations.runtime_availability import detect


@dataclass(frozen=True)
class CapabilityNode:
    capability: str
    repository: str
    trust: str
    integration: str
    adapter: str | None
    readiness: str


ADAPTER_MAP = {
    "agent-runtime": "langgraph",
    "rag": "r2r",
    "memory": "khoj",
    "browser-agent": "browser_use",
    "workflow": "langgraph",
    "observability": "opentelemetry",
    "agent-framework": "google_adk",
}


def build_graph(runtime: dict | None = None) -> dict[str, list[dict]]:
    runtime = runtime or detect()
    available = set(runtime.get("available", []))
    graph: dict[str, list[dict]] = {}
    for item in capabilities():
        capability = item.get("capability")
        repository = item.get("repository")
        if not capability or not repository:
            continue
        adapter = ADAPTER_MAP.get(capability)
        ready = "ready" if adapter is None or adapter in available else "unavailable"
        node = CapabilityNode(
            capability=capability,
            repository=repository,
            trust=item.get("trust", "unknown"),
            integration=item.get("integration", "unknown"),
            adapter=adapter,
            readiness=ready,
        )
        graph.setdefault(capability, []).append(asdict(node))

    # Local first-party connectors are not external repositories. They enter
    # the graph only at their observed runtime state; configuration alone is
    # not treated as validated connectivity.
    instagram_state = runtime.get("summary", {}).get("instagram_api", "missing")
    graph.setdefault("social-publishing", []).append(asdict(CapabilityNode(
        capability="social-publishing",
        repository="local/integrations/instagram",
        trust="internal",
        integration="oauth2-api-connector",
        adapter="instagram_api",
        readiness="ready" if instagram_state in {"validated", "active"} else instagram_state,
    )))
    return graph


def providers(capability: str, runtime: dict | None = None) -> list[dict]:
    return [x for x in build_graph(runtime).get(capability, []) if x["readiness"] == "ready"]
