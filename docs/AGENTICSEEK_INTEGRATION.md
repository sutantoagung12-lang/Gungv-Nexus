# AgenticSeek integration

Gungv-Nexus now contains a small, dependency-free capability bridge inspired by
the architecture of [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek).

## What is combined

AgenticSeek's documented architecture provides useful patterns for:

- task-aware agent routing;
- explicit planner, browser, coding and file-agent roles;
- model/provider selection;
- web interaction as an agent capability;
- session/memory recovery;
- tool-oriented execution.

Nexus already provides complementary infrastructure for planning, agent
orchestration, memory, research, capability resolution, execution gates,
evaluation, recovery and guarded self-repair. The bridge connects the two
conceptual layers instead of replacing Nexus components.

The resulting flow is:

    user task
      -> Nexus orchestration
      -> AgenticSeek capability profile
      -> Nexus-native agents
      -> capability/provider resolver
      -> gated execution
      -> evaluation / memory / learning

## Android-oriented constraint

The bridge itself has no Docker, browser-driver, model-runtime or cloud API
dependency. It only classifies the task and selects logical roles. Actual
browser automation, local LLM inference, or external tool execution remains a
separate adapter and must be validated by Nexus before activation.

This keeps the architecture compatible with a lightweight Android client while
allowing a more capable remote runtime to provide heavy components.

## License boundary

This integration is an architectural adaptation. No AgenticSeek source file,
prompt, model asset, or binary is copied into Gungv-Nexus. AgenticSeek remains
an external reference/project and retains its own GPL-3.0 license.

## Safety boundary

The bridge does not execute actions. Nexus execution policy remains
confirmation-gated for destructive operations, and external components remain
untrusted until validated.
