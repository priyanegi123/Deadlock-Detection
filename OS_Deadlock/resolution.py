import data

def score(process_id):
    held_resources = sum([1 for r, p in data.allocations.items() if p == process_id])
    priority = data.process_metadata.get(process_id, {}).get("priority", 5)
    runtime = data.process_metadata.get(process_id, {}).get("runtime", 5)
    return held_resources * 2 + runtime + (10 - priority)

def resolve_deadlock():
    candidates = list(data.processes)
    candidates.sort(key=score)
    victim = candidates[0]
    print(f"[Resolution] Terminating process: {victim}")
    
    to_remove = []
    for resource, holder in data.allocations.items():
        if holder == victim:
            to_remove.append(resource)
    for r in to_remove:
        data.rag[r].discard(victim)
        del data.allocations[r]

    if victim in data.rag:
        del data.rag[victim]
    data.processes.remove(victim)
