import json
from typing import Iterable

from pyflink.datastream import WindowFunction, CountWindow, ReduceFunction

from flink.wrapper.petri_net_serializer import PetriNetSerDes
from heuristics.algorithms.petrinet_merger import PetriNetMerger


class PetriNetsMergerFlink(ReduceFunction):

    def reduce(self, value1, value2):
        merger = PetriNetMerger()
        petri_net1 = PetriNetSerDes().deserialize(value1)
        petri_net2 = PetriNetSerDes().deserialize(value2)
        merged_petri_net = merger.merge_petri_nets(petri_net1, petri_net2)
        return PetriNetSerDes().serialize(merged_petri_net)
