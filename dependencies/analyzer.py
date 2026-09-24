"""Lightweight dependency and impact analysis."""
from dataclasses import dataclass
@dataclass
class Impact:
    target: str
    changed_paths: list[str]
    affected_roles: list[str]
    risk: str
class DependencyAnalyzer:
    def analyze(self, target, changed_paths, registry):
        affected=[]
        for item in registry:
            if item["name"] == target: continue
            role=item.get("role","")
            if any(p.endswith(".py") and "api" in role for p in changed_paths): affected.append(role)
        risk="high" if len(affected)>2 else ("medium" if affected else "low")
        return Impact(target, list(changed_paths), affected, risk)
