"""AgenticSeek-inspired browser cognitive loop for Nexus.

The loop models the useful browser-agent control cycle without copying
AgenticSeek implementation code and without executing browser actions itself.

Execution remains delegated to a validated Nexus worker after policy checks.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

from integrations.adapters.browser_use import BrowserUseAdapter


STAGES = ("plan", "observe", "reason", "action", "verify", "complete")


@dataclass(frozen=True)
class BrowserLoopState:
    stage: str
    goal: str
    observation: str | None = None
    reasoning: str | None = None
    action: dict | None = None
    verification: str | None = None


class AgenticSeekBrowserLoop:
    """Prepare a browser-agent cycle; never performs the browser action."""

    def __init__(self, adapter: BrowserUseAdapter | None = None):
        self.adapter = adapter or BrowserUseAdapter()

    def start(self, goal: str, *, requires_confirmation: bool = True) -> dict:
        if not goal.strip():
            raise ValueError("goal must not be empty")
        state = BrowserLoopState(stage="plan", goal=goal)
        return {
            "state": asdict(state),
            "stages": list(STAGES),
            "execution": "delegated-to-nexus-worker",
            "action_request": self.adapter.action_request(
                goal, requires_confirmation=requires_confirmation
            ),
        }

    def observe(self, state: dict, observation: str) -> dict:
        self._require_stage(state, "observe", allow_from=("plan",))
        if not observation.strip():
            raise ValueError("observation must not be empty")
        return {**state, "stage": "reason", "observation": observation}

    def reason(self, state: dict, reasoning: str) -> dict:
        self._require_stage(state, "reason", allow_from=("reason",))
        if not reasoning.strip():
            raise ValueError("reasoning must not be empty")
        return {**state, "stage": "action", "reasoning": reasoning}

    def prepare_action(self, state: dict, action: dict) -> dict:
        self._require_stage(state, "action", allow_from=("action",))
        if not isinstance(action, dict) or not action:
            raise ValueError("action must be a non-empty dict")
        return {**state, "action": action, "stage": "verify"}

    def verify(self, state: dict, verification: str) -> dict:
        self._require_stage(state, "verify", allow_from=("verify",))
        if not verification.strip():
            raise ValueError("verification must not be empty")
        return {**state, "stage": "complete", "verification": verification}

    @staticmethod
    def _require_stage(state: dict, expected: str, *, allow_from: tuple[str, ...]) -> None:
        current = state.get("stage")
        if current not in allow_from or expected not in STAGES:
            raise ValueError(f"invalid browser loop transition: {current} -> {expected}")
