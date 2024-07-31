import string
from typing import List, Dict

import pm4py
from pandas import Timestamp, DataFrame
from pm4py import PetriNet, Marking
from pm4py.objects.petri_net.utils import reduction

from mining.heuristics.results.heuristics_net import HeuristicsResult
from mining.heuristics.results.petri_net import SerializablePetriNet


class PetriNetWrapper:

    def __init__(self, name):
        self.net = SerializablePetriNet() #PetriNet(name)
        self.initial_marking = Marking()
        self.final_marking = Marking()

    def add_place_with_name(self, name):
        #place = PetriNet.Place(name)
        #self.net.places.add(place)
        place_name = f"place_{name}"
        self.net.places.append(place_name)
        return place_name #place

    def mark_start_place(self, start_place):
        self.initial_marking[start_place] = 1

    def mark_end_place(self, end_place):
        self.final_marking[end_place] = 1

    def add_silent_transition(self, name):
        #transition=PetriNet.Transition(name=name, label=None)
        #self.net.transitions.append(transition)
        self.net.transitions.append(name)
        return name

    def add_transition_for_activity(self, activity) -> tuple[string, string]:
        #place = PetriNet.Place(f"pre_{activity}")
        place_name = f"pre_{activity}"
        self.net.places.append(place_name)
        #transition = PetriNet.Transition(name=f"Entering {activity}", label=activity)
        self.net.transitions.append(activity)
        self.net.arcs.append((place_name, activity))
        #add_arc_from_to(place, transition, self.net)
        return place_name, activity

    def add_split_place(self, label):
        split_place = self.add_place_with_name(f"split_{label}")
        return split_place
    def add_new_relation(self, transition, place):
        split_place = self.add_split_place(transition.label)
        self.net.arcs.append((transition, place))
        #add_arc_from_to(transition, split_place, self.net)
        silent_transition = self.add_silent_transition(f"silent{transition.label}")
        #add_arc_from_to(split_place, silent_transition, self.net)
        #add_arc_from_to(silent_transition, place, self.net)
        self.net.arcs.append((split_place, silent_transition))
        self.net.arcs.append((silent_transition, place))
        return split_place

    def add_relation(self, transition, place):
        self.net.arcs.append((transition, place))
        #add_arc_from_to(transition, place, self.net)

    def remove_unused_places(self):
        places_to_remove = []
        for place in self.net.places:
            if place not in self.initial_marking and not place.in_arcs:
                places_to_remove.append(place)

        #for i in range(len(places_to_remove)):
        #    remove_place(self.net, places_to_remove[i])

    def connect_places_silent(self, place1: PetriNet.Place, place2: PetriNet.Place):
        #silent_transition = self.add_silent_transition(f"silent_{place1.name}_{place2.name}")
        #add_arc_from_to(place1, silent_transition, self.net)
        #add_arc_from_to(silent_transition, place2, self.net)
        self.net.arcs.append((place1, place2))
        #add_arc_from_to(place1, place2, self.net)

    def add_hidden_transition_and_connect_with_places(self, place1: PetriNet.Place, connect_places: List[PetriNet.Place]):
        hidden_transition = self.add_silent_transition(f"silent_split_{place1}")
        #add_arc_from_to(place1, hidden_transition, self.net)
        self.net.arcs.append((place1, hidden_transition))
        for connect_place in connect_places:
            self.net.arcs.append((hidden_transition, connect_place))
            #add_arc_from_to(hidden_transition, connect_place, self.net)

    def add_start_activity(self):
        pass

    def add_end_activity(self):
        pass


class ActivityConnector:

    def __init__(self):
        self.activities: Dict[string, tuple[PetriNet.Place, PetriNet.Transition]] = dict()
        self.activities_concurrent: Dict[string, PetriNet.Transition] = dict()

    def register_activity(self, activity, place_with_transition):
        self.activities[activity] = place_with_transition
    def insert_concurrent(self, activity: string, transition: PetriNet.Transition):
        self.activities_concurrent[activity] = transition

    def get_connection_for(self, activity1, activity2):
        _, transition = self.activities[activity1]
        place, _ = self.activities[activity2]
        return transition, place

    def get_place_for(self, activity):
        return self.activities[activity][0]

    def get_transition(self, activity):
        return self.activities[activity][1]

    def connect(self) -> PetriNet.Transition | PetriNet.Place:
        pass

    def connect_concurrent(self) -> PetriNet.Transition | PetriNet.Place:
        pass


