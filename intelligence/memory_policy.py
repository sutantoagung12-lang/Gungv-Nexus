"""Governed memory policy: store, reflect, abstract, and promote."""
from __future__ import annotations


def should_store(*, reward: float, quality: float, confidence: float,
                 destructive: bool = False) -> bool:
    if destructive:
        return False
    return min(reward, quality, confidence) >= 0.55


def should_promote(*, reward: float, quality: float, confidence: float,
                   evidence_count: int = 1) -> bool:
    return (
        reward >= 0.7 and quality >= 0.7 and confidence >= 0.65
        and evidence_count >= 1
    )
