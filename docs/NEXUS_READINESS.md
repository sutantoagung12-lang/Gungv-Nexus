# Nexus Recovery and Readiness

Nexus now has three local-only layers:

1. **Health** — detects runtime and activation conditions.
2. **Recovery** — maps diagnostics to explicit, guarded recovery plans.
3. **Recovery validation** — checks every built-in recovery plan against deterministic safety/structure criteria.

The readiness synthesis is generated with:

`python scripts/nexus_readiness.py health/nexus-readiness.json`

A readiness result of `PASS` means the local health contract and recovery-plan validation passed. It does **not** claim production readiness or authorize external execution.

Google Cloud Build runs all of these checks before the normal test suite.
