from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .orchestrator import Orchestrator
from .registry import Repository, Registry, Worker

app = FastAPI(title="Gungv Nexus", version="0.1.0")
registry = Registry()
orchestrator = Orchestrator(registry)


class JobRequest(BaseModel):
    kind: str = Field(min_length=1)
    target: str = Field(min_length=1)
    payload: dict = Field(default_factory=dict)


@app.get("/")
def root():
    return {"service": "gungv-nexus", "status": "ok", "role": "control-plane"}


@app.get("/health")
def health():
    return {"status": "ok", "repositories": len(registry.repositories), "workers": len(registry.workers), "jobs": len(orchestrator.jobs)}


@app.post("/api/repositories")
def register_repository(repo: Repository):
    return registry.register_repository(repo)


@app.get("/api/repositories")
def repositories():
    return registry.list_repositories()


@app.post("/api/workers")
def register_worker(worker: Worker):
    return registry.register_worker(worker)


@app.get("/api/workers")
def workers():
    return registry.list_workers()


@app.post("/api/jobs")
def submit_job(request: JobRequest):
    try:
        return orchestrator.submit(request.kind, request.target, request.payload)
    except PermissionError as exc:
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
