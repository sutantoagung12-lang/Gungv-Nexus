from skills.immortality import ImmortalitySkill

def test_checkpoint_and_recovery_preserve_state():
    skill=ImmortalitySkill()
    state={"knowledge":["a"],"cycle":7}
    cp=skill.checkpoint(state)
    recovered=skill.recover(cp)
    assert recovered["verified"] is True
    assert skill.continuity_check(state,recovered["state"])["continuous"] is True

def test_evolution_cannot_drop_baseline_state():
    skill=ImmortalitySkill()
    assert skill.evolve_without_loss({"a":1,"b":2},{"a":1})["status"]=="BLOCKED"
    assert skill.evolve_without_loss({"a":1},{"a":1,"b":2})["status"]=="SAFE_TO_PROMOTE"
