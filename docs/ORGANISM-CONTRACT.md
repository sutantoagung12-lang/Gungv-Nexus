# CMRA-X Organism Contract

## Purpose

Gungv Nexus is the control plane for a provider-neutral CMRA-X organism. It coordinates repositories, workers, jobs, policy and federation health without becoming a model provider or memory implementation.

## Organism map

```text
Nexus       = executive/control plane
CMRA        = memory + reasoning cortex
Neuron      = provider-neutral cognitive execution layer
Workers     = execution body
Automation  = durable behavior/workflows
Verifier    = safety/immune layer
Outcome     = experience/learning signal
Evolution   = controlled adaptation
```

## Runtime loop

```text
Task -> memory/context -> neuron selection -> execution -> verification
     -> outcome -> aggregate learning -> strategy evaluation -> shadow/canary
```

## Federation contract

Every service should expose a lightweight health endpoint. Nexus consumes health as a read-only signal and never forwards secrets, private reasoning traces, or raw provider payloads through the organism-status endpoint.

Environment variables are used only for service URLs/tokens. Credentials remain in deployment environments.

## Evolution boundary

Nexus may orchestrate candidate jobs and record auditable decisions. It must not automatically edit production source code. Candidate changes require regression evidence, shadow evaluation, canary evaluation and rollback capability.

## Current integration

- `Gungv` supplies the mature CMRA-X learning/evolution primitives.
- `Gungv-CMRA` supplies the separated memory/reasoning runtime foundation.
- `Neuron` defines provider-neutral cognitive execution contracts.
- `Gungv-Workers` owns worker execution and provider adapters.
- `Gungv-Automation` owns durable schedules and monetization/content workflows.
- Nexus exposes `/api/organism/status` as the aggregate read-only control-plane view.
