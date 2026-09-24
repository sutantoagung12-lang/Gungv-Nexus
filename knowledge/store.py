import json
from pathlib import Path

class KnowledgeStore:
    def __init__(self, path="knowledge/data/claims.jsonl"):
        self.path=Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
    def add(self, record):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False)+"\n")
    def all(self):
        if not self.path.exists(): return []
        return [json.loads(x) for x in self.path.read_text(encoding="utf-8").splitlines() if x.strip()]
    def search(self, query, limit=10):
        q=set(query.lower().split()); scored=[]
        for r in self.all():
            text=(r.get("content","")+" "+r.get("type","")).lower(); score=sum(1 for w in q if w in text)
            if score: scored.append((score,r))
        scored.sort(key=lambda x:x[0], reverse=True)
        return [r for _,r in scored[:limit]]
