import json
import string
from typing import Dict

from mining.heuristics.results.directly_follows_graph import DirectlyFollowsGraph


class DirectlyFollowsGraphSerDes:

    def serialize(self, directly_follows_graph: DirectlyFollowsGraph) -> string:
        serializable_relations = dict()
        relations = directly_follows_graph.relations
        for relation in relations:
            serializable_relations[str(relation)] = (relation, relations[relation])

        relations = json.dumps(serializable_relations)
        start_activities = json.dumps(directly_follows_graph.start_activities)
        end_activities = json.dumps(directly_follows_graph.end_activities)

        result = dict()
        result["relations"] = relations
        result["start_activities"] = start_activities
        result["end_activities"] = end_activities

        return json.dumps(result)

    def deserialize(self, directly_follows_graph: str) -> DirectlyFollowsGraph:
        directly_follows_graph_dict = json.loads(directly_follows_graph)
        relation_dict = json.loads(directly_follows_graph_dict["relations"])

        unwrapped_relations: Dict[tuple[string, string], int] = dict()
        for relation_key in relation_dict:
            relation = relation_dict[relation_key]
            unwrapped_relations[(relation[0][0], relation[0][1])] = relation[1]

        return DirectlyFollowsGraph(
            counted_relations=unwrapped_relations,
            start_activities=directly_follows_graph_dict["start_activities"],
            end_activities=directly_follows_graph_dict["end_activities"]
        )
