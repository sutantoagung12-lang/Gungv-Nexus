# Gungv Nexus

Gungv Nexus is the control plane for the Gungv ecosystem: CMRA memory, repository registry, worker federation, policy, jobs, health and controlled cross-repository orchestration.

## Principles

- One control plane, many repositories and workers.
- Repository actions are explicit, auditable and permission-bound.
- Jobs and memory are durable; workers are disposable.
- Provider-neutral adapters avoid lock-in.
- Secrets never live in source control.
- Nexus does not bypass GitHub permissions or repository protections.

## Initial modules

- `nexus/registry.py` — repository and worker registry.
- `nexus/policy.py` — action policy and safety boundaries.
- `nexus/orchestrator.py` — job routing and lifecycle.
- `nexus/api.py` — FastAPI control-plane API.
- `config/repos.yaml` — declarative repository registry.
- `docs/ARCHITECTURE.md` — system design.

## Status

Foundation initialized. Next stages can add GitHub adapters, CMRA integration, worker federation, durable storage and CI-driven orchestration.