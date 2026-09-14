from nexus.cognition import AdaptiveRouter, ModelProfile, TaskProfile, plan_parallelism


def test_router_prefers_capable_model():
    router = AdaptiveRouter([
        ModelProfile("cheap", {"coding": 0.55}, latency=0.2, cost=0.1),
        ModelProfile("coder", {"coding": 0.98, "reasoning": 0.9}, latency=0.7, cost=0.6),
    ])
    task = TaskProfile("coding", complexity=0.8, coding=1.0, reasoning=0.8)
    assert router.choose(task).name == "coder"


def test_experience_updates_reliability():
    router = AdaptiveRouter([ModelProfile("m", {"research": 0.9})])
    model = router.models["m"]
    router.learn("m", True)
    router.learn("m", True)
    assert model.successes == 2
    assert model.observed_reliability > model.reliability


def test_parallelism_is_bounded_and_adaptive():
    assert plan_parallelism(TaskProfile("simple", complexity=0.2)) == 1
    assert plan_parallelism(TaskProfile("research", complexity=0.7, research=0.9)) == 6
    assert plan_parallelism(TaskProfile("high", complexity=0.95, risk=0.2)) == 10
    assert plan_parallelism(TaskProfile("critical", complexity=0.95, risk=0.95)) == 4
