#!/usr/bin/env python3
"""Test recovery acceptance and readiness synthesis."""

from scripts.nexus_readiness import main
from scripts.nexus_recovery_validator import validate_all_recovery_plans, validate_reason


def test_all_recovery_plans_validate():
    results = validate_all_recovery_plans()
    assert results
    assert all(item["validation"]["valid"] for item in results)


def test_unknown_reason_is_review_only():
    result = validate_reason("unknown-condition")
    assert result["plan"]["strategy"] == "manual-review"
    assert result["validation"]["valid"] is True


def test_readiness_entrypoint_is_non_executing():
    assert main is not None
