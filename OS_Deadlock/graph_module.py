import data

def add_process(process_id):
    data.processes.add(process_id)
    data.rag[process_id] = set()

def add_resource(resource_id):
    data.resources.add(resource_id)
    data.rag[resource_id] = set()

def allocate_resource(process_id, resource_id):
    if resource_id not in data.rag:
        raise KeyError(f"Resource {resource_id} does not exist. Please add it first.")
    if process_id not in data.rag:
        raise KeyError(f"Process {process_id} does not exist. Please add it first.")
    data.rag[resource_id].add(process_id)
    data.allocations[resource_id] = process_id


def request_resource(process_id, resource_id):
    data.rag[process_id].add(resource_id)
    if process_id not in data.requests:
        data.requests[process_id] = set()
    data.requests[process_id].add(resource_id)
