#!/usr/bin/env python3
"""Dependency-light Nexus contract validator.

This validator intentionally performs no network, browser, credential, or write
operations. It checks that the core control-plane boundaries can be imported
and that high-risk integrations remain blocked by default.
"""

from integrations.agenticseek_browser_loop import AgenticSeekBrowserLoop
from integrations.activation_gate import evaluate_activation
from integrations.runtime import inspect_runtime


def main() -> int:
    runtime = inspect_runtime()
    assert runtime["mode"] == "adaptive"
    assert runtime["external_execution"] is False
    assert runtime["installation_performed"] is False

    loop = AgenticSeekBrowserLoop()
    prepared = loop.start("validate browser planning boundary")
    assert prepared["execution"] == "delegated-to-nexus-worker"
    assert prepared["action_request"]["executed"] is False

    decision = evaluate_activation("android-chrome-cdp")
    assert decision.allowed is False
    assert decision.reason == "environment_not_validated"

    browser = evaluate_activation(
        "browser-use",
        environment_validated=True,
        tests_passed=True,
        human_approved=False,
    )
    assert browser.allowed is False
    assert browser.reason == "human_approval_required_for_browser_actions"

    print("NEXUS_VALIDATOR_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
