"""Cross-check helper requiring independent source identifiers."""
def cross_check(claim, sources):
    unique=[]
    for source in sources:
        if source not in unique: unique.append(source)
    return {"claim":claim,"independent_sources":unique,"status":"validated-candidate" if len(unique)>=2 else "insufficient"}
