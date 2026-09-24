from dataclasses import dataclass, field

@dataclass
class Evaluation:
    passed: bool
    metrics: dict = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

class Evaluator:
    def run(self, *, checks: dict[str,bool], metrics=None):
        failed=[k for k,v in checks.items() if not v]
        return Evaluation(not failed, metrics or {}, [f"failed:{x}" for x in failed])
