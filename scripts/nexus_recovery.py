"""Safe recovery planning for Nexus diagnostics.

Recovery plans describe validated next steps. They do not execute external
actions, install dependencies, change credentials, or bypass approval gates.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RecoveryPlan:
    check: str
    reason: str
    strategy: str
    steps: tuple[str, ...]
    requires_human_approval: bool = False


RECOVERY_RULES = {
    "environment_not_validated": RecoveryPlan(
        "activation",
        "environment_not_validated",
        "validate-environment",
        (
            "Run the dependency-light Nexus validator.",
            "Confirm the intended runtime and capability endpoint.",
            "Re-run health diagnostics.",
        ),
    ),
    "integration_tests_not_passed": RecoveryPlan(
        "integration",
        "integration_tests_not_passed",
        "validate-tests",
        (
            "Run pytest.",
            "Run the Nexus contract validator.",
            "Re-run health diagnostics.",
        ),
    ),
    "human_approval_required_for_browser_actions": RecoveryPlan(
        "browser_use",
        "human_approval_required_for_browser_actions",
        "approval-gated-browser-activation",
        (
            "Validate the browser worker environment.",
            "Review the exact browser action.",
            "Obtain explicit human approval.",
            "Re-run the activation gate.",
        ),
        True,
    ),
    "human_approval_required_for_android_chrome_actions": RecoveryPlan(
        "android_chrome_cdp",
        "human_approval_required_for_android_chrome_actions",
        "approval-gated-android-chrome-activation",
        (
            "Validate the authorized CDP endpoint.",
            "Review the exact Android Chrome action.",
            "Obtain explicit human approval.",
            "Re-run the activation gate.",
        ),
        True,
    ),
    "browser_adapter_unavailable": RecoveryPlan(
        "browser_use",
        "browser_adapter_unavailable",
        "configure-browser-adapter",
        (
            "Inspect the browser adapter runtime.",
            "Install or configure dependencies only in the controlled execution environment.",
            "Run integration tests.",
            "Re-run health diagnostics.",
        ),
    ),
    "android_chrome_cdp_endpoint_unavailable": RecoveryPlan(
        "android_chrome_cdp",
        "android_chrome_cdp_endpoint_unavailable",
        "configure-authorized-cdp",
        (
            "Expose an authorized Android Chrome CDP endpoint.",
            "Set NEXUS_ANDROID_CHROME_CDP_URL.",
            "Verify endpoint availability.",
            "Re-run health diagnostics.",
        ),
        True,
    ),
}


def plan_recovery(reason: str) -> RecoveryPlan:
    """Return a safe recovery plan; unknown reasons remain review-only."""
    return RECOVERY_RULES.get(
        reason,
        RecoveryPlan(
            "unknown",
            reason,
            "manual-review",
            (
                "Inspect the diagnostic evidence.",
                "Run the smallest relevant validation.",
                "Do not change activation state until the condition is understood.",
            ),
        ),
    )


def build_recovery_report(diagnostics: list[dict]) -> list[dict]:
    plans = []
    for item in diagnostics:
        plan = plan_recovery(item["reason"])
        plans.append(asdict(plan))
    return plans
