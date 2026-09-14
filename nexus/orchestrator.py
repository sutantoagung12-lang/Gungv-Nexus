from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from uuid import uuid4

from .cognition import AdaptiveRouter, ModelProfile, TaskProfile, plan_parallelism
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
    selected_model: str | None = None
    swarm_width: int = 1


class Orchestrator:
    """Low-overhead orchestrator with adaptive model and swarm planning."""

    def __init__(
        self,
        registry: Registry | None = None,
        policy: ActionPolicy = DEFAULT_POLICY,
        router: AdaptiveRouter | None = None,
    ):
        self.registry = registry or Registry()
        self.policy = policy
        self.router = router or AdaptiveRouter()
        self.jobs: dict[str, Job] = {}

    def submit(
        self,
        kind: str,
        target: str,
        payload: dict | None = None,
        task: TaskProfile | None = None,
    ) -> Job:
        kind = str(kind).strip()
        target = str(target).strip()
        if not kind or not target:
            raise ValueError("kind and target are required")
        if kind == "main_write" and not self.policy.allows("main_write"):
            raise PermissionError("Direct main-branch writes are disabled by policy")
        body = payload if isinstance(payload, dict) else {}
        profile = task or TaskProfile(kind=kind)
        selected = self.router.choose(profile)
        job = Job(
            uuid4().hex,
            kind,
            target,
            body,
            selected_model=selected.name if selected else None,
            swarm_width=plan_parallelism(profile),
        )
        self.jobs[job.job_id] = job
        return job

    def register_model(self, model: ModelProfile) -> ModelProfile:
        return self.router.register(model)

    def record_model_result(self, model_name: str, success: bool) -> None:
        self.router.learn(model_name, success)

    def get(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)

    def list_jobs(self) -> list[Job]:
        return list(self.jobs.values())
