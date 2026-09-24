"""Google ADK adapter boundary."""
class GoogleADKAdapter:
    name = "Google ADK"
    def status(self):
        try:
            import google.adk  # type: ignore
        except ImportError:
            return {"name": self.name, "available": False, "active": False}
        return {"name": self.name, "available": True, "active": True}
