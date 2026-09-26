#!/usr/bin/env python3
"""Validate guarded Nexus recovery planning."""

from scripts.nexus_health import build_report
from scripts.nexus_recovery import build_recovery_report, plan_recovery


def main() -> int:
    report = build_report()
    plans = build_recovery_report(report["diagnostics"])

    assert plans
    for plan in plans:
        assert plan["steps"]
        assert plan["strategy"]

    approval = plan_recovery(
        "human_approval_required_for_android_chrome_actions"
    )
    assert approval.requires_human_approval is True
    assert "Obtain explicit human approval." in approval.steps

    unknown = plan_recovery("unrecognized_condition")
    assert unknown.strategy == "manual-review"
    assert unknown.requires_human_approval is False

    print("NEXUS_RECOVERY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
