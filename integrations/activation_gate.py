"""Risk-aware activation gate for optional integrations."""
from dataclasses import dataclass
from integrations.runtime import inspect_runtime


@dataclass(frozen=True)
class ActivationDecision:
    capability: str
    allowed: bool
    reason: str


RISK = {"browser-use": "high", "browser_use": "high", "github-write": "high", "code-execution": "high"}


def evaluate_activation(capability: str, *, environment_validated: bool = False,
                        tests_passed: bool = False, human_approved: bool = False) -> ActivationDecision:
    runtime = inspect_runtime()
    if not environment_validated:
        return ActivationDecision(capability, False, "environment_not_validated")
    if not tests_passed:
        return ActivationDecision(capability, False, "integration_tests_not_passed")
    if RISK.get(capability, "low") == "high" and not human_approved:
        return ActivationDecision(capability, False, "human_approval_required_for_high_risk_capability")
    if capability in {"browser-use", "browser_use"} and "browser_use" not in set(runtime["available_adapters"]):
        return ActivationDecision(capability, False, "browser_adapter_unavailable")
    return ActivationDecision(capability, True, "activation_requirements_satisfied")


def activation_report(*, environment_validated: bool = False,
                      tests_passed: bool = False, human_approved: bool = False) -> dict:
    runtime = inspect_runtime()
    decisions = [
        evaluate_activation(name, environment_validated=environment_validated,
                            tests_passed=tests_passed, human_approved=human_approved).__dict__
        for name in runtime["adapter_names"]
    ]
    return {"runtime": runtime, "decisions": decisions, "external_execution": False}
