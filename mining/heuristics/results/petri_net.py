import string
from typing import List

from pm4py import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to


class SerializablePetriNet:

    def __init__(self):
        self.places: List[string] = []
        self.transitions: List[string] = []
        self.arcs: List[tuple[string, string]] = []

    def get_object(self, petri_net, name):
        for transition in petri_net.transitions:
            if transition.name == name:
                return transition
        for place in petri_net.places:
            if place.name == name:
                return place
        return None

    def to_pm4py_petri_net(self) -> PetriNet:
        petri_net = PetriNet()

        for place in self.places:
            petri_net.places.add(PetriNet.Place(place))

        for transition in self.transitions:
            petri_net.transitions.add(PetriNet.Transition(transition, label=transition))

        for arc in self.arcs:
            arc_start = self.get_object(petri_net, name=arc[0])
            arc_end = self.get_object(petri_net, name=arc[1])
            add_arc_from_to(arc_start, arc_end, petri_net)

        return petri_net
