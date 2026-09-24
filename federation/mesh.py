class FederationMesh:
    def register(self,source,trust='UNTRUSTED'): return {'source':source,'trust':trust,'validation_required':trust!='TRUSTED'}
