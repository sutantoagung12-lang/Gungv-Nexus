# Colibri × Gungv-Nexus

Gungv-Nexus now contains an adapter boundary for [JustVugg/colibri](https://github.com/JustVugg/colibri).

## Design

Colibri is not copied into Nexus. Nexus treats it as an inference provider:

Human / ChatGPT
→ Nexus orchestration
→ capability resolution
→ Colibri adapter
→ `coli serve`
→ large local model

Nexus remains responsible for agents, skills, memory, provenance, security,
evaluation, recovery and execution policy. Colibri is responsible for model
inference and its memory-hierarchy optimizations.

## Adapted concepts

1. SSD-backed model storage and streaming are represented as provider
   placement metadata.
2. RAM is treated as resident hot state.
3. VRAM is optional acceleration rather than a hard dependency.
4. Expert caching remains inside the provider boundary.
5. Colibri's OpenAI-compatible server becomes the stable integration surface.
6. Provider availability is environment-validated before capability routing.

## Configuration

Set:

```text
NEXUS_COLIBRI_BASE_URL=http://127.0.0.1:8080
NEXUS_COLIBRI_MODEL=auto
NEXUS_COLIBRI_TIMEOUT=30
```

The adapter uses only Python's standard library.

## Runtime checks

The Nexus runtime reports Colibri as configured when
`NEXUS_COLIBRI_BASE_URL` exists. This does not claim the server is reachable.
The adapter's `health()` performs an explicit runtime probe against
`/health`, falling back to `/v1/models`.

## Android boundary

An Android phone can act as a client to a Colibri/Nexus server. This integration
does not claim that large Colibri models can run directly on an Android phone.
A remote or separate Linux/macOS/Windows host is required for the large-model
runtime unless a future Android-compatible Colibri build is validated.

## Safety

No credentials, model weights, or external source code are added to Nexus.
Destructive repository operations remain outside this adapter.
