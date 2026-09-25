from integrations.adapters.browser_use import BrowserUseAdapter
from integrations.adapters.khoj import KhojAdapter
from integrations.adapters.langgraph import LangGraphAdapter
from integrations.adapters.r2r import R2RAdapter
from integrations.adapters.stack import status


def test_adapters_are_optional():
    results = status()
    names = {item["name"] for item in results}
    assert {"LangGraph", "R2R", "Khoj", "browser-use"}.issubset(names)
    assert all("available" in item and "active" in item for item in results)


def test_langgraph_plan_is_execution_neutral():
    request = LangGraphAdapter().build_plan("research task", ["researcher", "reviewer"])
    assert request["execution_owner"] == "Gungv-Nexus"
    assert request["nodes"] == ["researcher", "reviewer"]


def test_r2r_and_khoj_requests_validate_input():
    assert R2RAdapter().query_request("nexus", 5)["limit"] == 5
    assert KhojAdapter().search_request("memory", 3)["limit"] == 3


def test_browser_actions_are_not_executed_by_adapter():
    request = BrowserUseAdapter().action_request("open a page")
    assert request["requires_confirmation"] is True
    assert request["executed"] is False
    assert request["execution_owner"] == "Gungv-Workers"
