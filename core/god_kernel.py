"""GOD-CORE Kernel: single coordination surface for Nexus organs."""
from typing import Any
from core.god_core import GodCore
from core.god_lifecycle import GodLifecycle
from core.god_signal_router import GodSignalRouter
from core.body_system import NexusBody
from core.self_awareness_loop import SelfAwarenessLoop
from core.skill_orchestrator import SkillOrchestrator
from core.daily_skill_frontier import DailySkillFrontier


class GodKernel:
    def __init__(self, nexus: Any):
        self.nexus = nexus
        self.god = GodCore(nexus)
        self.lifecycle = GodLifecycle(self.god)
        self.signals = GodSignalRouter(self.god)
        self.body = NexusBody()
        self.awareness = SelfAwarenessLoop(nexus, self.god)
        self.skills = SkillOrchestrator()
        self.frontier = DailySkillFrontier()
        self._wire()

    def _wire(self):
        self.signals.on(
            "HEARTBEAT",
            lambda s: self.nexus.nervous_system.emit("HEARTBEAT", s.payload, "god-core"),
        )
        self.signals.on(
            "ERROR",
            lambda s: self.nexus.nervous_system.emit("ERROR", s.payload, s.source),
        )

    def run(self, task: str):
        self.signals.emit("TASK_RECEIVED", {"task": task}, "god-kernel")
        skill_plan = self.skills.plan(task)
        awareness = self.awareness.update(task)
        result = self.lifecycle.run(task)
        result["awareness"] = awareness.__dict__
        result["skill_plan"] = skill_plan
        self.awareness.reflect(
            {
                "task": task,
                "verified": result["verified"],
                "status": result["status"],
                "cycle": self.god.state.cycle,
                "skills_selected": skill_plan["selected"],
            }
        )
        self.signals.emit(
            "TASK_VERIFIED",
            {
                "task": task,
                "verified": result["verified"],
                "skills_selected": skill_plan["selected"],
            },
            "god-kernel",
        )
        return result

    def daily_frontier(self, candidates: list[dict[str, Any]]):
        return self.frontier.daily_cycle(candidates)

    def pulse(self):
        return self.signals.pulse()

    def map_body(self):
        return self.body.map()

    def awareness_status(self):
        return self.awareness.status()

    def reflect(self, observation: Any):
        return self.awareness.reflect(observation)

    def status(self):
        return {
            "mode": self.god.state.mode,
            "cycle": self.god.state.cycle,
            "organs": len(self.body.map()),
            "signals": len(self.signals.history),
            "awareness": self.awareness.status(),
            "skills_registered": len(self.skills.skills),
            "frontier_policy": "daily-frontier",
        }
