from typing import List

from pandas import Timestamp

from mining.heuristics.datastructure.event import Event


def build_event_log_from_datastream():
    event_log = dict()
    events: List[Event] = [
        Event("1", 'register request'),
        Event("1", 'examine thoroughly'),
        Event("1", 'check ticket'),
        Event("1", 'decide')
    ]

    event_log["concept:name"] = {}
    event_log["time:timestamp"] = {}
    event_log["case:concept:name"] = {}

    for i, event in enumerate(events):
        event_log["concept:name"][i] = event.activity
        event_log["time:timestamp"][i] = Timestamp.now()
        event_log["case:concept:name"][i] = event.caseId

    return event_log
