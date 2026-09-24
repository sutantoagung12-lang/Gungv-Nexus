import json
from pathlib import Path
from kernel.models import Memory

class MemoryStore:
    def __init__(self, root: str = "memory/data"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "memories.jsonl"

    def add(self, memory: Memory):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(memory.to_dict(), ensure_ascii=False) + "\n")
        return memory

    def all(self):
        if not self.path.exists(): return []
        rows=[]
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip(): rows.append(json.loads(line))
        return rows

    def search(self, query: str, limit: int = 10):
        q = set(query.lower().split())
        scored=[]
        for row in self.all():
            words=set(row.get("content","").lower().split())
            score=len(q & words)
            if score: scored.append((score,row))
        scored.sort(key=lambda x:x[0], reverse=True)
        return [row for _,row in scored[:limit]]
