"""Unified discovery surface for the optional public AI stack."""

from .browser_use import BrowserUseAdapter
from .khoj import KhojAdapter
from .langgraph import LangGraphAdapter
from .r2r import R2RAdapter


def status() -> list[dict]:
    return [
        LangGraphAdapter().status(),
        R2RAdapter().status(),
        KhojAdapter().status(),
        BrowserUseAdapter().status(),
    ]
