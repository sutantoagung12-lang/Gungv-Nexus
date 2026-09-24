from integrations.capability_graph import build_graph


def test_instagram_connector_is_visible_but_not_claimed_ready_without_validation():
    graph = build_graph({
        "available": [],
        "summary": {"instagram_api": "missing"},
    })
    node = graph["social-publishing"][0]
    assert node["adapter"] == "instagram_api"
    assert node["readiness"] == "missing"


def test_instagram_connector_becomes_ready_only_after_validation():
    graph = build_graph({
        "available": ["instagram_api"],
        "summary": {"instagram_api": "validated"},
    })
    node = graph["social-publishing"][0]
    assert node["readiness"] == "ready"
