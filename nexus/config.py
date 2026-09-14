from __future__ import annotations

from pathlib import Path

import yaml

from .registry import Registry, Repository


def load_repositories(path: str | Path, registry: Registry) -> Registry:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    for item in data.get("repositories", []):
        registry.register_repository(
            Repository(
                name=item["name"],
                full_name=item["full_name"],
                role=item.get("role", "managed"),
                enabled=item.get("enabled", True),
                capabilities=set(item.get("capabilities", [])),
                metadata=item.get("metadata", {}),
            )
        )
    return registry
