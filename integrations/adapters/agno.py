"""Agno adapter boundary."""
class AgnoAdapter:
    name = "Agno"
    def status(self):
        try:
            import agno  # type: ignore
        except ImportError:
            return {"name": self.name, "available": False, "active": False}
        return {"name": self.name, "available": True, "active": True}
