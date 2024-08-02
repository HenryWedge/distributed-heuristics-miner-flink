import json

from flink.wrapper.directly_follows_graph_serializer import DirectlyFollowsGraphSerDes
from heuristics.algorithms.directly_follows_graph_creator import DirectlyFollowsGraphCreator
from heuristics.datastructure.event import Event

class DirectlyFollowsGraphCreatorFlink:

    def __init__(self, bucket_size):
        self.directly_follows_graph_creator = DirectlyFollowsGraphCreator(bucket_size)

    def process(self, event_string: str) -> str:
        event_as_dict = json.loads(event_string)
        event = Event(
            timestamp=event_as_dict["timestamp"],
            sensor_value=event_as_dict["sensor_value"],
            case_id=event_as_dict["case_id"],
            sensor_name=event_as_dict["sensor_name"],
        )
        directly_follows_graph = self.directly_follows_graph_creator.process(event)
        directly_follows_graph_as_string = DirectlyFollowsGraphSerDes().serialize(directly_follows_graph)
        return directly_follows_graph_as_string
