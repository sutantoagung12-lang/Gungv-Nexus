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
