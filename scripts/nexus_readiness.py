#!/usr/bin/env python3
"""Validate Nexus recovery plans and produce a final readiness document."""

import json
import sys
from pathlib import Path

from scripts.nexus_health import build_report
from scripts.nexus_recovery_report import build_recovery_document
from scripts.nexus_recovery_validator import validate_all_recovery_plans


def main() -> int:
    health = build_report()
    recovery = build_recovery_document()
    validations = validate_all_recovery_plans()

    validation_failures = [x for x in validations if not x["validation"]["valid"]]
    document = {
        "schema": "nexus-readiness/v1",
        "health": {
            "schema": health["schema"],
            "overall": health["overall"],
            "summary": health["summary"],
        },
        "recovery": {
            "schema": recovery["schema"],
            "execution": recovery["execution"],
            "plan_count": len(recovery["recovery_plans"]),
        },
        "recovery_validation": {
            "schema": "nexus-recovery-validation/v1",
            "overall": "FAIL" if validation_failures else "PASS",
            "plan_count": len(validations),
            "failure_count": len(validation_failures),
        },
        "external_execution": False,
        "production_readiness_claimed": False,
    }

    document["overall"] = (
        "PASS"
        if health["overall"] == "PASS" and not validation_failures
        else "ATTENTION"
    )

    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(document, indent=2))
    return 1 if validation_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
