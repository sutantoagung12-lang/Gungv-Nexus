from dataclasses import dataclass, field

@dataclass
class Experiment:
    id: str
    question: str
    hypothesis: str
    status: str = "DESIGNED"
    results: dict = field(default_factory=dict)

class ExperimentEngine:
    def design(self, id, question, hypothesis):
        return Experiment(id, question, hypothesis)
    def conclude(self, experiment, results, conclusion):
        experiment.results=results; experiment.status="CONCLUDED"; experiment.conclusion=conclusion; return experiment
