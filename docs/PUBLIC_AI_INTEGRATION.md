# Public AI Integration Layer

Gungv-Nexus treats public AI repositories as external capability sources. They are not trusted code and are not copied wholesale into the core.

## Capability routing

- LangGraph: stateful agent orchestration -> agent orchestrator
- CrewAI: role-based multi-agent coordination -> agent registry
- OpenHands: software-engineering agent -> isolated development worker
- browser-use: browser/computer-use -> isolated browser worker
- Dify: agentic workflows and RAG -> automation connector
- n8n: workflow automation -> automation connector
- Khoj: personal knowledge/retrieval -> memory adapter
- R2R: RAG/knowledge retrieval -> knowledge adapter
- LocalAI: self-hosted model API -> model-provider adapter

## Execution policy

External repositories remain untrusted until validated. Integration uses adapters, service connectors, or isolated workers. Dependency installation and runtime activation require environment review and tests. Credentials remain outside the repository. Destructive actions remain confirmation-gated.

This file defines the integration boundary only; it does not claim that external runtimes are installed or active.
