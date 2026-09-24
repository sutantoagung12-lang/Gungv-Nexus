"""Change gate for controlled evolution."""
DESTRUCTIVE={"delete","destroy","drop","reset","force_push","publish_private_repo"}

class ChangeGate:
    def assess(self, action):
        a=str(action).lower()
        destructive=any(x in a for x in DESTRUCTIVE)
        return {
            "action":action,
            "risk":"HIGH" if destructive else "NORMAL",
            "confirmation_required":destructive,
            "approved":not destructive
        }
