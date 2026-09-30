"""Dynamic organ registry: Nexus can add validated organs without changing its single-agent surface."""
from dataclasses import dataclass, asdict
from typing import Any
@dataclass
class Organ:
    organ_id:str; name:str; function:str; status:str='CANDIDATE'; version:int=1; evidence:int=0
class OrganRegistry:
    def __init__(self): self.organs:dict[str,Organ]={}
    def propose(self,organ_id,name,function):
        o=Organ(organ_id,name,function); self.organs[organ_id]=o; return o
    def validate(self,organ_id,evidence=1):
        o=self.organs[organ_id]; o.evidence+=evidence; o.status='VALIDATED' if o.evidence>0 else 'CANDIDATE'; return o
    def activate(self,organ_id):
        o=self.organs[organ_id]
        if o.status!='VALIDATED': raise ValueError('organ must be validated before activation')
        o.status='ACTIVE'; return o
    def snapshot(self): return [asdict(o) for o in self.organs.values()]
