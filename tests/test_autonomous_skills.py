#!/usr/bin/env python3
"""Dependency-light tests for the autonomous skill control plane.

These tests do not execute external skill repositories or external actions.
"""
from integrations.autonomous_skill_resolver import resolve_autonomous_skills
from integrations.autonomous_runtime import AutonomousRuntime


def test_resolver_selects_autonomous_sources():
    result = resolve_autonomous_skills("autonomous research and evaluation")
    assert result
    assert all(item["readiness"] == "reference" for item in result)
    assert all(item["execution_allowed"] is False for item in result)


def test_runtime_builds_lifecycle_plan():
    result = AutonomousRuntime().plan("autonomous research")
    assert result["autonomous"] is True
    assert result["lifecycle_phases"]
    assert result["promotion"] == "validation-gated"
    assert result["rollback"] == "last-verified-checkpoint"
