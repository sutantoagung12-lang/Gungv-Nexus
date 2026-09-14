from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .audit import AuditLog
from .config import load_repositories
from .orchestrator import Orchestrator
from .policy import DEFAULT_POLICY
from .registry import Repository, Registry, Worker

app = FastAPI(title="Gungv Nexus", version="0.2.0")
registry = Registry()
audit = AuditLog()
orchestrator = Orchestrator(registry)

config_path = Path(__file__).resolve().parent.parent / "config" / "repos.yaml"
if config_path.exists():
    load_repositories(config_path, registry)


class JobRequest(BaseModel):
    kind: str = Field(min_length=1)
    target: str = Field(min_length=1)
    payload: dict = Field(default_factory=dict)


@app.get("/")
def root():
    return {"service": "gungv-nexus", "status": "ok", "role": "control-plane"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "repositories": len(registry.repositories),
        "workers": len(registry.workers),
        "jobs": len(orchestrator.jobs),
        "audit_events": len(audit.events),
    }


@app.get("/api/policy")
def policy():
    return {
        "read": DEFAULT_POLICY.allow_read,
        "branch_changes": DEFAULT_POLICY.allow_branch_changes,
        "pull_requests": DEFAULT_POLICY.allow_pull_requests,
        "direct_main_writes": DEFAULT_POLICY.allow_direct_main_writes,
        "workflow_dispatch": DEFAULT_POLICY.allow_workflow_dispatch,
        "require_audit": DEFAULT_POLICY.require_audit,
    }


@app.get("/api/audit")
def audit_events():
    return audit.list()


@app.post("/api/repositories")
def register_repository(repo: Repository):
    result = registry.register_repository(repo)
    audit.record("repository_register", repo.full_name, metadata={"role": repo.role})
    return result


@app.get("/api/repositories")
def repositories():
    return registry.list_repositories()


@app.post("/api/workers")
def register_worker(worker: Worker):
    result = registry.register_worker(worker)
    audit.record("worker_register", worker.worker_id)
    return result


@app.get("/api/workers")
def workers():
    return registry.list_workers()


@app.post("/api/jobs")
def submit_job(request: JobRequest):
    try:
        job = orchestrator.submit(request.kind, request.target, request.payload)
        audit.record("job_submit", request.target, metadata={"job_id": job.job_id, "kind": request.kind})
        return job
    except PermissionError as exc:
        audit.record("job_submit", request.target, outcome="denied", metadata={"kind": request.kind})
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.get("/api/jobs")
def jobs():
    return orchestrator.list_jobs()


@app.get("/api/jobs/{job_id}")
def job(job_id: str):
    result = orchestrator.get(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="job not found")
    return result
