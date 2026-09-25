"""Attention selection based on explicit task signals."""

class AttentionEngine:
    def __init__(self, limit: int = 8):
        self.limit = max(1, int(limit))

    def select(self, items, keywords):
        scored = []
        for item in items:
            text = str(item).lower()
            scored.append((sum(k.lower() in text for k in keywords), item))
        return [x[1] for x in sorted(scored, key=lambda x: x[0], reverse=True)[: self.limit]]

    def focus(self, task: str, memories: list, knowledge: list) -> dict:
        keywords = [token for token in str(task).lower().split() if len(token) > 2]
        combined = list(memories) + list(knowledge)
        selected = self.select(combined, keywords)
        return {
            "budget": self.limit,
            "task": task,
            "keywords": keywords[:self.limit],
            "selected": selected[:self.limit],
        }
