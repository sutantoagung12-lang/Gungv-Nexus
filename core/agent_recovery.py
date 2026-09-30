"""Failure diagnosis and bounded recovery planning."""
class RecoveryEngine:
    def diagnose(self,error,attempts=0):
        return {'error':str(error),'attempts':attempts,'recoverable':attempts<3,'action':'retry_with_alternative' if attempts<3 else 'rollback_and_stop'}
