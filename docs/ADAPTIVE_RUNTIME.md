# Adaptive Cognitive Runtime

Gungv-Nexus now treats external repositories as a capability supply map rather than as dependencies.

Runtime flow:

\`task -> capability graph -> runtime readiness -> provider health -> adaptive resolution -> bounded fallback -> execution gate -> experience record\`

Core boundaries:

- \`integrations/capability_graph.py\` maps capabilities to providers and runtime readiness.
- \`integrations/capability_health.py\` ranks providers using readiness, trust, success and quality.
- \`integrations/capability_resolver.py\` selects only currently ready providers.
- \`execution/fallback.py\` prepares bounded alternatives but does not execute them.
- \`memory/experience_store.py\` stores bounded task outcomes for later learning.
- \`resources/manager.py\` exposes resource state without acquiring resources.
- \`integrations/activation_gate.py\` blocks unvalidated and high-risk activation.
- \`agents/orchestrator.py\` consumes the adaptive resolver instead of a static repository list.

The 1,181-entry repository pool remains metadata-only. A repository is not installed or executed merely because it is present in the pool.

Security posture remains conservative: external execution is disabled by default, destructive/high-risk operations remain approval-gated, and repository-side validation is required before activation.
