"""Build a sanitized public bootstrap snapshot. Never copy private repository topology."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
state=json.loads((ROOT/"state/system-state.json").read_text(encoding="utf-8"))
out={
 "bridge_version":"2.0.0",
 "architecture_version":state.get("architecture_version"),
 "health":state.get("health"),
 "capabilities":state.get("capabilities",[]),
 "safety":{
  "external_data":"untrusted_until_validated",
  "destructive_actions":"confirmation_required",
  "unknown_state":"do_not_invent",
  "human_authority":True
 },
 "bootstrap_endpoint":"/bootstrap.json"
}
site=ROOT/"bridge/site"
site.mkdir(parents=True,exist_ok=True)
(site/"bootstrap.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(site/"index.html").write_text("""<!doctype html><meta charset="utf-8"><title>Gungv-Nexus Bridge</title><h1>Gungv-Nexus Bridge</h1><p>Sanitized read-only bootstrap endpoint.</p><p><a href="bootstrap.json">bootstrap.json</a></p>""",encoding="utf-8")
print("built sanitized bridge")
