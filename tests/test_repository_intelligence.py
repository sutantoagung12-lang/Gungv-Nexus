from nexus.repository_intelligence import RepositoryProfile, evaluate, rank


def test_evaluate_prefers_capability_match_and_read_only_access():
    profile = RepositoryProfile(
        name="graphiti",
        full_name="Memory-Agents/graphiti",
        capabilities=frozenset({"temporal-knowledge-graph", "hybrid-retrieval"}),
        maintenance_score=0.9,
        security_score=0.9,
        integration_cost=0.2,
    )
    result = evaluate(profile, {"temporal-knowledge-graph", "hybrid-retrieval"})
    assert result.score >= 0.8
    assert result.recommendation == "adopt_candidate"
    assert result.missing_capabilities == ()


def test_rank_orders_best_candidate_first():
    profiles = [
        RepositoryProfile("weak", "x/weak", frozenset({"foo"})),
        RepositoryProfile("strong", "x/strong", frozenset({"foo", "bar"}), maintenance_score=0.9, security_score=0.9),
    ]
    results = rank(profiles, {"foo", "bar"})
    assert results[0].full_name == "x/strong"
