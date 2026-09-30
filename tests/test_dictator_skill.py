from skills.dictator import DictatorSkill


def test_dictator_allows_safe_steps():
    d = DictatorSkill().enforce(["inspect", "plan", "code", "test", "validate"])
    assert d.mode == "strict-execution-discipline"
    assert len(d.approved_steps) == 5
    assert not d.rejected_steps
    assert d.fail_closed


def test_dictator_blocks_restricted_steps_without_authority():
    d = DictatorSkill().enforce(["delete", "spend", "deploy_production"])
    assert not d.approved_steps
    assert set(d.rejected_steps) == {"delete", "spend", "deploy_production"}


def test_dictator_requires_validation_for_restricted_steps():
    d = DictatorSkill().enforce(
        ["deploy_production"],
        human_approved=True,
        environment_validated=True,
    )
    assert d.approved_steps == ("deploy_production",)
    assert d.checkpoint_required
    assert d.verification_required
