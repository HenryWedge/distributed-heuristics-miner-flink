import datetime
import unittest

import pm4py

from heuristics.algorithms.petri_net_creator import PetriNetCreator
from heuristics.datastructure.event import Event
from heuristics.results.event_log import SerializableEventLog
from heuristics.results.heuristics_net import HeuristicsResult
from heuristics.results.petri_net import SerializablePetriNet

petriNetCreator: PetriNetCreator = PetriNetCreator()


class PetriNetCreatorTest(unittest.TestCase):

    def test_create_petri_net(self):
        heuristics_result: HeuristicsResult = HeuristicsResult(
            all_activities=["a", "b", "c", "d"],
            start_activities=["a"],
            end_activities=["d"],
            relations=[("a", "b"), ("a", "c"), ("c", "d"), ("b", "d")],
            concurrent_activities=["b", "c"]
        )

        petri_net: SerializablePetriNet = petriNetCreator.create_petri_net(heuristics_result)
        pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking = petri_net.to_pm4py_petri_net()

        pm4py.view_petri_net(pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking)
        event_log: SerializableEventLog = SerializableEventLog(
            [
                Event(datetime.datetime.now(), "a", "c1", "s1"),
                Event(datetime.datetime.now(), "b", "c1", "s1"),
                Event(datetime.datetime.now(), "d", "c1", "s1"),
                Event(datetime.datetime.now(), "a", "c2", "s1"),
                Event(datetime.datetime.now(), "b", "c2", "s1"),
                Event(datetime.datetime.now(), "c", "c2", "s1"),
                Event(datetime.datetime.now(), "d", "c2", "s1"),
            ]
        )

        pm4py_event_log = event_log.to_pm4py_event_log()

        pm4py.fitness_alignments(pm4py_event_log, pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking)
        pm4py.precision_alignments(pm4py_event_log, pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking)

    def test_relation(self):
        heuristics_result: HeuristicsResult = HeuristicsResult(
            all_activities=["a", "b", "c", "d", "e", "f", "g", "h"],
            start_activities=["a"],
            end_activities=["h"],
            relations=[("a", "b"), ("a", "c"), ("c", "d"), ("c", "e"), ("d", "f"), ("e", "f"), ("f", "h"), ("b", "g"), ("g", "h")],
            concurrent_activities=[("f", "g"), ("c", "b")]
        )

        petri_net: SerializablePetriNet = petriNetCreator.create_petri_net(heuristics_result)
        pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking = petri_net.to_pm4py_petri_net()

        pm4py.view_petri_net(pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking)
        event_log: SerializableEventLog = SerializableEventLog(
            [
                Event(datetime.datetime.now(), "a", "c1", "s1"),
                Event(datetime.datetime.now(), "b", "c1", "s1"),
                Event(datetime.datetime.now(), "d", "c1", "s1"),
                Event(datetime.datetime.now(), "a", "c2", "s1"),
                Event(datetime.datetime.now(), "b", "c2", "s1"),
                Event(datetime.datetime.now(), "c", "c2", "s1"),
                Event(datetime.datetime.now(), "d", "c2", "s1"),
            ]
        )

        pm4py_event_log = event_log.to_pm4py_event_log()

        print(pm4py.fitness_token_based_replay(pm4py_event_log, pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking))
        print(pm4py.precision_token_based_replay(pm4py_event_log, pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking))
        print(pm4py.fitness_alignments(pm4py_event_log, pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking))
        print(pm4py.precision_alignments(pm4py_event_log, pm4py_petrinet, pm4py_initial_marking, pmy4py_final_marking))