class PetriNetCreator:

    def __init__(self):
        self.petri_net_connector = ActivityConnector()
        self.petri_net = PetriNetWrapper(name="my-petrinet")

    def create_petri_net(self, heuristics_result: HeuristicsResult) -> (PetriNet, Marking, Marking):
        for activity in heuristics_result.all_activities:
            self.petri_net_connector.register_activity(activity, self.petri_net.add_transition_for_activity(activity))

        for activity in heuristics_result.all_activities:
            successors = heuristics_result.get_successors_of(activity)
            concurrent_successors = heuristics_result.get_concurrent_successors_of(activity)
            successor_count = len(successors)

            if successor_count == 1:
                transition, place = self.petri_net_connector.get_connection_for(activity, successors[0])
                self.petri_net.add_relation(transition, place)
            if len(concurrent_successors) > 1:
                split_place = self.petri_net.add_split_place(activity)
                self.petri_net.add_relation(self.petri_net_connector.get_transition(activity), split_place)
                successor_places = []
                for successor in concurrent_successors:
                    successor_places.append(self.petri_net_connector.get_place_for(successor))
                self.petri_net.add_hidden_transition_and_connect_with_places(split_place, successor_places)
            if successor_count > 1:
                split_place = self.petri_net.add_split_place(activity)
                self.petri_net.add_relation(self.petri_net_connector.get_transition(activity), split_place)
                for successor in successors:
                    if successor not in concurrent_successors:
                        transition = self.petri_net_connector.get_transition(successor)
                        #successor_place = self.petri_net_connector.get_place_for(successor)
                        self.petri_net.add_relation(split_place, transition)
                        #self.petri_net.connect_places_silent(split_place, self.petri_net_connector.get_place_for(successor))

        for start_activity in heuristics_result.start_activities:
            start_place = self.petri_net_connector.get_place_for(start_activity)
            self.petri_net.mark_start_place(start_place)

        for end_activity in heuristics_result.end_activities:
            end_transition = self.petri_net_connector.get_transition(end_activity)
            end_place = self.petri_net.add_place_with_name(f"end_{end_transition}")
            self.petri_net.mark_end_place(end_place)
            self.petri_net.add_relation(end_transition, end_place)

        #self.petri_net.remove_unused_places()

        return self.petri_net.net, self.petri_net.initial_marking, self.petri_net.final_marking

def build_event_log_from_datastream():
    event_log = dict()
    events: List[string] = [
        "a", "b", "c"
    ]

    event_log["concept:name"] = {}
    event_log["time:timestamp"] = {}
    event_log["case:concept:name"] = {}

    for i, activity in enumerate(events):
        event_log["concept:name"][i] = activity
        event_log["time:timestamp"][i] = Timestamp.now()
        event_log["case:concept:name"][i] = "1"

    return event_log

def test():
    result = HeuristicsResult(
        all_activities=[
            #"a", "b", "c", "d", "e", "f"
            "a", "b", "c", "d", "e", "f"
        ],
        start_activities=[
            #"a", "f"
            "a"
        ],
        end_activities=[
            #"e", "d"
            #"b",
            #"c",
            #"d",
            #"e",
            "f"
        ],
        relations=[
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            #("c", "d"),
            #("b", "e"),
            ("c", "e"),
            ("d", "f"),
            ("e", "f"),
            ("a", "f")
            #("c", "d"),
            #("b", "d"),
            #("a", "c"),
            #("a", "d"),
            #("b", "e"),
            #("c", "e"),
            #("f", "b")
        ],
        concurrent_activities=[
            ("a", ("b", "c"))
        ]
    )
    creator = PetriNetCreator()
    petri_net, initial_marking, final_marking = creator.create_petri_net(result)
    event_log = DataFrame.from_dict(build_event_log_from_datastream())
    petri_net = petri_net.to_pm4py_petri_net()
    reduction.apply_simple_reduction(petri_net)

    pm4py.view_petri_net(petri_net, initial_marking, final_marking)
    print(pm4py.precision_token_based_replay(event_log, petri_net, Marking(), Marking()))
    print(pm4py.fitness_token_based_replay(event_log, petri_net, initial_marking, final_marking))
    print(pm4py.fitness_alignments(event_log, petri_net, initial_marking, final_marking))
    print(pm4py.precision_alignments(event_log, petri_net, initial_marking, final_marking))

if __name__ == '__main__':
    test()