"""Domain expansion skill for Nexus.

Discovers adjacent domains, maps concepts and capabilities across domains,
identifies reusable skills, and proposes validated expansions without
silently activating untrusted capabilities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Domain:
    name: str
    concepts: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExpansionProposal:
    source_domain: str
    target_domain: str
    bridges: tuple[str, ...]
    candidate_capabilities: tuple[str, ...]
    validation_steps: tuple[str, ...]
    status: str = "CANDIDATE"


class DomainExpansionSkill:
    """Expand Nexus knowledge/capability coverage through validated bridges."""

    def discover(
        self,
        source: Domain,
        candidates: Iterable[Domain],
        *,
        min_bridge_score: int = 1,
    ) -> list[ExpansionProposal]:
        source_terms = set(source.concepts) | set(source.capabilities)
        proposals = []

        for target in candidates:
            target_terms = set(target.concepts) | set(target.capabilities)
            bridges = tuple(sorted(source_terms & target_terms))
            if len(bridges) < min_bridge_score:
                continue

            capabilities = tuple(
                sorted(set(target.capabilities) - set(source.capabilities))
            )
            proposals.append(
                ExpansionProposal(
                    source_domain=source.name,
                    target_domain=target.name,
                    bridges=bridges,
                    candidate_capabilities=capabilities,
                    validation_steps=(
                        "inspect-source",
                        "check-license-and-security",
                        "adapt-in-isolation",
                        "run-tests",
                        "evaluate-results",
                        "promote-after-validation",
                    ),
                )
            )

        return sorted(
            proposals,
            key=lambda x: (-len(x.bridges), x.target_domain),
        )

    @staticmethod
    def merge_knowledge(
        existing: Domain,
        additions: Iterable[str],
    ) -> Domain:
        concepts = tuple(sorted(set(existing.concepts) | set(additions)))
        return Domain(
            name=existing.name,
            concepts=concepts,
            capabilities=existing.capabilities,
        )
