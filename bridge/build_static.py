import json
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"bridge"/"site"
OUT.mkdir(parents=True,exist_ok=True)
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
state=load("state/system-state.json")
registry=load("github/registry/repositories.json")
topology=load("github/topology/topology.json")
snapshot={"bridge_version":"1.1.0","generated_at":datetime.now(timezone.utc).isoformat(),"architecture_version":state.get("architecture_version"),"health":state.get("health"),"evolution_state":state.get("evolution_state"),"capabilities":state.get("capabilities",[]),"repositories":registry,"topology":topology,"safety":{"external_data":"untrusted_until_validated","destructive_actions":"confirmation_required","unknown_state":"do_not_invent","human_authority":True}}
(OUT/"bootstrap.json").write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(OUT/"index.html").write_text("<!doctype html><meta charset='utf-8'><title>Gungv-Nexus Bridge</title><p>Read-only bootstrap endpoint.</p><p><a href='bootstrap.json'>bootstrap.json</a></p>",encoding="utf-8")
