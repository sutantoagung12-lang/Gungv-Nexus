# Nexus Web Environment

Gungv-Nexus can be hosted behind a browser-accessible control plane. The web environment is treated as an adapter, not as the intelligence itself.

## Architecture

Android browser -> Web UI -> HTTP/WebSocket control plane -> Nexus Agent / God Kernel -> policy + capability resolver -> validated workers -> GitHub / terminal / browser / external services

## Rules

- Browser credentials stay outside the repository.
- The browser is an untrusted boundary.
- External code remains reference-only until validation.
- Consequential actions remain authorization-gated.
- Persistent state is supplied by the host.
- Checkpoints and verification remain mandatory.

## Minimal web contract

A host should expose:
- GET /health
- GET /capabilities
- POST /session
- POST /task
- GET /session/{id}
- WebSocket /events

The runtime/web_environment_adapter.py module provides the platform-neutral session and capability model. A concrete web host can be implemented with FastAPI, Flask, Node, or another runtime without changing Nexus core.
