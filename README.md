# Gungv-Nexus

Gungv-Nexus is the control plane for the Gungv GitHub-Native Cognitive System.

## Mission
Build a persistent, auditable, research-capable cognitive ecosystem connecting ChatGPT, the user's repositories, memory, knowledge, agents, experiments, evaluation, governance, recovery, and controlled evolution.

## Current state
Architecture baseline: v27.0.0 — self-learning skill evolution with guarded repair.

The repository contains runtime foundations for context and reasoning orchestration, memory and knowledge stores, research and experiments, evaluation and learning, work queues and bounded agents, economic opportunity analysis, multi-agent routing, world-model simulation, controlled evolution and promotion, federation boundaries, recovery, bounded autonomous operations, and guarded self-repair.

## Operating boundary
External information is untrusted until provenance, security checks, cross-checking, and validation are satisfied.
Destructive operations require human confirmation.
The runtime does not contain credentials. Chat-session persistence depends on available ChatGPT memory/context and connected runtime. Full CI execution must be verified from actual GitHub Actions runs before claiming production readiness.

## GitHub / ChatGPT
CHATGPT_BOOTSTRAP.md and CHATGPT_NEW_CHAT.md define the ChatGPT bootstrap protocol. The public bridge exposes only sanitized metadata and is read-only.

## Verification
Repository state is authoritative only when read from the current GitHub revision. Workflow definitions are not proof of successful execution; inspect actual workflow runs and conclusions.
