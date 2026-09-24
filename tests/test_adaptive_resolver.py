from integrations.capability_resolver import resolve


def test_resolver_returns_runtime_ready_providers():
    result = resolve("build an agent runtime", limit=2)
    assert result
    assert all(len(item["providers"]) <= 2 for item in result)
    assert all("health_score" in provider for item in result for provider in item["providers"])
