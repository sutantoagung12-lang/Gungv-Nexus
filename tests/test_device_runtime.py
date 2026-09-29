from integrations.device_runtime import DeviceIdentity, DeviceRuntime, RuntimeStrategy


def test_probe_failure_is_isolated():
    runtime = DeviceRuntime(DeviceIdentity(manufacturer="test", model="phone"))
    runtime.register_probe("virtual_display", lambda: True)

    def broken():
        raise RuntimeError("unsupported")

    runtime.register_probe("window_control", broken)
    results = {item["name"]: item for item in runtime.probe_all()}

    assert results["virtual_display"]["available"] is True
    assert results["window_control"]["available"] is False


def test_strategy_falls_back_to_first_supported():
    runtime = DeviceRuntime()
    runtime.register_probe("virtual_display", lambda: True)
    runtime.register_strategy(RuntimeStrategy("native-windowing", ("virtual_display",), 10))
    runtime.register_strategy(RuntimeStrategy("safe-observation", (), 20))

    assert runtime.select_strategy()["strategy"] == "native-windowing"


def test_session_journal_restores_original_state():
    runtime = DeviceRuntime()
    journal = runtime.start_session("s1")
    journal.record("orientation", "portrait")
    journal.record("density", 420)
    journal.record("orientation", "landscape")

    assert runtime.restore_session("s1") == {
        "orientation": "portrait",
        "density": 420,
    }
    assert runtime.restore_session("s1") == {}
