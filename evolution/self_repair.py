"""Guarded self-repair planning for Nexus v27.

Generates repair candidates from failures, but only promotes a candidate after
deterministic validation. The engine never bypasses repository safety gates.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256


@dataclass
class RepairCandidate:
    repair_id: str
    target: str
    diagnosis: str
    change: str
    evidence: list[str]
    confidence: float
    status: str = "PROPOSED"
    created_at: str = ""


class SelfRepairEngine:
    MIN_EVIDENCE = 2
    MIN_CONFIDENCE = 0.85

    def diagnose(self, failure: dict) -> RepairCandidate:
        target = str(failure.get("target", "unknown"))
        diagnosis = str(failure.get("diagnosis") or failure.get("error") or "unclassified failure")
        change = str(failure.get("suggested_change") or "isolate, test, and revise the failing component")
        evidence = [str(x) for x in failure.get("evidence", []) if str(x).strip()]
        confidence = float(failure.get("confidence", 0.0))
        seed = f"{target}|{diagnosis}|{change}".lower().encode()
        repair_id = sha256(seed).hexdigest()[:16]
        return RepairCandidate(
            repair_id=repair_id,
            target=target,
            diagnosis=diagnosis,
            change=change,
            evidence=evidence,
            confidence=confidence,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def validate(self, candidate: RepairCandidate, *, tests_passed: bool, regression_free: bool) -> dict:
        enough_evidence = len(candidate.evidence) >= self.MIN_EVIDENCE
        safe_confidence = candidate.confidence >= self.MIN_CONFIDENCE
        if tests_passed and regression_free and enough_evidence and safe_confidence:
            candidate.status = "READY_FOR_PROMOTION"
        else:
            candidate.status = "REJECTED"
        return {
            **asdict(candidate),
            "gates": {
                "tests_passed": tests_passed,
                "regression_free": regression_free,
                "enough_evidence": enough_evidence,
                "safe_confidence": safe_confidence,
            },
        }
