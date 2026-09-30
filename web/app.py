"""Minimal web host for the Nexus browser computer."""
from __future__ import annotations
from typing import Any

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
except ImportError:  # pragma: no cover
    FastAPI = None


if FastAPI:
    app = FastAPI(title="Gungv-Nexus Web Computer")

    class TaskRequest(BaseModel):
        task: str

    def get_kernel():
        from core.nexus_agent import GungvNexusAgent
        from core.god_kernel import GodKernel
        return GodKernel(GungvNexusAgent())

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "READY", "service": "gungv-nexus-web"}

    @app.get("/capabilities")
    def capabilities() -> dict[str, Any]:
        kernel = get_kernel()
        return kernel.status()

    @app.post("/api/task")
    def task(request: TaskRequest) -> dict[str, Any]:
        if not request.task.strip():
            raise HTTPException(status_code=400, detail="task is required")
        try:
            return get_kernel().run(request.task)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.get("/")
    def index():
        return FileResponse("web/index.html")
else:
    app = None
