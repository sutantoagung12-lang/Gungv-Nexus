from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class RepositoryAdapter(Protocol):
    name: str

    def inspect(self, target: str) -> dict: ...

    def plan(self, target: str, operation: str, payload: dict) -> dict: ...


@dataclass(frozen=True)
class AdapterCapability:
    name: str
    operations: frozenset[str]
    read_only: bool = True


class AdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, RepositoryAdapter] = {}

    def register(self, adapter: RepositoryAdapter) -> None:
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> RepositoryAdapter | None:
        return self._adapters.get(name)

    def capabilities(self) -> list[str]:
        return sorted(self._adapters)
