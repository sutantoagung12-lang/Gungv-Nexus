# Autonomous Skill Integration

Nexus treats public skill repositories as external capability sources, not trusted code.

## Integrated source families

- anyoneanderson/agent-skills: specification-driven orchestration, implementation, review, testing, acceptance evaluation, harness loops, delegation and handover.
- mthines/agent-skills: autonomous workflow dispatcher, bug-fixing workflow, confidence gates, critical review and TDD.
- stellarlinkco/skills: durable harness execution, high-recall review and measurable self-evolution.
- VectorSpaceLab/AREX-Skill: distillation of repository knowledge into executable skills with routing, validation and recovery context.
- Orchestra-Research/AI-Research-SKILLs: AI research lifecycle and specialized engineering skills.

## Nexus execution model

DISCOVER -> RETRIEVE -> PLAN -> POLICY_CHECK -> EXECUTE -> CHECKPOINT -> OBSERVE -> VERIFY -> RECOVER -> LEARN -> EVOLVE

The registry is descriptive. Runtime availability, authorization, credentials, dependency compatibility and test evidence remain authoritative.

## Skill promotion

A discovered skill is first classified as reference. It can become candidate after adaptation design, then validated after tests and acceptance evidence, and only then active.

## Safety boundaries

External code is not copied automatically. License, security, dependency and compatibility checks are required before adaptation. Credentials remain outside source control. Destructive operations remain confirmation-gated. Failed mutations must roll back to the last verified checkpoint.

## Intended next runtime layer

The next implementation step is a capability resolver that converts this registry into runtime decisions:

source -> capability -> lifecycle phase -> permitted agent -> execution adapter -> verifier -> evidence -> promotion/rollback.
