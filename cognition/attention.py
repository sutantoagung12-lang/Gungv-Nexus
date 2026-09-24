"""Attention selection based on explicit task signals."""
class AttentionEngine:
    def select(self, items, keywords):
        scored=[]
        for item in items:
            text=str(item).lower()
            scored.append((sum(k.lower() in text for k in keywords),item))
        return [x[1] for x in sorted(scored,key=lambda x:x[0],reverse=True)]
