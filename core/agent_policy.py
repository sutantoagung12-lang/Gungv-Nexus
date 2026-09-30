"""Policy and authorization boundary for the unified agent."""
from __future__ import annotations
from typing import Any
CONSEQUENTIAL={'publish','send_external_message','spend_money','delete_data','change_credentials','change_access','deploy_production'}
class AgentPolicy:
    def check(self, action: str, *, human_approved=False, environment_validated=False) -> dict[str,Any]:
        restricted=action in CONSEQUENTIAL
        allowed=(not restricted) or (human_approved and environment_validated)
        return {'action':action,'restricted':restricted,'allowed':allowed,'reason':'approved' if allowed else 'authorization_or_validation_required'}
