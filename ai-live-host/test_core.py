import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core import Event, HostController  # noqa: E402


def test_demo_response():
    c = HostController()
    e = Event(kind="chat", text="Apa kabar?", user="A")
    c.ingest(e)
    assert "Apa kabar?" in c.respond(e)
    assert len(c.memory.messages) == 2


def test_support_memory():
    c = HostController()
    e = Event(kind="support", user="B", amount=10000, currency="IDR")
    c.ingest(e)
    response = c.respond(e)
    assert "10000" in response
    assert c.memory.supporters["B"] == 10000


def test_dry_run_default():
    old = os.environ.pop("LIVE_DRY_RUN", None)
    try:
        c = HostController()
        assert c.dry_run is True
    finally:
        if old is not None:
            os.environ["LIVE_DRY_RUN"] = old
