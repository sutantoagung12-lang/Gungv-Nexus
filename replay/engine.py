"""Replay recorded telemetry without side effects."""
import json
def load_events(path):
    try:
        with open(path,encoding="utf-8") as f: return [json.loads(x) for x in f if x.strip()]
    except FileNotFoundError: return []
def summarize(events):
    return {"count":len(events),"types":sorted({e.get("event") for e in events if e.get("event")})}
