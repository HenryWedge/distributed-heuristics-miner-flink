import string
from typing import List

from pandas import Timestamp

from conformance.source.event_log.event_log_source import EventLogSource


class TestEventLogSource(EventLogSource):

    def get_event_log(self):
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
