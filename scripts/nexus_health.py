#!/usr/bin/env python3
"""Generate a deterministic Nexus health report with actionable diagnostics."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from integrations.activation_gate import evaluate_activation
from integrations.runtime import inspect_runtime


REMEDIATION = {
    "environment_not_validated": {
        "severity": "activation",
        "action": "Validate the target environment before activation.",
        "next_step": "Run the Nexus contract validator and verify the intended runtime endpoint.",
    },
    "integration_tests_not_passed": {
        "severity": "activation",
        "action": "Run and pass the integration tests before activation.",
        "next_step": "Run pytest and the dependency-light Nexus validator.",
    },
    "human_approval_required_for_browser_actions": {
        "severity": "approval",
        "action": "Keep browser execution blocked until an authorized human approves it.",
        "next_step": "Validate the browser worker and explicitly approve the intended action.",
    },
    "human_approval_required_for_android_chrome_actions": {
        "severity": "approval",
        "action": "Keep Android Chrome execution blocked until explicit approval.",
        "next_step": "Expose an authorized CDP endpoint, validate it, then approve the action.",
    },
    "browser_adapter_unavailable": {
        "severity": "configuration",
        "action": "Configure the BrowserUse adapter before activation.",
        "next_step": "Install/configure the required runtime dependency in the execution environment.",
    },
    "android_chrome_cdp_endpoint_unavailable": {
        "severity": "configuration",
        "action": "Configure an authorized Android Chrome CDP endpoint.",
        "next_step": "Set NEXUS_ANDROID_CHROME_CDP_URL and verify that the endpoint is reachable.",
    },
}


def diagnostic(reason: str) -> dict:
    item = REMEDIATION.get(
        reason,
        {
            "severity": "review",
            "action": "Inspect the reported condition before changing activation state.",
            "next_step": "Run the relevant validation and review the capability gate.",
        },
    )
    return {"reason": reason, **item}


def build_report() -> dict:
    runtime = inspect_runtime()
    checks = []

    def add(name: str, status: str, detail: str, reason: str | None = None) -> None:
        item = {"name": name, "status": status, "detail": detail}
        if reason:
            item["diagnostic"] = diagnostic(reason)
        checks.append(item)

    add(
        "runtime",
        "PASS" if runtime["mode"] == "adaptive" else "FAIL",
        f'mode={runtime["mode"]}',
    )
    add(
        "external_execution",
        "PASS" if runtime["external_execution"] is False else "FAIL",
        "disabled by default",
    )
    add(
        "installation",
        "PASS" if runtime["installation_performed"] is False else "FAIL",
        "no installation performed by runtime inspection",
    )

    android = evaluate_activation("android-chrome-cdp")
    add(
        "android_chrome_cdp",
        "BLOCKED" if not android.allowed else "READY",
        android.reason,
        android.reason if not android.allowed else None,
    )

    browser = evaluate_activation("browser-use")
    add(
        "browser_use",
        "BLOCKED" if not browser.allowed else "READY",
        browser.reason,
        browser.reason if not browser.allowed else None,
    )

    passed = sum(item["status"] == "PASS" for item in checks)
    blocked = sum(item["status"] == "BLOCKED" for item in checks)
    failed = sum(item["status"] == "FAIL" for item in checks)

    diagnostics = [
        {
            "check": item["name"],
            **item["diagnostic"],
        }
        for item in checks
        if "diagnostic" in item
    ]

    return {
        "schema": "nexus-health/v2",
        "overall": "FAIL" if failed else "PASS",
        "summary": {
            "pass": passed,
            "blocked": blocked,
            "fail": failed,
        },
        "runtime": runtime,
        "checks": checks,
        "diagnostics": diagnostics,
        "external_execution": False,
    }


def main() -> int:
    report = build_report()
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else None

    if destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(report, indent=2))
    return 1 if report["overall"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
