#!/usr/bin/env python3
"""Generate a deterministic Nexus health report.

The report is local-only: no network, browser, credential, or write to the
repository is performed. A JSON report can optionally be written to a caller
provided path.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from integrations.activation_gate import evaluate_activation
from integrations.runtime import inspect_runtime


def build_report() -> dict:
    runtime = inspect_runtime()
    checks = []

    def add(name: str, status: str, detail: str) -> None:
        checks.append({"name": name, "status": status, "detail": detail})

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
    )

    browser = evaluate_activation("browser-use")
    add(
        "browser_use",
        "BLOCKED" if not browser.allowed else "READY",
        browser.reason,
    )

    passed = sum(item["status"] == "PASS" for item in checks)
    blocked = sum(item["status"] == "BLOCKED" for item in checks)
    failed = sum(item["status"] == "FAIL" for item in checks)

    return {
        "schema": "nexus-health/v1",
        "overall": "FAIL" if failed else "PASS",
        "summary": {
            "pass": passed,
            "blocked": blocked,
            "fail": failed,
        },
        "runtime": runtime,
        "checks": checks,
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

    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["overall"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
