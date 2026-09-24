"""Evidence-aware research preparation."""
class ResearchIntelligence:
    def prepare(self,question,sources=None):
        sources=sources or []
        return {"question":question,"sources":sources,"validated":False,"next":["cross_check","assess_provenance","experiment","evaluate"]}
