class RecoveryManager:
    STATES=("ERROR","IDENTIFY_STATE","LOCATE_CHANGE","RESTORE","VERIFY","RECORDED")
    def plan(self, error: str):
        return {"error":error,"steps":list(self.STATES)}
