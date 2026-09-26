from integrations.agenticseek_bridge import AgenticSeekBridge


def test_browser_and_coder_roles_are_composed():
    profile = AgenticSeekBridge().profile("browse the web and write a Python program")
    names = [role["nexus_agent"] for role in profile["roles"]]
    assert "planner" in names
    assert "browser" in names
    assert "coder" in names


def test_unknown_task_stays_planner_only():
    profile = AgenticSeekBridge().profile("say hello")
    assert [role["nexus_agent"] for role in profile["roles"]] == ["planner"]


def test_bridge_does_not_execute():
    profile = AgenticSeekBridge().profile("execute a tool")
    assert profile["execution"] == "delegated-to-nexus"
    assert profile["destructive_actions"] == "confirmation-gated"


from integrations.agenticseek_browser_loop import AgenticSeekBrowserLoop


def test_browser_loop_is_planned_but_not_executed():
    loop = AgenticSeekBrowserLoop()
    result = loop.start("find a public documentation page")
    assert result["state"]["stage"] == "plan"
    assert result["execution"] == "delegated-to-nexus-worker"
    assert result["action_request"]["executed"] is False


def test_browser_loop_covers_observe_reason_action_verify():
    loop = AgenticSeekBrowserLoop()
    state = loop.start("find a public documentation page")["state"]
    state = loop.observe(state, "Search results were returned.")
    assert state["stage"] == "reason"
    state = loop.reason(state, "Choose the documentation result.")
    assert state["stage"] == "action"
    state = loop.prepare_action(state, {"type": "open", "target": "documentation"})
    assert state["stage"] == "verify"
    state = loop.verify(state, "Documentation page loaded.")
    assert state["stage"] == "complete"
