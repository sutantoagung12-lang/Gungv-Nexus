from nexus.audit import AuditLog
from nexus.health import snapshot
from nexus.orchestrator import Orchestrator
from nexus.registry import Registry, Worker


def test_audit_event_is_recorded():
    log = AuditLog()
    event = log.record("inspect", "sutantoagung12-lang/Gungv")
    assert event.action == "inspect"
    assert len(log.list()) == 1


def test_health_counts_online_workers():
    registry = Registry()
    registry.register_worker(Worker("w1", "local", status="online"))
    registry.register_worker(Worker("w2", "offline", status="offline"))
    data = snapshot(registry, Orchestrator(registry))
    assert data["workers"] == 2
    assert data["online_workers"] == 1
