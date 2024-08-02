import string
from typing import List, Dict
from pm4py import PetriNet

from heuristics.results.heuristics_net import HeuristicsResult
from heuristics.results.petri_net import SerializablePetriNet, create_empty_petri_net


class PetriNetWrapper:

    def __init__(self, name):
        self.net: SerializablePetriNet = create_empty_petri_net()
        self.place_before_activity: Dict[string, string] = dict()
        self.place_after_activity: Dict[string, string] = dict()
        self.concurrent_place_before_activity: Dict[string, string] = dict()
        self.concurrent_place_after_activity: Dict[string, string] = dict()
        self.concurrent_transition_before_activity: Dict[string, string] = dict()
        self.concurrent_transition_after_activity: Dict[string, string] = dict()

        self.activities: Dict[string, tuple[PetriNet.Place, PetriNet.Transition]] = dict()
        self.activities_concurrent: Dict[string, PetriNet.Transition] = dict()

    def add_start_activity(self, start_activity):
        self.net.add_start_activity(start_activity)

    def add_end_activity(self, end_activity):
        self.net.add_end_activity(end_activity)

    def add_transition_for_activity(self, activity):
        self.net.transitions.add(activity)

    def add_relation(self, predecessor, successor):
        if successor in self.place_before_activity:
            successor_place = self.place_before_activity[successor]
        else:
            successor_place = f"place_{successor}"
            self.net.add_place(successor_place)
            self.net.add_arc_place_transition(successor_place, successor)
            self.place_before_activity[successor] = successor_place

        self.net.add_arc_transition_place(predecessor, successor_place)
        self.place_after_activity[predecessor] = successor_place

    def add_concurrent_split(self, predecessor, successor):
        if predecessor in self.concurrent_place_after_activity:
            split_place = self.concurrent_place_after_activity[predecessor]
        else:
            split_place = f"place_split_{predecessor}"
            self.net.add_place(split_place)

        if predecessor in self.concurrent_transition_after_activity:
            split_transition = self.concurrent_transition_after_activity[predecessor]
        else:
            split_transition = f"split_{predecessor}"
            self.net.add_transition(split_transition)
            self.net.add_arc_place_transition(split_place, split_transition)

        self.net.add_arc_transition_place(predecessor, split_place)

        if successor in self.concurrent_place_before_activity:
            successor_place = self.concurrent_place_before_activity[successor]
        else:
            successor_place = f"place_concurrent_before_{successor}"
            self.net.add_place(successor_place)
            self.net.add_arc_place_transition(successor_place, successor)

        self.net.add_arc_transition_place(split_transition, successor_place)

    def add_concurrent_join(self, predecessor, successor):
        if successor in self.concurrent_place_before_activity:
            join_place = self.concurrent_place_before_activity[successor]
        else:
            join_place = f"place_join_{successor}"
            self.net.add_place(join_place)

        if successor in self.concurrent_transition_before_activity:
            join_transition = self.concurrent_transition_before_activity[predecessor]
        else:
            join_transition = f"join_{successor}"
            self.net.add_transition(join_transition)
            self.net.add_arc_transition_place(join_transition, join_place)

        self.net.add_arc_place_transition(join_place, successor)

        if predecessor in self.concurrent_place_after_activity:
            predecessor_place = self.concurrent_place_after_activity[successor]
        else:
            predecessor_place = f"place_concurrent_after_{predecessor}"
            self.net.add_place(predecessor_place)
            self.net.add_arc_transition_place(predecessor, predecessor_place)

        self.net.add_arc_place_transition(predecessor_place, join_transition)


class PetriNetCreator:

    def __init__(self):
        self.petri_net = PetriNetWrapper(name="my-petrinet")

    def _is_concurrent(self, activity, concurrent_activities: List[tuple[string, string]]):
        for concurrent_activity in concurrent_activities:
            if activity == concurrent_activity[0] or activity == concurrent_activity[1]:
                return True
        return False

    def create_petri_net(self, heuristics_result: HeuristicsResult) -> SerializablePetriNet:
        for activity in heuristics_result.all_activities:
            self.petri_net.add_transition_for_activity(activity)

        for start_activity in heuristics_result.start_activities:
            self.petri_net.add_start_activity(start_activity)

        for end_activity in heuristics_result.end_activities:
            self.petri_net.add_end_activity(end_activity)

        for relation in heuristics_result.relations:
            predecessor = relation[0]
            successor = relation[1]
            if self._is_concurrent(successor, heuristics_result.concurrent_activities):
                self.petri_net.add_concurrent_split(predecessor, successor)
            elif self._is_concurrent(predecessor, heuristics_result.concurrent_activities):
                self.petri_net.add_concurrent_join(predecessor, successor)
            else:
                self.petri_net.add_relation(predecessor, successor)

        return self.petri_net.net
