from conformance.source.model.model_source import ModelSource
from heuristics.algorithms.petri_net_creator import PetriNetCreator
from heuristics.results.heuristics_net import HeuristicsResult
from heuristics.results.petri_net import create_empty_petri_net


class TestModelSource(ModelSource):
    def get_petri_net(self):
        return create_empty_petri_net()
