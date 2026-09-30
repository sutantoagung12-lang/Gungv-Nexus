from core.agent_controller import NexusAgent


def test_unified_agent_has_single_control_loop():
    agent = NexusAgent()
    decision = agent.plan("research and improve autonomous AI capabilities")
    assert decision.status == "PLANNED"
    assert decision.plan[0] == "WAKE"
    assert "POLICY_CHECK" in decision.plan
    assert decision.plan[-1] == "SLEEP"
    assert decision.guardrails["fail_closed"] is True


def test_unified_agent_blocks_external_execution_by_policy():
    status = NexusAgent().status()
    assert status["mode"] == "unified-single-agent"
