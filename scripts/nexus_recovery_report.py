#!/usr/bin/env python3
"""Generate Nexus health plus guarded recovery plans."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from scripts.nexus_health import build_report
from scripts.nexus_recovery import build_recovery_report


def build_recovery_document() -> dict:
    health = build_report()
    return {
        "schema": "nexus-recovery/v1",
        "health_schema": health["schema"],
        "overall": health["overall"],
        "diagnostics": health["diagnostics"],
        "recovery_plans": build_recovery_report(health["diagnostics"]),
        "execution": "plan-only",
        "external_execution": False,
    }


def main() -> int:
    document = build_recovery_document()
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(document, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
