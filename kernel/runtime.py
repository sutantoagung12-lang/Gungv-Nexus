import json
from pathlib import Path
from context.compiler import ContextCompiler
from memory.store import MemoryStore
from knowledge.store import KnowledgeStore
from agents.orchestrator import Orchestrator
from security.policy import SecurityPolicy
from telemetry.logger import Telemetry
from agents.execution import ExecutionEngine
from evaluation.engine import Evaluator
from evolution.learning import LearningLoop
from cognition.attention import AttentionEngine
from cognition.power import PowerEngine

class NexusRuntime:
    def __init__(self, root="."):
        self.root=Path(root)
        self.memory=MemoryStore(str(self.root/"memory/data"))
        self.knowledge=KnowledgeStore(str(self.root/"knowledge/data/claims.jsonl"))
        self.context=ContextCompiler()
        self.orchestrator=Orchestrator()
        self.security=SecurityPolicy()
        self.telemetry=Telemetry(str(self.root/"telemetry/events.jsonl"))
        self.execution=ExecutionEngine(self)
        self.evaluator=Evaluator()
        self.learning=LearningLoop(self)
        self.attention=AttentionEngine(limit=8)
        self.power=PowerEngine(self)

    def handle(self, user_input: str):
        agents=self.orchestrator.select(user_input)
        ctx=self.context.compile(user_input, memories=self.memory.search(user_input), knowledge=self.knowledge.search(user_input))
        self.telemetry.emit("task_received", input=user_input, agents=agents)
        return {"input":user_input,"agents":agents,"context":ctx.__dict__}

    def run_cycle(self, goal: str, task: str):
        from cognition.orchestration import OrchestrationCycle
        cycle = OrchestrationCycle(self).run(goal, task)
        evaluation = self.evaluator.run(checks={
            "cycle_created": bool(cycle.get("cycle_id")),
            "agents_selected": bool(cycle.get("agents")),
            "context_compiled": bool(cycle.get("context"))
        })
        execution = self.execution.execute("record_memory", {
            "id": cycle["cycle_id"] + "-result",
            "type": "execution-result",
            "content": f"Cycle evaluated: {evaluation.passed}",
            "status": "COMPLETED"
        })
        learning = self.learning.learn(
            cycle_id=cycle["cycle_id"], goal=goal, task=task,
            evaluation={"passed": evaluation.passed}
        )
        return {
            "cycle": cycle,
            "evaluation": evaluation.__dict__,
            "execution": execution,
            "learning": learning
        }

    def power_plan(self, objective: str, task: str):
        return self.power.plan(objective, task)

    def health(self):
        return {"status":"ok","memory_records":len(self.memory.all()),"knowledge_records":len(self.knowledge.all())}
