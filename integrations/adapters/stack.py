"""Unified discovery surface for external AI capabilities."""

from .adk import GoogleADKAdapter
from .agno import AgnoAdapter
from .browser_use import BrowserUseAdapter
from .cognee import CogneeAdapter
from .dspy import DSPyAdapter
from .hindsight import HindsightAdapter
from .khoj import KhojAdapter
from .langgraph import LangGraphAdapter
from .observability import OpenTelemetryAdapter
from .pydantic_ai import PydanticAIAdapter
from .r2r import R2RAdapter


ADAPTERS = [
    LangGraphAdapter,
    R2RAdapter,
    KhojAdapter,
    BrowserUseAdapter,
    GoogleADKAdapter,
    AgnoAdapter,
    DSPyAdapter,
    PydanticAIAdapter,
    CogneeAdapter,
    HindsightAdapter,
    OpenTelemetryAdapter,
]


def status() -> list[dict]:
    return [adapter().status() for adapter in ADAPTERS]
