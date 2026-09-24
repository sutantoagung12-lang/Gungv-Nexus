from work.queue import WorkQueue
from experiments.lab import ExperimentLab
from governance.gate import ChangeGate

def test_work_queue():
    q=WorkQueue(); x=q.enqueue('o','t'); assert q.next()['id']==x['id']

def test_experiment():
    x=ExperimentLab().create('q','h'); assert x['status']=='DESIGN'

def test_gate():
    assert ChangeGate().assess('delete data')['confirmation_required']
