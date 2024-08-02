import string
from typing import List, Set

from pm4py import PetriNet, Marking
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to


def create_empty_petri_net():
    return SerializablePetriNet(set(), set(), set(), [], [])


class SerializablePetriNet:

    def __init__(
            self,
            places,
            transitions,
            arcs,
            start_activities,
            end_activities):
        self.places: Set[string] = places
        self.transitions: Set[string] = transitions
        self.arcs: Set[tuple[string, string]] = arcs
        self.start_activities = start_activities
        self.end_activities = end_activities

    def get_object(self, petri_net, name):
        for transition in petri_net.transitions:
            if transition.name == name:
                return transition
        for place in petri_net.places:
            if place.name == name:
                return place
        return None

    def to_pm4py_petri_net(self) -> (PetriNet, Marking, Marking):
        petri_net = PetriNet()
        initial_marking = Marking()
        final_marking = Marking()

        for place in self.places:
            petri_net.places.add(PetriNet.Place(place))

        for transition in self.transitions:
            petri_net.transitions.add(PetriNet.Transition(transition, label=transition))

        for arc in self.arcs:
            arc_start = self.get_object(petri_net, name=arc[0])
            arc_end = self.get_object(petri_net, name=arc[1])
            add_arc_from_to(arc_start, arc_end, petri_net)

        for start_activity in self.start_activities:
            place = self.get_object(petri_net, start_activity)
            initial_marking[place] = 1

        for end_activity in self.end_activities:
            place = self.get_object(petri_net, end_activity)
            final_marking[place] = 1

        return petri_net, initial_marking, final_marking
