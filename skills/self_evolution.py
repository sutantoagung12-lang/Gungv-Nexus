"""Self-evolution skill for Nexus.

Coordinates safe, measurable capability improvement. It proposes evolution,
requires a checkpoint and validation evidence, and supports rollback planning.
It never grants new authority merely because an evolution succeeds.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class EvolutionPlan:
    target: str
    gaps: tuple[str, ...]
    experiments: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    checkpoint: str
    rollback: str
    status: str = "CANDIDATE"


class SelfEvolutionSkill:
    """Turn capability gaps into validation-gated evolution plans."""

    def plan(
        self,
        target: str,
        gaps: Iterable[str],
        *,
        baseline_metric: float | None = None,
    ) -> EvolutionPlan:
        gap_list = tuple(dict.fromkeys(x.strip() for x in gaps if x.strip()))
        experiments = tuple(
            f"isolated-experiment:{gap}" for gap in gap_list
        )
        criteria = (
            "compare-against-baseline",
            "verify-regression-free",
            "verify-policy-compliance",
            "record-evidence",
            "promote-only-if-acceptance-passes",
        )
        if baseline_metric is not None:
            criteria = criteria + ("measure-improvement-over-baseline",)

        return EvolutionPlan(
            target=target.strip(),
            gaps=gap_list,
            experiments=experiments,
            acceptance_criteria=criteria,
            checkpoint="create-last-verified-checkpoint-before-mutation",
            rollback="restore-last-verified-checkpoint-on-regression",
        )

    @staticmethod
    def evaluate(
        baseline: float,
        candidate: float,
        *,
        regression_tolerance: float = 0.0,
    ) -> str:
        if candidate + regression_tolerance < baseline:
            return "ROLLBACK_REQUIRED"
        if candidate > baseline:
            return "PROMOTION_CANDIDATE"
        return "NO_IMPROVEMENT"
