from nexus.organism import build_organism_status


def test_organism_status_is_compact_and_read_only() -> None:
    snapshot = build_organism_status(
        repositories=6,
        workers=3,
        jobs=11,
        audit_events=19,
        federation={"cmra": {"status": "ok"}},
    ).to_dict()

    assert snapshot["service"] == "gungv-nexus"
    assert snapshot["status"] == "ok"
    assert snapshot["repositories"] == 6
    assert snapshot["workers"] == 3
    assert snapshot["jobs"] == 11
    assert snapshot["federation"]["cmra"]["status"] == "ok"
    assert "payload" not in snapshot
    assert "token" not in snapshot
    assert "secret" not in snapshot
