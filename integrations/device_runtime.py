"""Device/runtime capability abstraction inspired by Dextop's adaptive architecture.

This module does not call Android hidden APIs and does not change device state.
It provides Nexus with a portable contract for capability probes, ordered
strategies, and reversible session state. A future Android adapter can plug
into this boundary without making the Python control plane device-specific.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Callable


@dataclass(frozen=True)
class DeviceIdentity:
    manufacturer: str = "unknown"
    model: str = "unknown"
    device: str = "unknown"
    sdk: int | None = None
    environment: str = "unknown"


@dataclass(frozen=True)
class CapabilityResult:
    name: str
    available: bool
    detail: str = ""


@dataclass(frozen=True)
class RuntimeStrategy:
    name: str
    required: tuple[str, ...] = ()
    priority: int = 100


@dataclass
class SessionJournal:
    """Reversible in-memory journal; persistence is owned by the caller."""

    session_id: str
    original_state: dict[str, object] = field(default_factory=dict)
    active: bool = True

    def record(self, key: str, value: object) -> None:
        if key not in self.original_state:
            self.original_state[key] = value

    def restore(self) -> dict[str, object]:
        restored = dict(self.original_state)
        self.active = False
        return restored


class DeviceRuntime:
    """Read-only capability discovery plus ordered, bounded strategy selection."""

    def __init__(self, identity: DeviceIdentity | None = None):
        self.identity = identity or DeviceIdentity()
        self._probes: dict[str, Callable[[], object]] = {}
        self._strategies: list[RuntimeStrategy] = []
        self._sessions: dict[str, SessionJournal] = {}

    def register_probe(self, name: str, probe: Callable[[], object]) -> None:
        if not name or not callable(probe):
            raise ValueError("probe requires a name and callable")
        self._probes[name] = probe

    def register_strategy(self, strategy: RuntimeStrategy) -> None:
        self._strategies.append(strategy)
        self._strategies.sort(key=lambda item: (item.priority, item.name))

    def probe_all(self) -> list[dict]:
        results = []
        for name, probe in sorted(self._probes.items()):
            try:
                value = probe()
                available = bool(value)
                detail = "" if isinstance(value, bool) else str(value)
            except Exception as exc:
                available = False
                detail = f"{type(exc).__name__}: {exc}"
            results.append(asdict(CapabilityResult(name, available, detail)))
        return results

    def available_capabilities(self) -> set[str]:
        return {item["name"] for item in self.probe_all() if item["available"]}

    def select_strategy(self) -> dict:
        available = self.available_capabilities()
        for strategy in self._strategies:
            if set(strategy.required).issubset(available):
                return {
                    "strategy": strategy.name,
                    "required": list(strategy.required),
                    "available": sorted(available),
                }
        return {"strategy": None, "required": [], "available": sorted(available)}

    def start_session(self, session_id: str) -> SessionJournal:
        if not session_id:
            raise ValueError("session_id is required")
        journal = SessionJournal(session_id=session_id)
        self._sessions[session_id] = journal
        return journal

    def restore_session(self, session_id: str) -> dict[str, object]:
        journal = self._sessions.pop(session_id, None)
        if journal is None:
            return {}
        return journal.restore()

    def status(self) -> dict:
        return {
            "identity": asdict(self.identity),
            "capabilities": self.probe_all(),
            "selected_strategy": self.select_strategy(),
            "active_sessions": sorted(self._sessions),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
