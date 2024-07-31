import string
from typing import List


class HeuristicsResult:
    def __init__(self, all_activities, start_activities, end_activities, relations, concurrent_activities):
        self.all_activities: List[string] = all_activities
        self.start_activities: List[string] = start_activities
        self.end_activities: List[string] = end_activities
        self.relations: List[tuple[string, string]] = relations
        self.concurrent_activities: List[tuple[string, string]] = concurrent_activities

    def get_successors_of(self, activity):
        successors = []
        for relation in self.relations:
            if relation[0] == activity:
                successors.append(relation[1])
        return successors

    def get_concurrent_successors_of(self, activity):
        concurrent_successors = []
        for concurrent in self.concurrent_activities:
            if concurrent[0] == activity:
                concurrent_successors.append(concurrent[1][0])
                concurrent_successors.append(concurrent[1][1])
        return concurrent_successors
