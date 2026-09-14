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
    def __init__(self) -> None:
        self.repositories: dict[str, Repository] = {}
        self.workers: dict[str, Worker] = {}

    def register_repository(self, repo: Repository) -> Repository:
        self.repositories[repo.full_name] = repo
        return repo

    def register_worker(self, worker: Worker) -> Worker:
        self.workers[worker.worker_id] = worker
        return worker

    def get_repository(self, full_name: str) -> Repository | None:
        return self.repositories.get(full_name)

    def list_repositories(self) -> list[Repository]:
        return list(self.repositories.values())

    def list_workers(self) -> list[Worker]:
        return list(self.workers.values())
