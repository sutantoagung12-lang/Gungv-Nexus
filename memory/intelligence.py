"""Memory Intelligence 2.0: consolidation, conflict detection and decay."""
from collections import defaultdict
from datetime import datetime, timezone

class MemoryIntelligence:
    def __init__(self, runtime):
        self.runtime=runtime

    def analyze(self):
        rows=self.runtime.memory.all()
        conflicts=[]
        by_key=defaultdict(list)
        for r in rows:
            key=str(r.get("topic") or r.get("kind") or r.get("type") or "")
            by_key[key].append(r)
        for key,items in by_key.items():
            statuses={str(x.get("status","")) for x in items}
            if len(items)>1 and len(statuses)>1:
                conflicts.append({"key":key,"records":[x.get("id") for x in items],"statuses":sorted(statuses)})
        return {"records":len(rows),"conflicts":conflicts,"conflict_count":len(conflicts)}

    def consolidate(self, limit=100):
        rows=self.runtime.memory.all()[-limit:]
        seen={}
        merged=[]
        for r in rows:
            content=str(r.get("content","")).strip()
            if not content: continue
            key=content.lower()
            if key in seen:
                continue
            seen[key]=r
            merged.append(r)
        return {"input_records":len(rows),"unique_records":len(merged),"duplicates_removed":len(rows)-len(merged),
                "generated_at":datetime.now(timezone.utc).isoformat()}
