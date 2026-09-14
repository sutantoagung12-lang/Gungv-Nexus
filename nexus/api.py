from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .audit import AuditLog
from .clients import automation_client, cmra_client, workers_client
from .cognition import ModelProfile, TaskProfile
from .config import load_repositories
from .orchestrator import Orchestrator
from .policy import DEFAULT_POLICY
from .registry import Repository, Registry, Worker

app = FastAPI(title="Gungv Nexus", version="0.3.0")
registry = Registry()
audit = AuditLog()
orchestrator = Orchestrator(registry)

config_path = Path(__file__).resolve().parent.parent / "config" / "repos.yaml"
if config_path.exists():
    load_repositories(config_path, registry)


class JobRequest(BaseModel):
    kind: str = Field(min_length=1, max_length=80)
    target: str = Field(min_length=1, max_length=200)
    payload: dict = Field(default_factory=dict)
    complexity: float = Field(default=0.5, ge=0, le=1)
    risk: float = Field(default=0.1, ge=0, le=1)
    reasoning: float = Field(default=0, ge=0, le=1)
    coding: float = Field(default=0, ge=0, le=1)
    research: float = Field(default=0, ge=0, le=1)
    multimodal: float = Field(default=0, ge=0, le=1)
    tool_use: float = Field(default=0, ge=0, le=1)
    latency_budget: float = Field(default=1, gt=0)
    cost_budget: float = Field(default=1, gt=0)


class ModelRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    capabilities: dict[str, float] = Field(default_factory=dict)
    latency: float = Field(default=1, gt=0)
    cost: float = Field(default=1, gt=0)
    reliability: float = Field(default=0.8, ge=0, le=1)
    privacy: float = Field(default=0.5, ge=0, le=1)


@app.get("/")
def root():
    return {"service": "gungv-nexus", "status": "ok", "role": "control-plane", "cognition": "cmra-x"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "repositories": len(registry.repositories),
        "workers": len(registry.workers),
        "models": len(orchestrator.router.models),
        "jobs": len(orchestrator.jobs),
        "audit_events": len(audit.events),
    }


def _check_service(name: str, client):
    if client is None:
        return name, {"configured": False, "status": "not_configured"}
    try:
        return name, {"configured": True, "status": "ok", "health": client.health()}
    except Exception as exc:
        return name, {"configured": True, "status": "unreachable", "error": type(exc).__name__}


@app.get("/api/federation/health")
def federation_health():
    """Probe federation members concurrently so one slow service cannot serialize all checks."""
    services = {"cmra": cmra_client(), "workers": workers_client(), "automation": automation_client()}
    configured = [(name, client) for name, client in services.items() if client is not None]
    result = {name: {"configured": False, "status": "not_configured"} for name, client in services.items() if client is None}
    if configured:
        with ThreadPoolExecutor(max_workers=len(configured)) as pool:
            for name, status in pool.map(lambda item: _check_service(*item), configured):
                result[name] = status
    return result


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


@app.post("/api/models")
def register_model(request: ModelRequest):
    model = orchestrator.register_model(ModelProfile(**request.model_dump()))
    audit.record("model_register", request.name)
    return model


@app.get("/api/models")
def models():
    return list(orchestrator.router.models.values())


@app.post("/api/models/{model_name}/result")
def model_result(model_name: str, success: bool = True):
    if model_name not in orchestrator.router.models:
        raise HTTPException(status_code=404, detail="model not found")
    orchestrator.record_model_result(model_name, success)
    audit.record("model_result", model_name, metadata={"success": success})
    return orchestrator.router.models[model_name]


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
        task = TaskProfile(
            kind=request.kind,
            complexity=request.complexity,
            risk=request.risk,
            reasoning=request.reasoning,
            coding=request.coding,
            research=request.research,
            multimodal=request.multimodal,
            tool_use=request.tool_use,
            latency_budget=request.latency_budget,
            cost_budget=request.cost_budget,
        )
        job = orchestrator.submit(request.kind, request.target, request.payload, task)
        audit.record(
            "job_submit",
            request.target,
            metadata={
                "job_id": job.job_id,
                "kind": request.kind,
                "selected_model": job.selected_model,
                "swarm_width": job.swarm_width,
            },
        )
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
