import json
from pathlib import Path
from datetime import datetime, timezone

class Telemetry:
    def __init__(self, path="telemetry/events.jsonl"):
        self.path=Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
    def emit(self, event, **data):
        row={"timestamp":datetime.now(timezone.utc).isoformat(),"event":event,**data}
        with self.path.open("a",encoding="utf-8") as f: f.write(json.dumps(row,ensure_ascii=False)+"\n")
        return row
