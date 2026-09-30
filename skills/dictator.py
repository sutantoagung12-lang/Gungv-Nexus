"""Dictator skill for Nexus.

The name is an internal engineering metaphor: strict execution discipline,
not political control. It enforces deterministic rules, checkpoints,
verification, and fail-closed behavior over Nexus tasks.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DictatorDecision:
    mode: str
    approved_steps: tuple[str, ...]
    rejected_steps: tuple[str, ...]
    checkpoint_required: bool
    verification_required: bool
    fail_closed: bool


class DictatorSkill:
    """Apply strict task-discipline without granting extra authority."""

    SAFE_STEPS = {
        "inspect", "research", "analyze", "plan", "code", "test",
        "validate", "checkpoint", "observe", "learn", "propose",
    }
    RESTRICTED_STEPS = {
        "delete", "publish", "spend", "change_credentials",
        "change_access", "deploy_production", "external_message",
    }

    def enforce(
        self,
        steps: Iterable[str],
        *,
        human_approved: bool = False,
        environment_validated: bool = False,
    ) -> DictatorDecision:
        requested = tuple(dict.fromkeys(s.strip() for s in steps if s.strip()))
        approved = []
        rejected = []

        for step in requested:
            if step in self.SAFE_STEPS:
                approved.append(step)
            elif step in self.RESTRICTED_STEPS:
                if human_approved and environment_validated:
                    approved.append(step)
                else:
                    rejected.append(step)
            else:
                rejected.append(step)

        return DictatorDecision(
            mode="strict-execution-discipline",
            approved_steps=tuple(approved),
            rejected_steps=tuple(rejected),
            checkpoint_required=True,
            verification_required=True,
            fail_closed=True,
        )
