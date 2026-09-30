from skills.self_evolution import SelfEvolutionSkill


def test_self_evolution_builds_gated_plan():
    plan = SelfEvolutionSkill().plan(
        "expand research capability",
        ["source discovery", "evaluation"],
        baseline_metric=0.7,
    )
    assert plan.status == "CANDIDATE"
    assert len(plan.experiments) == 2
    assert "compare-against-baseline" in plan.acceptance_criteria
    assert "measure-improvement-over-baseline" in plan.acceptance_criteria
    assert "checkpoint" in plan.checkpoint


def test_self_evolution_detects_improvement():
    assert SelfEvolutionSkill.evaluate(0.7, 0.8) == "PROMOTION_CANDIDATE"


def test_self_evolution_detects_regression():
    assert SelfEvolutionSkill.evaluate(0.8, 0.6) == "ROLLBACK_REQUIRED"


def test_self_evolution_detects_no_improvement():
    assert SelfEvolutionSkill.evaluate(0.8, 0.8) == "NO_IMPROVEMENT"
