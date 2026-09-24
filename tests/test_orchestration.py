import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kernel.runtime import NexusRuntime
from cognition.orchestration import OrchestrationCycle

def test_orchestration_cycle():
    with tempfile.TemporaryDirectory() as d:
        n=NexusRuntime(d)
        result=OrchestrationCycle(n).run("Build Nexus", "design memory workflow")
        assert result["status"] == "READY_FOR_EXECUTION"
        assert result["goal"] == "Build Nexus"
        assert result["task"] == "design memory workflow"
        assert result["cycle_id"]
        assert n.memory.all()
