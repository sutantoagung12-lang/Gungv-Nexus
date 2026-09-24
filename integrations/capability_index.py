"""Capability index for the evolving public-repository composition pool."""
from __future__ import annotations

from collections import defaultdict

from integrations.github_pool import capabilities


def build_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    for item in capabilities():
        capability = item.get("capability")
        repository = item.get("repository")
        if capability and repository and repository not in index[capability]:
            index[capability].append(repository)
    return dict(sorted(index.items()))


def resolve(task: str, limit: int = 5) -> list[dict]:
    text = task.lower()
    index = build_index()
    matches = []
    for capability, repositories in index.items():
        tokens = capability.replace("-", " ").replace("/", " ").split()
        score = sum(1 for token in tokens if token in text)
        if score:
            matches.append((score, capability, repositories))
    matches.sort(key=lambda x: (-x[0], x[1]))
    return [
        {"capability": capability, "repositories": repos[:limit]}
        for _, capability, repos in matches
    ]
