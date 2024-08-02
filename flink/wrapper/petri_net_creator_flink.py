import json

from heuristics.algorithms.petri_net_creator import PetriNetCreator
from heuristics.results.heuristics_net import HeuristicsResult


class PetriNetCreatorFlink:

    def __init__(self):
        self.petri_net_creator = PetriNetCreator()

    def process(self, heuristics_result_str: str) -> str:
        heuristics_result_dict = json.loads(heuristics_result_str)
        heuristics_result = HeuristicsResult(
            all_activities=heuristics_result_dict["all_activities"],
            start_activities=[],#heuristics_result_dict["start_activities"],
            end_activities=[],#heuristics_result_dict["end_activities"],
            relations=heuristics_result_dict["relations"],
            concurrent_activities=heuristics_result_dict["concurrent_activities"],
        )
        petri_net = self.petri_net_creator.create_petri_net(heuristics_result)

        petri_net_dict = dict()
        petri_net_dict["places"] = list(petri_net.places)
        petri_net_dict["transitions"] = list(petri_net.transitions)
        petri_net_dict["arcs"] = list(petri_net.arcs)
        petri_net_dict["start_activities"] = petri_net.start_activities
        petri_net_dict["end_activities"] = petri_net.end_activities

        petri_net_str = json.dumps(petri_net_dict)
        return petri_net_str
