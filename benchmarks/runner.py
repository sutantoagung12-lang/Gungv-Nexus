"""Benchmark abstraction."""
class BenchmarkRunner:
    def run(self,name,cases,fn):
        results=[]
        for case in cases:
            try: results.append({"case":case,"ok":bool(fn(case))})
            except Exception as exc: results.append({"case":case,"ok":False,"error":type(exc).__name__})
        return {"name":name,"passed":sum(r["ok"] for r in results),"total":len(results),"results":results}
