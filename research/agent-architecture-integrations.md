# AI Agent Architecture Integration Map

Status: research-integrated
Date: 2026-09-30
Target: Gungv-Nexus

This document records external AI-agent repositories as architecture references. They are not treated as trusted runtime dependencies and are not copied directly into Nexus.

## 1. Ouroboros
Repository: https://github.com/razzant/ouroboros

Patterns to study:
- durable identity, memory, history, and continuity across restarts
- specialist-agent swarm coordination
- background reflection and initiative
- self-modification of code, architecture, prompts, tools, and dependencies
- governed evolution through reviewed changes

Nexus target:
- evolution engine
- specialist swarm
- background learning/reflection
- controlled self-improvement

## 2. AgentOS
Repository: https://github.com/framerslab/agentos

Patterns to study:
- persistent cognitive memory
- runtime tool forging
- multi-agent orchestration
- guardrails
- dynamic skill loading
- multiple model/provider abstraction

Nexus target:
- dynamic skill factory
- dynamic tool factory
- agent spawning/orchestration
- provider-neutral model layer

## 3. Web Agent
Repository: https://github.com/nikola66/web-agent

Patterns to study:
- browser-native runtime
- WebContainers
- local-first persistence
- browser-scoped profiles/workspaces
- reusable skills and tools
- planning, reflection, learning, cron
- self-improvement loop

Nexus target:
- Android/browser execution path
- browser worker
- local-first agent workspace
- browser skill runtime

## 4. XMem
Repository: https://github.com/XortexAI/XMem

Status: archived/read-only as of 2026-06-03.

Patterns to study:
- active agentic memory
- memory classification/routing
- temporal and multimodal memory
- judge-based ADD/UPDATE/DELETE/NOOP decisions
- specialized memory agents/stores

Nexus target:
- memory governance
- memory lifecycle
- stale-memory control
- specialized retrieval/promotion

## 5. Agent Cockpit
Repository: https://github.com/daronyondem/agent-cockpit

Patterns to study:
- browser cockpit for multiple AI backends
- provider-neutral workspace context
- local conversations/memory/knowledge base
- mobile PWA interface
- backend switching

Nexus target:
- Nexus control panel
- multi-agent/backend interface
- mobile PWA control surface

## Integration rule

External repositories are research inputs. Before direct code adoption:
1. inspect license compatibility;
2. inspect security model;
3. isolate experiments;
4. adapt architecture rather than blindly copying;
5. run regression tests;
6. require human confirmation for destructive or irreversible operations.

## Intended combined architecture

Gungv-Nexus
-> cognitive kernel
-> persistent memory
-> knowledge layer
-> agent registry/orchestrator
-> dynamic skills
-> dynamic tools
-> specialist swarm
-> browser-native worker
-> agent cockpit/control plane
-> reflection/evaluation
-> guarded self-repair
-> controlled self-evolution

The objective is a modular AI-agent system that can learn from validated experience, acquire new skills/tools, delegate specialized work, operate through browser/mobile interfaces, and evolve under explicit safety and validation gates.
