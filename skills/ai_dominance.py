"""AI capability mastery skill for Nexus.

"Dominasi AI" is treated as technical mastery: systematically map, evaluate,
combine, and improve AI capabilities while preserving validation, provenance,
authorization, and human control.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AIMasteryDecision:
    domains: tuple[str, ...]
    capabilities: tuple[str, ...]
    gaps: tuple[str, ...]
    actions: tuple[str, ...]
    status: str = "CANDIDATE"


class AIDominanceSkill:
    """Build a measurable AI capability-mastery plan."""

    CORE_DOMAINS = (
        "reasoning",
        "agents",
        "memory",
        "rag",
        "coding",
        "browser-automation",
        "multimodal",
        "evaluation",
        "observability",
        "security",
        "deployment",
        "research",
    )

    def assess(
        self,
        known_domains: Iterable[str],
        known_capabilities: Iterable[str],
    ) -> AIMasteryDecision:
        domains = set(x.strip().lower() for x in known_domains if x.strip())
        capabilities = set(
            x.strip().lower() for x in known_capabilities if x.strip()
        )
        gaps = tuple(sorted(set(self.CORE_DOMAINS) - domains))
        actions = (
            "discover-missing-capabilities",
            "retrieve-primary-sources",
            "compare-alternatives",
            "build-isolated-prototypes",
            "benchmark",
            "verify",
            "integrate-only-validated-capabilities",
            "record-lessons",
            "reassess",
        )
        return AIMasteryDecision(
            domains=tuple(sorted(domains)),
            capabilities=tuple(sorted(capabilities)),
            gaps=gaps,
            actions=actions,
        )

    @staticmethod
    def expansion_rule() -> str:
        return (
            "Never equate more tools with more intelligence. "
            "Promote a capability only when evidence shows improved "
            "performance, reliability, or coverage without violating policy."
        )
