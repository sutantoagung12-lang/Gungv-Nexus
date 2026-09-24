import json
from pathlib import Path
from context.compiler import ContextCompiler
from memory.store import MemoryStore
from knowledge.store import KnowledgeStore
from agents.orchestrator import Orchestrator
from security.policy import SecurityPolicy
from telemetry.logger import Telemetry

class NexusRuntime:
    def __init__(self, root="."):
        self.root=Path(root)
        self.memory=MemoryStore(str(self.root/"memory/data"))
        self.knowledge=KnowledgeStore(str(self.root/"knowledge/data/claims.jsonl"))
        self.context=ContextCompiler()
        self.orchestrator=Orchestrator()
        self.security=SecurityPolicy()
        self.telemetry=Telemetry(str(self.root/"telemetry/events.jsonl"))

    def handle(self, user_input: str):
        agents=self.orchestrator.select(user_input)
        ctx=self.context.compile(user_input, memories=self.memory.search(user_input), knowledge=self.knowledge.search(user_input))
        self.telemetry.emit("task_received", input=user_input, agents=agents)
        return {"input":user_input,"agents":agents,"context":ctx.__dict__}

    def health(self):
        return {"status":"ok","memory_records":len(self.memory.all()),"knowledge_records":len(self.knowledge.all())}
