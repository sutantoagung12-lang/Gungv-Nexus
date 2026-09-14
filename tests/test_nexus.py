from nexus.orchestrator import Orchestrator
from nexus.policy import DEFAULT_POLICY
from nexus.registry import Registry, Repository


def test_registry_and_job_submission():
    registry = Registry()
    registry.register_repository(Repository("Gungv", "sutantoagung12-lang/Gungv"))
    nexus = Orchestrator(registry)
    job = nexus.submit("pull_request", "sutantoagung12-lang/Gungv", {"reason": "sync"})
    assert job.status == "queued"
    assert nexus.get(job.job_id) is job


def test_main_write_is_denied_by_default():
    nexus = Orchestrator()
    assert DEFAULT_POLICY.allows("main_write") is False
    try:
        nexus.submit("main_write", "sutantoagung12-lang/Gungv")
    except PermissionError:
        return
    raise AssertionError("direct main write should be denied")
