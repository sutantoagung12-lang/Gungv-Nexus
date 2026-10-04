"""Minimal persistence contract for CMRA service adapters."""
from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any

class StateStore(ABC):
    @abstractmethod
    def read(self, key: str) -> Any: raise NotImplementedError
    @abstractmethod
    def write(self, key: str, value: Any) -> None: raise NotImplementedError
    @abstractmethod
    def delete(self, key: str) -> None: raise NotImplementedError

class MemoryStateStore(StateStore):
    def __init__(self) -> None: self._data: dict[str, Any] = {}
    def read(self, key: str) -> Any: return deepcopy(self._data.get(key))
    def write(self, key: str, value: Any) -> None: self._data[key] = deepcopy(value)
    def delete(self, key: str) -> None: self._data.pop(key, None)
