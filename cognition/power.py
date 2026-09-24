"""Power-mode cognitive cycle: attention, reasoning context, evaluation and learning."""
from dataclasses import dataclass, asdict

@dataclass
class PowerPlan:
    objective: str
    task: str
    agents: list
    focus: dict
    safeguards: list
    next_steps: list

class PowerEngine:
    def __init__(self, runtime):
        self.runtime=runtime

    def plan(self, objective, task):
        agents=self.runtime.orchestrator.select(task)
        focus=self.runtime.attention.focus(
            task, self.runtime.memory.all(), self.runtime.knowledge.all()
        )
        safeguards=[
            "external_data_untrusted_until_validated",
            "destructive_actions_require_confirmation",
            "unknown_state_must_not_be_invented",
            "human_remains_final_authority"
        ]
        steps=[
            "inspect relevant memory and knowledge",
            "execute only approved safe actions",
            "evaluate result against explicit checks",
            "record durable lesson"
        ]
        return asdict(PowerPlan(objective,task,agents,focus,safeguards,steps))
