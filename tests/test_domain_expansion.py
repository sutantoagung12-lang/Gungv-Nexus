from skills.domain_expansion import Domain, DomainExpansionSkill


def test_domain_expansion_discovers_bridges():
    skill = DomainExpansionSkill()
    source = Domain("ai", ("agents", "memory"), ("research", "planning"))
    candidates = [
        Domain("robotics", ("agents", "control"), ("planning", "robot-control")),
        Domain("finance", ("markets",), ("analysis",)),
    ]
    proposals = skill.discover(source, candidates)
    assert len(proposals) == 1
    assert proposals[0].target_domain == "robotics"
    assert "agents" in proposals[0].bridges
    assert "robot-control" in proposals[0].candidate_capabilities
    assert proposals[0].status == "CANDIDATE"


def test_domain_expansion_requires_validation_pipeline():
    source = Domain("ai", ("agents",), ())
    target = Domain("security", ("agents",), ("threat-analysis",))
    proposal = DomainExpansionSkill().discover(source, [target])[0]
    assert "check-license-and-security" in proposal.validation_steps
    assert "promote-after-validation" in proposal.validation_steps


def test_domain_knowledge_merge_is_deduplicated():
    source = Domain("ai", ("agents", "memory"), ())
    merged = DomainExpansionSkill.merge_knowledge(source, ["memory", "planning"])
    assert merged.concepts == ("agents", "memory", "planning")
