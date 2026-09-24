"""PydanticAI adapter boundary."""
class PydanticAIAdapter:
    name = "PydanticAI"
    def status(self):
        try:
            import pydantic_ai  # type: ignore
        except ImportError:
            return {"name": self.name, "available": False, "active": False}
        return {"name": self.name, "available": True, "active": True}
