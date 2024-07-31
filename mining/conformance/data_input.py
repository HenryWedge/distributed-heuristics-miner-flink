import string
from typing import List

from kafka import KafkaConsumer
from pandas import DataFrame, Timestamp
from abc import abstractmethod

from mining.heuristics.algorithms.petri_net_creator import PetriNetCreator, HeuristicsResult


class AbstractDataInput:
    @abstractmethod
    def get_petri_net(self):
        pass

    @abstractmethod
    def get_event_log(self):
        pass


class DataInput(AbstractDataInput):

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

    def build_event_log_from_datastream(self):
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

    def get_event_log(self):
        return DataFrame.from_dict(self.build_event_log_from_datastream())


class KafkaDataInput(AbstractDataInput):

    def __init__(self):
        self.petri_net = None
        self.event_log = dict()
        self.results_kafka_consumer = KafkaConsumer(
            topics="results",
            bootstrap_servers="kube1-1:30376",
            group_id="my-group",
        )

        self.log_kafka_consumer = KafkaConsumer(
            topics="input",
            bootstrap_servers="kube1-1:30376",
            group_id="my-group2",
        )

    def run(self):
        for message in self.results_kafka_consumer:
            self.petri_net = message

        for event in self.log_kafka_consumer:
            case_id = event.case_id
            if case_id not in self.event_log:
                self.event_log[case_id] = []
            else:
                self.event_log[case_id].append(event)

    def get_petri_net(self):
        return self.petri_net

    def get_event_log(self):
        for case in self.event_log:
            return self.event_log[case]
        return dict()
