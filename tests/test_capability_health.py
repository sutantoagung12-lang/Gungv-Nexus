from integrations.capability_health import rank


def test_health_ranking_is_bounded():
    providers = [{"repository": "a/x", "readiness": "ready", "trust": "external-public"}]
    result = rank(providers, {"a/x": {"success_rate": 1.0, "quality": 1.0}})
    assert result[0]["health_score"] == 1.0
