# Nexus CI Fallback Matrix

Nexus has multiple independent validation paths so a failure or unavailable
provider does not become a dead end.

1. **GitHub Actions** — native repository CI.
2. **Google Cloud Build** — cloud validation through a GitHub trigger.
3. **CircleCI** — independent GitHub-connected CI.
4. **GitLab CI** — external CI fallback using a GitHub-connected project.

All four paths run the same core contract, health, recovery, readiness, and
pytest checks. None of these configurations grants permission to execute
browser actions or Android Chrome actions.

## Fallback rule

A provider is considered usable only after an actual run is observed.

A configuration file alone is not evidence of success.

If one provider produces no run or cannot be connected, use the next provider.
Do not change Nexus runtime safety gates merely to make CI pass.

## Current limitation

External providers require their respective account/repository connection and
trigger setup. Nexus can keep the configurations ready, but cannot claim that
an external provider is active until a real run is observed.
