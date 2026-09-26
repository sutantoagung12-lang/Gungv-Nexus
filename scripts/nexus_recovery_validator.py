"""Validate recovery plans against deterministic acceptance criteria.

This module validates plan structure and safety properties only. It never
executes a recovery action.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from scripts.nexus_recovery import RecoveryPlan, plan_recovery


@dataclass(frozen=True)
class RecoveryValidation:
    strategy: str
    valid: bool
    checks: tuple[str, ...]
    failures: tuple[str, ...]


def validate_plan(plan: RecoveryPlan) -> RecoveryValidation:
    checks = []
    failures = []

    if plan.steps:
        checks.append("non_empty_steps")
    else:
        failures.append("empty_steps")

    if plan.strategy:
        checks.append("strategy_present")
    else:
        failures.append("missing_strategy")

    joined = " ".join(plan.steps).lower()
    forbidden = ("execute immediately", "bypass approval", "skip validation")
    if any(term in joined for term in forbidden):
        failures.append("unsafe_instruction_present")
    else:
        checks.append("no_unsafe_instruction")

    if plan.requires_human_approval:
        if "approval" in joined:
            checks.append("approval_requirement_explicit")
        else:
            failures.append("approval_requirement_missing")

    return RecoveryValidation(
        strategy=plan.strategy,
        valid=not failures,
        checks=tuple(checks),
        failures=tuple(failures),
    )


def validate_reason(reason: str) -> dict:
    plan = plan_recovery(reason)
    result = validate_plan(plan)
    return {
        "reason": reason,
        "plan": asdict(plan),
        "validation": asdict(result),
    }


def validate_all_recovery_plans() -> list[dict]:
    from scripts.nexus_recovery import RECOVERY_RULES

    return [validate_reason(reason) for reason in RECOVERY_RULES]
