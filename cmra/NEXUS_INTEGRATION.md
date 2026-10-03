# CMRA ↔ Gungv-Nexus integration

## Release
- CMRA: `1.0.0`
- CMRA schema: `3`
- rollback baseline: `0.9.0`
- Nexus architecture: `27.0.0`
- protocol: `nexus-cmra/v1`

## Responsibility boundary
CMRA owns local state integrity, canonical state hashing, audit-chain verification,
snapshots, import validation, recovery and rollback.

Gungv-Nexus owns orchestration, memory/knowledge retrieval, agent routing, skills,
policy, evaluation, recovery planning and controlled promotion.

The bridge is deliberately prepare-only. It cannot execute external or destructive
actions. Rollback requests require explicit human approval.

## Flow
`Nexus task → CMRA handshake → prepare operation → CMRA local execution → integrity/self-test → Nexus evaluation → controlled promotion`

Rollback remains versioned: the CMRA `0.9.0` artifact is the immediate baseline for
this integration release.

## Verification
The integration tests validate the handshake, execution boundary, release/schema
contract and rollback approval gate without credentials or network side effects.
