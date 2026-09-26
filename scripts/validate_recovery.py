#!/usr/bin/env python3
"""Validate every built-in Nexus recovery strategy."""

import json
import sys
from pathlib import Path

from scripts.nexus_recovery_validator import validate_all_recovery_plans


def main() -> int:
    results = validate_all_recovery_plans()
    failures = [item for item in results if not item["validation"]["valid"]]
    document = {
        "schema": "nexus-recovery-validation/v1",
        "overall": "FAIL" if failures else "PASS",
        "plans": results,
        "execution": "validation-only",
        "external_execution": False,
    }

    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(document, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
