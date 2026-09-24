"""High-signal retrieval for Nexus memory and knowledge."""
import re
from math import log1p

STOPWORDS={"the","and","atau","dan","yang","untuk","dengan","this","that","dari","pada","adalah"}

def terms(text):
    return {x for x in re.findall(r"[a-z0-9_\-]{2,}", text.lower()) if x not in STOPWORDS}

class RetrievalEngine:
    def rank(self, query, records, limit=8):
        q=terms(query)
        ranked=[]
        for row in records or []:
            content=str(row.get("content",""))
            r=terms(content)
            overlap=len(q & r)
            if not overlap: continue
            confidence=float(row.get("confidence",0.5) or 0.5)
            recency_bonus=0.1 if row.get("status") in ("ACTIVE","CONFIRMED") else 0.0
            score=(overlap/max(1,len(q))) + (0.2*confidence) + recency_bonus
            ranked.append((score,row))
        ranked.sort(key=lambda x:x[0], reverse=True)
        return [row for _,row in ranked[:limit]]
