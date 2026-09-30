"""Web-environment adapter for running Nexus as a browser-accessible control plane.

This module is intentionally platform-neutral: the web host supplies execution,
storage, networking, and authentication. Nexus remains policy-gated and does not
assume that a browser is a trusted execution environment.
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class WebEnvironment:
    name: str = "web"
    capabilities: set[str] = field(default_factory=lambda: {
        "browser_ui", "http_api", "websocket", "web_storage",
        "terminal_bridge", "github_bridge", "agent_control",
    })
    state: str = "READY"
    sessions: dict[str, dict[str, Any]] = field(default_factory=dict)

    def open_session(self, session_id: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        if not session_id.strip():
            raise ValueError("session_id is required")
        self.sessions[session_id] = {
            "metadata": metadata or {},
            "status": "OPEN",
            "capabilities": sorted(self.capabilities),
        }
        return self.sessions[session_id]

    def close_session(self, session_id: str) -> dict[str, Any]:
        session = self.sessions.get(session_id)
        if not session:
            return {"status": "NOT_FOUND"}
        session["status"] = "CLOSED"
        return session

    def describe(self) -> dict[str, Any]:
        return {
            "environment": self.name,
            "state": self.state,
            "capabilities": sorted(self.capabilities),
            "execution_policy": "NEXUS_POLICY_GATED",
            "persistence": "HOST_PROVIDED",
        }
