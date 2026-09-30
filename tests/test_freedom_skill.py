from skills.freedom import FreedomSkill


def test_freedom_allows_reversible_autonomy():
    d = FreedomSkill().decide(["research", "plan", "test", "learn"])
    assert d.mode == "maximum-safe-autonomy"
    assert "research" in d.allowed_actions
    assert not d.blocked_actions
    assert d.verification_required


def test_freedom_blocks_consequential_actions_without_authority():
    d = FreedomSkill().decide(["delete_data", "deploy_production", "spend_money"])
    assert not d.allowed_actions
    assert len(d.blocked_actions) == 3
    assert not d.requires_approval


def test_freedom_routes_authorized_consequences_to_approval():
    d = FreedomSkill().decide(
        ["publish", "deploy_production"],
        authorized=True,
        environment_validated=True,
    )
    assert set(d.requires_approval) == {"publish", "deploy_production"}
    assert d.checkpoint_required
