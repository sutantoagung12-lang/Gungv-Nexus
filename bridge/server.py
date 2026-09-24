"""Gungv-Nexus bridge and Instagram OAuth entry point."""
import json
import os
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from integrations.instagram.connector import (
    InstagramConfig,
    InstagramConnectorError,
    authorization_url,
    exchange_code,
    exchange_long_lived,
    profile,
)

ROOT = Path(__file__).resolve().parents[1]
OAUTH_STATES = {}
CONNECTED = {}

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def bootstrap():
    state = load("state/system-state.json")
    registry = load("github/registry/repositories.json")
    topology = load("github/topology/topology.json")
    return {
        "bridge_version": "1.1.0",
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

def result_page(title, detail, error=False):
    cls = "color:#ff8a8a;" if error else ""
    return ("<!doctype html><html lang='id'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<body style='background:#111;color:#fff;font:16px system-ui;padding:32px'>"
            "<h1>" + title + "</h1><p style='" + cls + "'>" + detail + "</p>"
            "<p>Gungv-Nexus</p></body></html>")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/instagram":
            body = (ROOT / "bridge" / "instagram_connect.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        if parsed.path == "/instagram/connect":
            try:
                config = InstagramConfig.from_env()
                url, state = authorization_url(config)
                OAUTH_STATES[state] = time.time()
                self.json_response({"authorization_url": url})
            except InstagramConnectorError as exc:
                self.json_response({"error": str(exc)}, 503)
            return

        if parsed.path == "/instagram/callback":
            params = urllib.parse.parse_qs(parsed.query)
            state = params.get("state", [None])[0]
            code = params.get("code", [None])[0]
            error = params.get("error_description", [None])[0] or params.get("error", [None])[0]
            if error:
                self.html_response(result_page("Instagram login cancelled.", error, True))
                return
            issued = OAUTH_STATES.pop(state, None) if state else None
            if not code or issued is None or time.time() - issued > 600:
                self.html_response(result_page("Connection failed.", "Invalid or expired OAuth state.", True), 400)
                return
            try:
                config = InstagramConfig.from_env()
                short = exchange_code(config, code)
                short_token = short.get("access_token")
                if not short_token:
                    raise InstagramConnectorError("Instagram did not return an access token.")
                long_lived = exchange_long_lived(config, short_token)
                token = long_lived.get("access_token", short_token)
                account = profile(config, token)
                key = account.get("id") or account.get("user_id") or "connected"
                CONNECTED[key] = {"profile": account, "access_token": token, "connected_at": int(time.time())}
                self.html_response(result_page("Instagram connected.", account.get("username", "Account connected")))
            except InstagramConnectorError as exc:
                self.html_response(result_page("Connection failed.", str(exc), True), 502)
            return

        if parsed.path not in ("/bootstrap", "/health"):
            self.send_response(404)
            self.end_headers()
            return

        if parsed.path == "/health":
            body = b'{"status":"ok","service":"gungv-nexus-bridge"}'
        else:
            body = json.dumps(bootstrap(), ensure_ascii=False).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def html_response(self, body, status=200):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_):
        pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8787"))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
