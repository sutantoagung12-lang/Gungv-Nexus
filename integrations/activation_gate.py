"""Safety gate for activating optional external AI integrations.

Activation is explicit and validation-driven. This module does not install
dependencies or execute external actions.
"""

from dataclasses import dataclass
from integrations.runtime import inspect_runtime


@dataclass(frozen=True)
class ActivationDecision:
    capability: str
    allowed: bool
    reason: str


REQUIRED_CAPABILITIES = {"LangGraph", "R2R", "Khoj", "browser-use"}


def evaluate_activation(capability: str, *, environment_validated: bool = False,
                        tests_passed: bool = False,
                        human_approved: bool = False) -> ActivationDecision:
    if capability not in REQUIRED_CAPABILITIES:
        return ActivationDecision(capability, False, "capability_not_registered")
    if not environment_validated:
        return ActivationDecision(capability, False, "environment_not_validated")
    if not tests_passed:
        return ActivationDecision(capability, False, "integration_tests_not_passed")
    if capability == "browser-use" and not human_approved:
        return ActivationDecision(capability, False, "human_approval_required_for_browser_actions")
    return ActivationDecision(capability, True, "activation_requirements_satisfied")


def activation_report(*, environment_validated: bool = False,
                      tests_passed: bool = False,
                      human_approved: bool = False) -> dict:
    runtime = inspect_runtime()
    decisions = [
        evaluate_activation(
            capability,
            environment_validated=environment_validated,
            tests_passed=tests_passed,
            human_approved=human_approved,
        )
        for capability in sorted(REQUIRED_CAPABILITIES)
    ]
    return {
        "runtime": runtime,
        "decisions": [d.__dict__ for d in decisions],
        "external_execution": False,
    }
