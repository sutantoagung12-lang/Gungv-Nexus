"""Human-body-inspired anatomy map for the unified Nexus agent."""
from dataclasses import dataclass
@dataclass(frozen=True)
class BodyOrgan:
    organ:str; function:str; component:str; vital:bool=True
class NexusBody:
    ORGANS=(
        BodyOrgan('BRAIN','reasoning, planning, decision coordination','core/nexus_agent.py'),
        BodyOrgan('NERVOUS_SYSTEM','events, signals, lifecycle coordination','core/agent_event_bus.py'),
        BodyOrgan('SPINAL_CORD','central execution/state flow','core/agent_cycle.py'),
        BodyOrgan('MEMORY','experience, skills, learned context','core/agent_memory.py'),
        BodyOrgan('SENSORY_SYSTEM','observation and runtime inspection','integrations/runtime.py'),
        BodyOrgan('IMMUNE_SYSTEM','policy, authorization, fail-closed protection','core/agent_policy.py'),
        BodyOrgan('MUSCLES','capability execution and workers','agents/orchestrator.py'),
        BodyOrgan('BLOODSTREAM','task/context/evidence transport','core/agent_state.py'),
        BodyOrgan('HEART','continuous work scheduling','core/agent_scheduler.py'),
        BodyOrgan('LIVER','filtering, validation, promotion control','core/agent_evaluator.py'),
        BodyOrgan('KIDNEYS','checkpoint, cleanup, recovery','core/agent_checkpoint.py'),
        BodyOrgan('LUNGS','external input/output interfaces','integrations/'),
        BodyOrgan('ENDOCRINE_SYSTEM','goals, priorities, long-term regulation','core/agent_goal.py'),
        BodyOrgan('DNA','architecture, contracts, persistent rules','state/system-state.json'),
        BodyOrgan('REPRODUCTIVE_SYSTEM','skill creation and capability evolution','memory/skill_builder.py'),
    )
    @classmethod
    def map(cls): return [o.__dict__ for o in cls.ORGANS]
