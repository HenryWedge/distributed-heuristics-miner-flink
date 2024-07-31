import string
from typing import Dict

from mining.heuristics.datastructure.directly_follows_relation import DirectlyFollowsRelation


class DirectlyFollowsGraph:

    def __init__(self, counted_relations: Dict[tuple[string, string], int], start_activities=None, end_activities=None):
        self.relations = counted_relations
        self.start_activities = start_activities
        self.end_activities = end_activities

    def __str__(self):
        output = ""
        for a in self.relations:
            output += f"{a}:{self.relations[a]}, "
        return output
