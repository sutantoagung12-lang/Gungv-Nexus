# Gungv-Nexus Unified Agent Architecture

Gungv-Nexus is structurally one agent. The modules under agents/, integrations/,
memory/, knowledge/, experiments/, and skills/ are internal organs of that
agent, not separate top-level agents.

## Unified flow

WAKE -> HYDRATE -> UNDERSTAND -> RETRIEVE -> DISCOVER -> PLAN ->
POLICY_CHECK -> EXECUTE -> CHECKPOINT -> OBSERVE -> VERIFY -> LEARN ->
EVOLVE -> SLEEP

## Cognitive organs

- Orchestrator: task routing and agent selection logic.
- Capability resolver: chooses available capabilities and fallbacks.
- Autonomous runtime: composes routing and autonomous skill patterns.
- Memory/knowledge: persistence, retrieval, experience and lessons.
- Skill system: builds, stores, promotes and retrieves skills.
- Experiment engine: isolates and evaluates improvements.
- Domain expansion: discovers validated capabilities outside the current domain.
- Self evolution: compares candidates against baselines and rolls back regressions.
- AI dominance: measures capability coverage and identifies technical gaps.
- Lifecycle/activation: controls execution boundaries and recovery.

## One-agent rule

Only GungvNexusAgent is the public structural entry point. Internal modules may
remain independently testable and replaceable. External repositories are
references until security, license, compatibility and tests validate them.

## Safety rule

Planning is not execution. External execution, destructive actions, credential
changes, production deployment and access changes require their existing
authorization and validation gates.

## Evolution rule

A change becomes active only after evidence, verification and regression checks.
Failed candidates return to the last verified checkpoint.
