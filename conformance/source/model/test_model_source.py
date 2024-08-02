from conformance.source.model.model_source import ModelSource
from heuristics.algorithms.petri_net_creator import PetriNetCreator
from heuristics.results.heuristics_net import HeuristicsResult


class TestModelSource(ModelSource):
    def get_petri_net(self):
        result = HeuristicsResult(
            all_activities=[
                "a", "b"
            ],
            start_activities=[
                "a"
            ],
            end_activities=[
                "b"
            ],
            relations=[
                ("a", "b"),
            ],
            concurrent_activities=[
                #("a", ("b", "c"))
            ]
        )
        creator = PetriNetCreator()
        return creator.create_petri_net(result)
