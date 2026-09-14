from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Repository:
    name: str
    full_name: str
    role: str = "managed"
    enabled: bool = True
    capabilities: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Worker:
    worker_id: str
    name: str
    capabilities: set[str] = field(default_factory=set)
    capacity: float = 1.0
    cost: float = 0.0
    trusted: bool = False
    status: str = "offline"
    metadata: dict[str, Any] = field(default_factory=dict)


class Registry:
    """In-memory control-plane registry with capability indexes for fast routing."""

    def __init__(self) -> None:
        self.repositories: dict[str, Repository] = {}
        self.workers: dict[str, Worker] = {}
        self._worker_capabilities: dict[str, set[str]] = {}

    def register_repository(self, repo: Repository) -> Repository:
        self.repositories[repo.full_name] = repo
        return repo

    def register_worker(self, worker: Worker) -> Worker:
        previous = self.workers.get(worker.worker_id)
        if previous:
            for capability in previous.capabilities:
                ids = self._worker_capabilities.get(capability)
                if ids:
                    ids.discard(worker.worker_id)
        worker.capabilities = {str(x).strip() for x in worker.capabilities if str(x).strip()}
        self.workers[worker.worker_id] = worker
        for capability in worker.capabilities:
            self._worker_capabilities.setdefault(capability, set()).add(worker.worker_id)
        return worker

    def get_repository(self, full_name: str) -> Repository | None:
        return self.repositories.get(full_name)

    def get_worker(self, worker_id: str) -> Worker | None:
        return self.workers.get(worker_id)

    def workers_for_capability(self, capability: str) -> list[Worker]:
        ids = self._worker_capabilities.get(str(capability).strip(), ())
        return [self.workers[worker_id] for worker_id in ids if worker_id in self.workers]

    def list_repositories(self) -> list[Repository]:
        return list(self.repositories.values())

    def list_workers(self) -> list[Worker]:
        return list(self.workers.values())
