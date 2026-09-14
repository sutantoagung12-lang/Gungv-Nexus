from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from uuid import uuid4

from .policy import ActionPolicy, DEFAULT_POLICY
from .registry import Registry


@dataclass
class Job:
    job_id: str
    kind: str
    target: str
    payload: dict = field(default_factory=dict)
    status: str = "queued"
    created_at: float = field(default_factory=time)


class Orchestrator:
    def __init__(self, registry: Registry | None = None, policy: ActionPolicy = DEFAULT_POLICY):
        self.registry = registry or Registry()
        self.policy = policy
        self.jobs: dict[str, Job] = {}

    def submit(self, kind: str, target: str, payload: dict | None = None) -> Job:
        if kind in {"main_write"} and not self.policy.allows("main_write"):
            raise PermissionError("Direct main-branch writes are disabled by policy")
        job = Job(uuid4().hex, kind, target, payload or {})
        self.jobs[job.job_id] = job
        return job

    def get(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)

    def list_jobs(self) -> list[Job]:
        return list(self.jobs.values())
