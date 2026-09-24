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
from memory.intelligence import MemoryIntelligence
from knowledge.intelligence import KnowledgeIntelligence
from governance.gate import ChangeGate
from evaluation.quality import QualityEvaluator
from cognition.runtime_loop import CognitiveRuntimeLoop
from economics.opportunity import OpportunityEngine
from research.loop import ResearchLoop
from recovery.checkpoint import CheckpointManager

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
        self.memory_intelligence_engine=MemoryIntelligence(self)
        self.knowledge_intelligence_engine=KnowledgeIntelligence(self)
        self.change_gate_engine=ChangeGate()
        self.quality_engine=QualityEvaluator()
        self.cognitive_loop=CognitiveRuntimeLoop(self)
        self.opportunity_engine=OpportunityEngine()
        self.research_loop=ResearchLoop(self)
        self.checkpoints=CheckpointManager(self)

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

    def memory_intelligence(self):
        return self.memory_intelligence_engine.analyze()

    def memory_consolidation(self, limit=100):
        return self.memory_intelligence_engine.consolidate(limit)

    def knowledge_intelligence(self):
        return self.knowledge_intelligence_engine.analyze()

    def change_gate(self, action):
        return self.change_gate_engine.assess(action)

    def quality_evaluate(self, result):
        return self.quality_engine.evaluate(result)

    def cognitive_cycle(self, objective: str, task: str):
        return self.cognitive_loop.run(objective, task)

    def opportunities(self, opportunities):
        return self.opportunity_engine.evaluate(opportunities)

    def research_prepare(self, question, sources=None):
        return self.research_loop.prepare(question, sources)

    def checkpoint_save(self, task_id, state):
        return self.checkpoints.save(task_id, state)

    def checkpoint_load(self, task_id):
        return self.checkpoints.load(task_id)

    def health(self):
        return {"status":"ok","memory_records":len(self.memory.all()),"knowledge_records":len(self.knowledge.all())}
