"""Open-ended capability expansion under evidence-gated evolution."""
class CapabilityEvolution:
    def __init__(self): self.proposals=[]
    def propose(self,capability,reason):
        p={'capability':capability,'reason':reason,'status':'PROPOSED'}; self.proposals.append(p); return p
    def validate(self,proposal,evidence):
        if not evidence: proposal['status']='REJECTED'; return proposal
        proposal['status']='VALIDATED'; proposal['evidence']=evidence; return proposal
    def promote(self,proposal):
        if proposal.get('status')!='VALIDATED': raise ValueError('capability must be validated before promotion')
        proposal['status']='ACTIVE'; return proposal
