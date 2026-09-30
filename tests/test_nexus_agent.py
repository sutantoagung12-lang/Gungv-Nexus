from core.nexus_agent import GungvNexusAgent


def test_nexus_is_one_agent():
    agent = GungvNexusAgent()
    result = agent.think("research autonomous AI and improve capabilities")
    assert result.stage == "PLAN"
    assert result.lifecycle[0] == "WAKE"
    assert result.lifecycle[-1] == "SLEEP"
    assert result.guards["fail_closed"] if "fail_closed" in result.guards else result.guards["failure"] == "fail_closed"


def test_nexus_contract_is_unified():
    contract = GungvNexusAgent().contract()
    assert contract["architecture"] == "one-agent-composed-system"
    assert contract["principle"] == "one decision surface, modular internal organs"
