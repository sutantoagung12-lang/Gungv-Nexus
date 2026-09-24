"""Quality-aware reflection and lesson synthesis."""
from __future__ import annotations


def reflect(task: str, outcome: dict, prior_lessons: list[dict] | None = None) -> dict:
    success = bool(outcome.get("success", False))
    quality = float(outcome.get("quality", 0.0))
    reward = float(outcome.get("reward", 0.0))
    errors = outcome.get("errors", [])
    if success and quality >= 0.8:
        lesson = f"Successful strategy for: {task}"
        kind = "procedural"
    elif errors:
        lesson = f"Avoid failure pattern on {task}: {errors[0]}"
        kind = "corrective"
    else:
        lesson = f"Review strategy for: {task}"
        kind = "strategic"
    return {
        "task": task,
        "type": kind,
        "lesson": lesson,
        "confidence": round(max(0.0, min(1.0, 0.5 * quality + 0.5 * reward)), 4),
        "evidence_count": len(prior_lessons or []),
    }
