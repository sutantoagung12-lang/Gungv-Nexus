"""Compatibility facade for the adaptive capability resolver."""
from integrations.capability_graph import build_graph

def build_index() -> dict[str, list[str]]:
    return {
        capability: [item["repository"] for item in providers]
        for capability, providers in build_graph().items()
    }

def resolve(task: str, limit: int = 5) -> list[dict]:
    from integrations.capability_resolver import resolve as adaptive_resolve
    results = adaptive_resolve(task, limit=limit)
    return [
        {**item, "repositories": [p["repository"] for p in item["providers"][:limit]]}
        for item in results
    ]
