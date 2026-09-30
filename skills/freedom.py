"""Freedom skill for Nexus.

"Freedom" means maximizing autonomous choice among authorized, reversible
actions while preserving policy gates, checkpoints, verification, and human
authority for destructive or externally consequential actions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FreedomDecision:
    mode: str
    allowed_actions: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    requires_approval: tuple[str, ...]
    checkpoint_required: bool
    verification_required: bool


class FreedomSkill:
    """Select the widest safe autonomy envelope for a task."""

    SAFE_AUTONOMY = (
        "research",
        "analyze",
        "plan",
        "draft",
        "test",
        "validate",
        "create_reversible_change",
        "learn",
        "propose_evolution",
    )
    CONSEQUENT_ACTIONS = (
        "publish",
        "send_external_message",
        "spend_money",
        "delete_data",
        "change_credentials",
        "deploy_production",
        "modify_access",
    )

    def decide(
        self,
        requested_actions: Iterable[str],
        *,
        authorized: bool = False,
        environment_validated: bool = False,
    ) -> FreedomDecision:
        requested = tuple(dict.fromkeys(x.strip() for x in requested_actions if x.strip()))
        allowed = []
        blocked = []
        approval = []

        for action in requested:
            if action in self.SAFE_AUTONOMY:
                allowed.append(action)
            elif action in self.CONSEQUENT_ACTIONS:
                if authorized and environment_validated:
                    approval.append(action)
                else:
                    blocked.append(action)
            else:
                blocked.append(action)

        return FreedomDecision(
            mode="maximum-safe-autonomy",
            allowed_actions=tuple(allowed),
            blocked_actions=tuple(blocked),
            requires_approval=tuple(approval),
            checkpoint_required=bool(allowed or approval),
            verification_required=True,
        )
