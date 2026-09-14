from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActionPolicy:
    allow_read: bool = True
    allow_branch_changes: bool = True
    allow_pull_requests: bool = True
    allow_direct_main_writes: bool = False
    allow_workflow_dispatch: bool = True
    require_audit: bool = True

    def allows(self, action: str) -> bool:
        mapping = {
            "read": self.allow_read,
            "branch_write": self.allow_branch_changes,
            "pull_request": self.allow_pull_requests,
            "main_write": self.allow_direct_main_writes,
            "workflow_dispatch": self.allow_workflow_dispatch,
        }
        return mapping.get(action, False)


DEFAULT_POLICY = ActionPolicy()
