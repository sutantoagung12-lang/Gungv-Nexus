from integrations.agenticseek_browser_loop import AgenticSeekBrowserLoop
from integrations.adapters.android_chrome import AndroidChromeWorker
from agents.orchestrator import Orchestrator


def test_browser_loop_rejects_invalid_transition():
    loop = AgenticSeekBrowserLoop()
    state = loop.start("find a public documentation page")["state"]
    try:
        loop.verify(state, "not ready")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid browser transition must be rejected")


def test_browser_loop_rejects_empty_action():
    loop = AgenticSeekBrowserLoop()
    state = loop.start("find a public documentation page")["state"]
    state = loop.observe(state, "Search results were returned.")
    state = loop.reason(state, "Choose the documentation result.")
    try:
        loop.prepare_action(state, {})
    except ValueError:
        pass
    else:
        raise AssertionError("empty browser action must be rejected")


def test_orchestrator_browser_preparation_exposes_worker_boundary():
    result = Orchestrator().prepare_browser_task("browse a website and read the page")
    assert result["execution"] == "delegated-to-nexus-worker"
    assert result["worker"]["name"] == "android-chrome-cdp"
    assert result["worker"]["requires_authorization"] is True
    assert result["action_request"]["executed"] is False


def test_android_chrome_worker_never_executes_without_approval():
    worker = AndroidChromeWorker("http://127.0.0.1:9222")
    try:
        worker.execute({"type": "snapshot"}, approved=False)
    except PermissionError as exc:
        assert "explicit approval" in str(exc)
    else:
        raise AssertionError("worker must require explicit approval")
