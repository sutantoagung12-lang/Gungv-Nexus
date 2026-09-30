# Nexus Human-Body Architecture

Gungv-Nexus models one unified agent as a human-body-like system. This is an engineering analogy: organs are software subsystems and the brain remains the single decision surface.

## Anatomy
- Brain: reasoning, planning and coordination.
- Nervous system: event bus and lifecycle signals.
- Spinal cord: deterministic cycle/state transitions.
- Memory: experiences, skills and learned context.
- Sensory system: observations and runtime health.
- Immune system: authorization, policy and fail-closed controls.
- Muscles: validated workers and capability adapters.
- Bloodstream: state, context and evidence flowing through the cycle.
- Heart: scheduler that keeps work moving.
- Liver: evaluation and filtering before promotion.
- Kidneys: checkpoints, recovery and rollback.
- Lungs: external interfaces and I/O.
- Endocrine system: goals and priorities.
- DNA: contracts, architecture and durable rules.
- Regeneration: creation and evolution of skills and capabilities.

## Core life loop
`WAKE -> SENSE -> THINK -> DECIDE -> ACT -> CHECKPOINT -> OBSERVE -> VERIFY -> LEARN -> EVOLVE -> SLEEP -> WAKE`

## Design principle
One organism, one agent, many organs. No organ independently becomes the public decision-maker. External code remains non-executable until validated; consequential actions remain authorization-gated.
