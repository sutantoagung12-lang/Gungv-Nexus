from integrations.capability_resolver import resolve


REFERENCE_REPOS = {
    "EverMind-AI/Raven",
    "onepointconsulting/nanobot-2026-07-30",
    "Shijou87/Brow",
    "mantou132/browser4agent",
    "shaun0927/openchrome",
    "reg2005/agent-mem",
}


def test_resolver_returns_runtime_ready_providers():
    result = resolve("build an agent runtime", limit=2)
    assert result
    assert all(len(item["providers"]) <= 2 for item in result)
    assert all("health_score" in provider for item in result for provider in item["providers"])


def test_resolver_does_not_select_reference_only_sources():
    result = resolve("build an agent runtime", limit=10)
    repositories = {
        provider["repository"]
        for item in result
        for provider in item["providers"]
    }
    assert repositories.isdisjoint(REFERENCE_REPOS)
