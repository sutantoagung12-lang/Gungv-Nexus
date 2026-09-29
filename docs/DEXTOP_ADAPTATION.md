# Dextop-inspired adaptive device runtime

Nexus adopts the architectural ideas from NarYuki/Dextop without copying its
GPL-3.0-or-later implementation.

The adaptation is deliberately a control-plane boundary. Dextop demonstrates
that Android desktop behavior should be selected from observed device
capabilities, not assumed from a manufacturer or SDK alone. Nexus now exposes
the same pattern as a portable Python contract:

- \`DeviceIdentity\` describes the target environment.
- \`DeviceRuntime.register_probe()\` registers read-only capability probes.
- \`DeviceRuntime.probe_all()\` isolates probe failures instead of crashing the runtime.
- \`RuntimeStrategy\` defines ordered backends with explicit capability requirements.
- \`DeviceRuntime.select_strategy()\` chooses the first compatible strategy.
- \`SessionJournal\` records original state before a session changes anything and
  returns that state for restoration.
- \`status()\` provides a machine-readable diagnostic snapshot.

This is not an Android controller yet. It is the stable seam for a future
Android worker/adapter. An Android implementation can provide probes for
virtual display, window control, input routing, orientation, multi-display
topology, and privileged access while keeping Nexus's orchestration and safety
gates unchanged.

Integration boundary:

    Nexus Orchestrator
          |
          v
    capability resolver
          |
          +---- DeviceRuntime
          |       +-- probes
          |       +-- ordered strategies
          |       +-- session journal
          |       +-- diagnostics
          |
          +---- repository/provider capabilities
          |
          v
    execution gate

Safety rules:

1. Probes are read-only.
2. DeviceRuntime itself never launches apps, changes Android settings, injects
   input, or calls hidden APIs.
3. External/device actions remain behind Nexus execution and confirmation gates.
4. A failed probe only removes the dependent strategy; it does not disable the
   whole runtime.
5. Restoration data is captured before a future adapter mutates temporary
   device state.

Next adapter target: Android worker implementing the DeviceRuntime contract.
The adapter should be tested per device/SDK/model and keep narrow matching
rules plus fallback strategies, following the Dextop device-support model.
