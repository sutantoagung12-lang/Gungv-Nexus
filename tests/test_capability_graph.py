from integrations.capability_graph import build_graph


def test_capability_graph_has_providers():
    graph = build_graph()
    assert graph
    assert "agent-runtime" in graph


def test_graph_nodes_have_readiness():
    graph = build_graph()
    node = graph["agent-runtime"][0]
    assert node["readiness"] in {"ready", "unavailable"}
