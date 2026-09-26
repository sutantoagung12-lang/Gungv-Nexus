#!/usr/bin/env python3
"""Dependency-light Nexus contract validator.

No network, browser, credential, Android Chrome, or repository-write operation
is performed. This validates the control-plane contracts only.
"""

from agents.orchestrator import Orchestrator
from integrations.activation_gate import evaluate_activation
from integrations.agenticseek_browser_loop import AgenticSeekBrowserLoop
from integrations.runtime import inspect_runtime


def main() -> int:
    runtime = inspect_runtime()
    assert runtime["mode"] == "adaptive"
    assert runtime["external_execution"] is False
    assert runtime["installation_performed"] is False
    assert runtime["adapter_count"] == len(runtime["adapter_names"])

    loop = AgenticSeekBrowserLoop()
    prepared = loop.start("validate browser planning boundary")
    assert prepared["execution"] == "delegated-to-nexus-worker"
    assert prepared["action_request"]["executed"] is False

    state = prepared["state"]
    state = loop.observe(state, "contract observation")
    state = loop.reason(state, "contract reasoning")
    state = loop.prepare_action(state, {"type": "snapshot"})
    state = loop.verify(state, "contract verification")
    assert state["stage"] == "complete"

    orchestrated = Orchestrator().prepare_browser_task(
        "browse a website and inspect the page"
    )
    assert orchestrated["action_request"]["executed"] is False
    assert orchestrated["worker"]["name"] == "android-chrome-cdp"
    assert orchestrated["worker"]["requires_authorization"] is True

    android = evaluate_activation("android-chrome-cdp")
    assert android.allowed is False
    assert android.reason == "environment_not_validated"

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
