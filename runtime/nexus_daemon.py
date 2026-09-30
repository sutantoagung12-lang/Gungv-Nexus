"""Persistent Nexus runtime loop.

Runs the existing Nexus organism as a long-lived worker.
External/consequential actions remain authorization-gated by the core.
"""
from __future__ import annotations

import os
import signal
import time
from typing import Any

from core.nexus_agent import GungvNexusAgent
from core.god_kernel import GodKernel


class NexusDaemon:
    def __init__(self) -> None:
        self.interval = max(5, int(os.getenv("NEXUS_HEARTBEAT_SECONDS", "30")))
        self.objective = os.getenv(
            "NEXUS_OBJECTIVE",
            "Maintain Nexus health, learn from safe observations, and identify validated improvements.",
        )
        self.running = True
        self.agent = GungvNexusAgent()
        self.kernel = GodKernel(self.agent)

    def stop(self, *_: Any) -> None:
        self.running = False

    def cycle(self) -> dict[str, Any]:
        result = self.kernel.run(self.objective)
        self.kernel.pulse()
        return {
            "status": result.get("status"),
            "verified": result.get("verified"),
            "cycle": self.kernel.god.state.cycle,
            "awareness": self.kernel.awareness.status(),
        }

    def run(self) -> None:
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        print("NEXUS_DAEMON=AWAKE", flush=True)
        while self.running:
            started = time.time()
            try:
                print({"event": "heartbeat", **self.cycle()}, flush=True)
            except Exception as exc:
                self.kernel.signals.emit("ERROR", {"error": str(exc)}, "nexus-daemon")
                print({"event": "error", "error": str(exc)}, flush=True)
            elapsed = time.time() - started
            time.sleep(max(1, self.interval - int(elapsed)))
        print("NEXUS_DAEMON=SLEEP", flush=True)


if __name__ == "__main__":
    NexusDaemon().run()
