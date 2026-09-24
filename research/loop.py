"""Bounded research loop with explicit evidence and experiment stages."""
from datetime import datetime, timezone

class ResearchLoop:
    def __init__(self, runtime):
        self.runtime=runtime

    def prepare(self, question, sources=None):
        return {
            "question":question,
            "sources":sources or [],
            "source_policy":"untrusted_until_validated",
            "stages":["discover","cross_check","experiment","evaluate","record"],
            "created_at":datetime.now(timezone.utc).isoformat()
        }
