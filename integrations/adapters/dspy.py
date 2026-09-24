"""DSPy adapter boundary."""
class DSPyAdapter:
    name = "DSPy"
    def status(self):
        try:
            import dspy  # type: ignore
        except ImportError:
            return {"name": self.name, "available": False, "active": False}
        return {"name": self.name, "available": True, "active": True}
