"""Minimal read-only bridge for Gungv-Nexus bootstrap context.

The service exposes only context retrieval. It does not execute repository changes.
Deploy behind authentication before exposing it publicly.
"""
import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def bootstrap():
    state = load("state/system-state.json")
    registry = load("github/registry/repositories.json")
    topology = load("github/topology/topology.json")
    return {
        "bridge_version": "1.0.0",
        "architecture_version": state.get("architecture_version"),
        "health": state.get("health"),
        "evolution_state": state.get("evolution_state"),
        "capabilities": state.get("capabilities", []),
        "repositories": registry,
        "topology": topology,
        "safety": {
            "external_data": "untrusted_until_validated",
            "destructive_actions": "confirmation_required",
            "unknown_state": "do_not_invent",
            "human_authority": True,
        },
    }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/bootstrap", "/health"):
            self.send_response(404)
            self.end_headers()
            return
        if self.path == "/health":
            body = b'{"status":"ok","service":"gungv-nexus-bridge"}'
        else:
            body = json.dumps(bootstrap(), ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8787), Handler).serve_forever()
