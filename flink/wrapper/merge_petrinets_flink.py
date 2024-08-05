import json
from typing import Iterable

from pyflink.datastream import WindowFunction, CountWindow, ReduceFunction

from flink.wrapper.petri_net_serializer import PetriNetSerializer
from heuristics.algorithms.petrinet_merger import PetriNetMerger
from heuristics.results.petri_net import SerializablePetriNet


class PetriNetsMergerFlink(ReduceFunction):

    def list_to_tuple(self, transitions):
        transitions_as_tuple = []
        for transition in transitions:
            transitions_as_tuple.append((transition[0], transition[1]))
        return transitions_as_tuple

    def transform_to_net(self, net_dict):
        return SerializablePetriNet(
            places=net_dict["places"],
            transitions=net_dict["transitions"],
            arc_place_transition=self.list_to_tuple(net_dict["arc_place_transition"]),
            arc_transition_place=self.list_to_tuple(net_dict["arc_transition_place"]),
            start_activities=net_dict["start_activities"],
            end_activities=net_dict["end_activities"]
        )

    def reduce(self, value1, value2):
        merger = PetriNetMerger()
        petri_net1 = self.transform_to_net(json.loads(value1))
        petri_net2 = self.transform_to_net(json.loads(value2))
        merged_petri_net = merger.merge_petri_nets(petri_net1, petri_net2)
        return PetriNetSerializer().serialize(merged_petri_net)
