"""Mobile-friendly HTTP server for the AI Live Host MVP."""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core import Event, HostController  # noqa: E402
from youtube import YouTubeError, YouTubeLive  # noqa: E402

controller = HostController()


def read_json(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", "0"))
    if length > 64_000:
        raise ValueError("payload too large")
    raw = handler.rfile.read(length) if length else b"{}"
    return json.loads(raw.decode("utf-8"))


class Handler(BaseHTTPRequestHandler):
    def send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, body: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_html((ROOT / "dashboard.html").read_bytes())
        elif parsed.path == "/scene":
            self.send_html((ROOT / "live_scene.html").read_bytes())
        elif parsed.path == "/health":
            self.send_json({"status": "ok", "service": "ai-live-host"})
        elif parsed.path == "/api/status":
            self.send_json(controller.status())
        elif parsed.path == "/api/scene":
            since = parse_qs(parsed.query).get("since", [""])[0]
            event = controller.events[-1] if controller.events else None
            if event is None or event.event_id == since:
                self.send_json({})
            else:
                response = controller.memory.messages[-1]["text"] if controller.memory.messages else ""
                self.send_json({
                    "event_id": event.event_id, "kind": event.kind, "user": event.user,
                    "response": response,
                })
        else:
            self.send_json({"error": "not_found"}, 404)

    def do_POST(self) -> None:
        try:
            data = read_json(self)
            if self.path == "/api/start":
                self.send_json(controller.start())
                return
            if self.path == "/api/stop":
                self.send_json(controller.stop())
                return
            if self.path in {"/api/chat", "/api/respond"}:
                event = Event(kind="chat", text=str(data.get("text", ""))[:1000], user=str(data.get("user", ""))[:100])
                controller.ingest(event)
                self.send_json({"event_id": event.event_id, "response": controller.respond(event)})
                return
            if self.path == "/api/support":
                amount = float(data.get("amount", 0))
                if amount < 0 or amount > 1_000_000_000:
                    raise ValueError("invalid amount")
                event = Event(kind="support", text=str(data.get("text", ""))[:500],
                              user=str(data.get("user", ""))[:100], amount=amount,
                              currency=str(data.get("currency", "IDR"))[:10])
                controller.ingest(event)
                self.send_json({"event_id": event.event_id, "response": controller.respond(event)})
                return
            if self.path == "/api/demo":
                event = Event(kind="chat", text="Halo AI, jelaskan cara kerja live ini.", user="demo")
                controller.ingest(event)
                self.send_json({"event_id": event.event_id, "response": controller.respond(event)})
                return
            if self.path == "/api/youtube/chat":
                message = str(data.get("message", ""))[:500]
                if not message:
                    raise ValueError("message is required")
                yt = YouTubeLive()
                if controller.dry_run:
                    self.send_json({"dry_run": True, "would_send": message})
                    return
                self.send_json(yt.send_chat(message))
                return
            self.send_json({"error": "not_found"}, 404)
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json({"error": str(exc)}, 400)
        except YouTubeError as exc:
            self.send_json({"error": str(exc)}, 502)
        except Exception as exc:
            self.send_json({"error": "internal_error", "detail": str(exc)}, 500)

    def log_message(self, *_args) -> None:
        pass


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8790"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
