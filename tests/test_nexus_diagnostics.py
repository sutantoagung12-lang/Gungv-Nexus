#!/usr/bin/env python3
"""Validate Nexus health diagnostics and dashboard contracts."""

from scripts.nexus_health import build_report
from scripts.nexus_dashboard import render


def main() -> int:
    report = build_report()
    assert report["schema"] == "nexus-health/v2"
    assert report["diagnostics"]
    assert all(
        "action" in item and "next_step" in item
        for item in report["diagnostics"]
    )

    dashboard = render(report)
    assert "Gungv-Nexus Health" in dashboard
    assert "BLOCKED" in dashboard
    assert "external execution remains disabled by default" in dashboard

    print("NEXUS_DIAGNOSTIC_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
