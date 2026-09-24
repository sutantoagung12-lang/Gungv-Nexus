"""Immutable snapshot manifest builder."""
from datetime import datetime, timezone
def manifest(repositories):
    return {"created_at":datetime.now(timezone.utc).isoformat(),"repositories":[{"name":r["name"],"branch":r.get("default_branch","main")} for r in repositories]}
