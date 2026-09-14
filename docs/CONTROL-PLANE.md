# Nexus Control Plane

## Parallel lanes

1. **Repository lane** — registry, inspection, planning and controlled changes.
2. **Worker lane** — disposable workers with capability/cost/trust metadata.
3. **Job lane** — durable-intent queue and lifecycle orchestration.
4. **CMRA lane** — memory and decision context supplied to jobs.
5. **Safety lane** — policy, audit and least-privilege boundaries.
6. **Delivery lane** — CI validates every change before release.

## Cross-repository model

Nexus can coordinate repositories only through permissions actually granted to the connected GitHub account/app. It should prefer inspection and branch/PR workflows over direct `main` writes. A repository is an explicit managed target, not an implicit permission grant.

## Worker model

Workers are replaceable execution capacity. Jobs must remain recoverable when a worker disappears. Provider-specific implementations belong behind adapters so the control plane remains portable.
