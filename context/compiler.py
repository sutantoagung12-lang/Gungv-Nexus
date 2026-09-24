from dataclasses import dataclass, field
from typing import Any

@dataclass
class Context:
    user_input: str
    goals: list[dict[str, Any]] = field(default_factory=list)
    memories: list[dict[str, Any]] = field(default_factory=list)
    knowledge: list[dict[str, Any]] = field(default_factory=list)
    repositories: list[dict[str, Any]] = field(default_factory=list)
    policies: list[str] = field(default_factory=list)

class ContextCompiler:
    """Build a bounded context from persisted system state and relevant records."""
    def compile(self, user_input: str, *, goals=None, memories=None, knowledge=None, repositories=None, policies=None):
        return Context(
            user_input=user_input,
            goals=list(goals or []),
            memories=list(memories or []),
            knowledge=list(knowledge or []),
            repositories=list(repositories or []),
            policies=list(policies or []),
        )
