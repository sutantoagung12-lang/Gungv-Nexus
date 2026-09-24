"""Transparent confidence metadata; never substitutes for validation."""
class ConfidenceEngine:
    def assess(self,evidence_count,independent_sources=0,validated=False):
        if validated: level="validated"
        elif evidence_count and independent_sources: level="supported"
        elif evidence_count: level="tentative"
        else: level="unknown"
        return {"level":level,"evidence_count":evidence_count,"independent_sources":independent_sources}
