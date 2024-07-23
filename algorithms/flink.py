import os
import random
from typing import List

import pm4py
from pandas import DataFrame, Timestamp
from pm4py.objects.log.obj import EventLog
from pm4py.util import constants, xes_constants
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from datastructure import Event, LossyCountingDictionary, CaseIdDictionary, MiningResult
from monitoring.conformance import calculate_metrics


class HeuristicsDiscovery:

    def __init__(self, bucket_size):
        self.activities = LossyCountingDictionary()
        self.relations = LossyCountingDictionary()
        self.cases = CaseIdDictionary()
        self.processedEvents = 0
        self.current_bucket = 1

    def get_bucket_size(self):
        if 'BUCKET_SIZE' not in os.environ:
            return 25
        return os.environ['BUCKET_SIZE']

    def process(self, event):
        self.processedEvents += 1
        case_id = event.caseId
        activity = event.activity
        bucket_size = self.get_bucket_size()
        self.current_bucket = int(self.processedEvents / bucket_size)

        self.activities.insert(activity, self.current_bucket)
        relation = self.cases.insert(case_id, activity)

        if relation is not None:
            self.relations.insert(relation, self.current_bucket)

        if self.processedEvents % bucket_size == 0:
            print(f"-------Bucket: {self.current_bucket}-------------")
            self.activities.clean_up(self.current_bucket)
            self.relations.clean_up(self.current_bucket)

        return MiningResult(self.relations.get_items_with_count())


def get_event_collection_of_size(size):
    events = []
    activities = ["A", "B", "C", "D", "E"]
    i = 0
    for i in range(size):
        events.append(Event(i, activities[int(random.uniform(0, len(activities)))]))
        events.append(Event(i, activities[int(random.uniform(0, len(activities)))]))
        events.append(Event(i, activities[int(random.uniform(0, len(activities)))]))
        events.append(Event(i, activities[int(random.uniform(0, len(activities)))]))
        events.append(Event(i, activities[int(random.uniform(0, len(activities)))]))
    return events



def mine_model():
    print("start")
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
    # TODO adjust parallelism
    env.set_parallelism(1)

    data_stream = env.from_collection(
        collection=get_event_collection_of_size(100)
    )

    heuristics_discovery = HeuristicsDiscovery(5)
    data_stream = data_stream.map(lambda event: heuristics_discovery.process(event))



    data_stream = data_stream.map(lambda mining_result: calculate_metrics(mining_result, ))

    data_stream.print()

    env.execute()

mine_model()