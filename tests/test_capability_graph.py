from integrations.capability_graph import build_graph


REFERENCE_REPOS = {
    "EverMind-AI/Raven",
    "onepointconsulting/nanobot-2026-07-30",
    "Shijou87/Brow",
    "mantou132/browser4agent",
    "shaun0927/openchrome",
    "reg2005/agent-mem",
}


def test_capability_graph_has_providers():
    graph = build_graph()
    assert graph
    assert "agent-runtime" in graph


def test_graph_nodes_have_readiness():
    graph = build_graph()
    assert all(
        node["readiness"] in {"ready", "reference", "unavailable"}
        for nodes in graph.values()
        for node in nodes
    )


def test_external_reference_nodes_are_not_executable():
    graph = build_graph()
    nodes = [
        node
        for nodes in graph.values()
        for node in nodes
        if node["repository"] in REFERENCE_REPOS
    ]
    assert nodes
    assert all(node["readiness"] == "reference" for node in nodes)
