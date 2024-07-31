import string
from typing import List

from mining.heuristics.algorithms.petri_net_creator import HeuristicsResult
from mining.heuristics.results.directly_follows_graph import DirectlyFollowsGraph


class HeuristicsNetCreator:

    def __init__(self, dependency_threshold, and_threshold):
        self.dependency_threshold = dependency_threshold
        self.and_threshold = and_threshold

    def create_heuristics_net(self, directly_follows_graph: DirectlyFollowsGraph) -> HeuristicsResult:
        all_activities = []
        causal_activities = []
        concurrent_activities = []
        self.relations = directly_follows_graph.relations

        for relation1 in self.relations:
            for relation2 in self.relations:
                if not relation1 == relation2 and relation1[0] == relation2[0]:
                    and_measure = self.get_and_measure(
                        relation1[0],
                        relation2[1],
                        relation1[1]
                    )
                    if and_measure > self.and_threshold:
                        concurrent_activities.append(
                            (relation1[1], relation2[1])
                        )
                    else:
                        causal_activities.append(
                            (relation1[1], relation2[1])
                        )
        relations_as_list: List[tuple[string, string]] = []
        for relation in self.relations:
            relations_as_list.append(relation)

        return HeuristicsResult(
            all_activities=all_activities,
            start_activities=directly_follows_graph.start_activities,
            end_activities=directly_follows_graph.end_activities,
            relations=relations_as_list,
            concurrent_activities=concurrent_activities
        )

    def get_count(self, relation: tuple[string, string]) -> int:
        if relation in self.relations:
            return self.relations[relation]
        return 0

    def get_and_measure(self, a, b, c):
        ab = self.get_count((a, b))
        ac = self.get_count((a, c))
        bc = self.get_count((b, c))
        cb = self.get_count((c, b))
        return (bc + cb) / (ab + ac + 1)

