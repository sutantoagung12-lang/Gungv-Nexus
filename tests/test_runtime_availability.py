from integrations.runtime_availability import detect


def test_runtime_availability_has_adaptive_mode():
    report = detect()
    assert report["mode"] == "adaptive"
    assert "github_api" in report["available"]
    assert set(report["available"]).isdisjoint(set(report["unavailable"]))
