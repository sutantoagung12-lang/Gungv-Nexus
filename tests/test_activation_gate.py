from integrations.activation_gate import evaluate_activation, activation_report


def test_activation_defaults_to_blocked():
    decision = evaluate_activation("LangGraph")
    assert decision.allowed is False
    assert decision.reason == "environment_not_validated"


def test_browser_requires_human_approval():
    decision = evaluate_activation(
        "browser-use",
        environment_validated=True,
        tests_passed=True,
        human_approved=False,
    )
    assert decision.allowed is False
    assert decision.reason == "human_approval_required_for_browser_actions"


def test_android_chrome_requires_human_approval():
    decision = evaluate_activation(
        "android-chrome-cdp",
        environment_validated=True,
        tests_passed=True,
        human_approved=False,
    )
    assert decision.allowed is False
    assert decision.reason == "human_approval_required_for_android_chrome_actions"


def test_activation_can_be_allowed_after_all_gates():
    decision = evaluate_activation(
        "LangGraph",
        environment_validated=True,
        tests_passed=True,
    )
    assert decision.allowed is True


def test_report_is_non_executing():
    report = activation_report()
    assert report["external_execution"] is False
    assert all(item["allowed"] is False for item in report["decisions"])
