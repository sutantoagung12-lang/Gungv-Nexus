from cmra.integration.cmra_bridge import (
    CMRA_RELEASE,
    CMRA_SCHEMA,
    build_handshake,
    prepare_state_operation,
    validate_handshake,
)

def test_handshake_contract():
    payload = build_handshake()
    ok, errors = validate_handshake(payload)
    assert ok, errors
    assert payload["cmra"]["release"] == CMRA_RELEASE
    assert payload["cmra"]["schema"] == CMRA_SCHEMA

def test_handshake_rejects_external_execution():
    payload = build_handshake()
    payload["execution"]["external"] = True
    ok, errors = validate_handshake(payload)
    assert not ok
    assert "external_execution_must_be_disabled" in errors

def test_operations_are_prepare_only():
    status = prepare_state_operation("status")
    rollback = prepare_state_operation("rollback", snapshot_id="snap-1")
    assert status["executed"] is False
    assert rollback["executed"] is False
    assert rollback["approval_required"] is True
