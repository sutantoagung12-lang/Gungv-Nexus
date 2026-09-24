"""Checkpoint state for recoverable long-running work."""
from datetime import datetime, timezone

class CheckpointManager:
    def __init__(self, runtime):
        self.runtime=runtime
        self.state={}

    def save(self, task_id, state):
        self.state[task_id]={
            "state":state,
            "saved_at":datetime.now(timezone.utc).isoformat()
        }
        return self.state[task_id]

    def load(self, task_id):
        return self.state.get(task_id)
