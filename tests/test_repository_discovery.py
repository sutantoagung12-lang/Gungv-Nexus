from integrations.repository_discovery import _score, load_config


def test_discovery_config_is_enabled_and_bounded():
    config = load_config()
    assert config["enabled"] is True
    assert 1 <= config["results_per_query"] <= 100
    assert 1 <= config["max_candidates"] <= 100


def test_score_is_numeric_and_monotonic_for_stars():
    low = _score({"stargazers_count": 10, "forks_count": 0})
    high = _score({"stargazers_count": 1000, "forks_count": 0})
    assert high > low
