from integrations.capability_index import build_index, resolve


def test_capability_index_is_nonempty():
    index = build_index()
    assert index
    assert "agent-runtime" in index


def test_capability_index_contains_multiple_sources():
    index = build_index()
    assert len(index["agent-runtime"]) >= 2


def test_resolve_is_bounded():
    results = resolve("build an agent runtime", limit=3)
    assert results
    assert all(len(item["repositories"]) <= 3 for item in results)
