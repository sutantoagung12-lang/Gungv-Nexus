from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import uuid

@dataclass
class ActionResult:
    action_id: str
    action: str
    status: str
    output: object = None
    error: str = ""

class ExecutionEngine:
    SAFE_ACTIONS = {"record_memory", "record_knowledge", "emit_telemetry"}

    def __init__(self, runtime):
        self.runtime = runtime

    def execute(self, action: str, payload=None):
        action_id = str(uuid.uuid4())
        payload = payload or {}
        if action not in self.SAFE_ACTIONS:
            result = ActionResult(action_id, action, "BLOCKED", error="action requires explicit confirmation or an approved adapter")
            self.runtime.telemetry.emit("action_blocked", action_id=action_id, action=action)
            return asdict(result)

        if action == "record_memory":
            output = self.runtime.memory.add(payload)
        elif action == "record_knowledge":
            output = self.runtime.knowledge.add(payload)
        else:
            output = self.runtime.telemetry.emit("external_action", **payload)

        result = ActionResult(action_id, action, "COMPLETED", output=output)
        self.runtime.telemetry.emit("action_completed", action_id=action_id, action=action)
        return asdict(result)
