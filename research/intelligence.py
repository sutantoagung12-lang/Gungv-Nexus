class ResearchIntelligence:
    def prepare(self,question,sources=None): return {'question':question,'sources':sources or [],'validated':False,'stages':['discover','cross_check','experiment','evaluate','record']}
