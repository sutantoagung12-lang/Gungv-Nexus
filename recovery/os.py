"""Recovery OS boundary."""
class RecoveryOS:
    def recover(self,state,error): return {'previous_state':state,'error':error,'action':'ROLLBACK_OR_RESTORE','verification_required':True}
