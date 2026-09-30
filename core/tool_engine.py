"""Dynamic tool engine for Nexus. Tools are registered, validated and observed before promotion."""
from dataclasses import dataclass, field
from typing import Any, Callable
@dataclass
class Tool:
    tool_id: str
    name: str
    description: str
    handler: Callable[..., Any]
    status: str = "CANDIDATE"
    evidence: list[dict[str, Any]] = field(default_factory=list)
class ToolEngine:
    def __init__(self): self.tools: dict[str, Tool] = {}
    def register(self, tool_id, name, description, handler):
        if not callable(handler): raise TypeError("handler must be callable")
        tool=Tool(tool_id,name,description,handler); self.tools[tool_id]=tool; return tool
    def validate(self, tool_id, evidence):
        tool=self.tools[tool_id]
        if not evidence: raise ValueError("validation evidence required")
        tool.evidence.append(evidence); tool.status="VALIDATED"; return tool
    def promote(self, tool_id):
        tool=self.tools[tool_id]
        if tool.status!="VALIDATED": raise ValueError("tool must be validated before promotion")
        tool.status="ACTIVE"; return tool
    def execute(self, tool_id, **kwargs):
        tool=self.tools[tool_id]
        if tool.status!="ACTIVE": return {"status":"BLOCKED","reason":"tool_not_active"}
        try:
            result=tool.handler(**kwargs)
            return {"status":"COMPLETED","tool":tool_id,"result":result}
        except Exception as exc:
            return {"status":"FAILED","tool":tool_id,"error":type(exc).__name__}
    def catalog(self):
        return [{"tool_id":t.tool_id,"name":t.name,"status":t.status,"evidence":len(t.evidence)} for t in self.tools.values()]
