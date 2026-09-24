from integrations.runtime import inspect_runtime


def test_runtime_inspection_is_non_destructive():
    result = inspect_runtime()
    assert result["installation_performed"] is False
    assert result["external_execution"] is False
    assert result["adapter_count"] == 8
    assert len(result["adapter_names"]) == 8
    assert isinstance(result["available_adapters"], list)
