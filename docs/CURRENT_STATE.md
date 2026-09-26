# Current State

- Architecture: 27.0.0
- Health: self-learning-skill-evolution-with-guarded-repair
- GitHub repository: public, main
- Cognitive OS foundations: integrated
- Self-learning and guarded self-repair: implemented
- ChatGPT bootstrap protocol: present
- Public bridge: sanitized, read-only
- Destructive operations: confirmation-gated
- Credentials in runtime: none by design
- AgenticSeek-inspired routing/browser bridge: merged into main
- Android Chrome CDP worker adapter: present, approval-gated, endpoint-dependent
- Dependency-light Nexus contract validator: present at `scripts/validate_nexus.py`
- Google Cloud Build validation path: present at `cloudbuild.yaml`
- GitHub Actions contract workflow: present at `.github/workflows/nexus-contract.yml`
- Workflow execution: not yet verified; observed GitHub workflow runs remain empty
- Production readiness: not claimed

## Validation layers

Nexus now has three intended validation paths:
1. GitHub Actions for repository-hosted CI.
2. Google Cloud Build as an independent cloud CI alternative.
3. `python scripts/validate_nexus.py` as a dependency-light contract check.

The validator is intentionally non-executing with respect to external systems: it performs no network, browser, credential, Android Chrome, or repository-write operations.

## Operating principle

When ChatGPT has GitHub access, read current Nexus state before continuing work. Use actual repository contents as the source of implementation state, then inspect, modify, test, verify, and record the result. Never treat a workflow definition as proof that its workflow succeeded. Browser execution additionally requires an authorized CDP endpoint and explicit approval.
