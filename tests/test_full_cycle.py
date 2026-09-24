import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kernel.runtime import NexusRuntime

def test_full_cycle():
    with tempfile.TemporaryDirectory() as d:
        n=NexusRuntime(d)
        result=n.run_cycle("Build Nexus", "test memory workflow")
        assert result["evaluation"]["passed"] is True
        assert result["execution"]["status"] == "COMPLETED"
        assert result["learning"]["recorded"] is True
