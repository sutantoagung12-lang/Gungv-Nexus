DESTRUCTIVE_WORDS={"delete","destroy","remove","reset","force","drop"}

class SecurityPolicy:
    def inspect(self, operation: str, source: str="internal"):
        low=operation.lower()
        destructive=any(w in low for w in DESTRUCTIVE_WORDS)
        return {
            "allowed": not destructive,
            "confirmation_required": destructive,
            "source_trust": "untrusted" if source!="internal" else "internal",
            "secret_scan_required": True,
        }
