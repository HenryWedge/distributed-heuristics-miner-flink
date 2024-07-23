from typing import Dict


class Event:
    def __init__(self, caseId, activity):
        self.caseId = caseId
        self.activity = activity


class MiningResult:
    def __init__(self, graph, start_activities = None, end_activities = None):
        self.graph = graph
        self.start_activities = start_activities
        self.end_activities = end_activities

    def __str__(self):
        output = ""
        for a in self.graph:
            output += f"{a}:{self.graph[a]}, "
        return output


class FrequencyDeltaPair:
    def __init__(self, delta: int):
        self.frequency = 1
        self.delta = delta

    def is_relevant(self, current_bucket_number) -> bool:
        return self.frequency + self.delta >= current_bucket_number

    def increment(self, current_bucket_number):
        self.frequency += 1
        self.delta = current_bucket_number

    def __str__(self):
        return f"({self.frequency}:{self.delta})"


class DirectlyFollowsRelation:
    def __init__(self, predecessor, successor):
        self.predecessor = predecessor
        self.successor = successor

    def __str__(self):
        return f"<{self.predecessor}, {self.successor}>"


class CountedDirectlyFollowsRelation:
    def __init__(self, directly_follows_relation, count: int):
        self.directly_follows_relation = directly_follows_relation
        self.count = count

    def __str__(self):
        return f"{self.directly_follows_relation}:{self.count}"


class LossyCountingDictionary:
    def __init__(self):
        self.dictionary = dict()

    def insert(self, item, bucket_number) -> None:
        if item in self.dictionary:
            self.dictionary[item].increment(bucket_number)
        else:
            self.dictionary[item] = FrequencyDeltaPair(bucket_number)

    def get_items_with_count(self):
        items_with_count = dict()
        items = self.dictionary.copy()
        for item in items:
            items_with_count[item] = self.dictionary[item].frequency
        return items_with_count

    def clean_up(self, bucket_number) -> None:
        relevant_items = dict()
        for key in self.dictionary:
            frequency_delta_pair = self.dictionary[key]
            if frequency_delta_pair.is_relevant(bucket_number):
                relevant_items[key] = frequency_delta_pair
        self.dictionary = relevant_items


class CaseIdDictionary:
    def __init__(self):
        self.start_activities = dict()
        self.dictionary = dict()

    def insert(self, case_id, activity) -> DirectlyFollowsRelation | None:
        if case_id not in self.dictionary:
            self.dictionary[case_id] = activity
            self.start_activities[case_id] = activity
            return None

        last_activity = self.dictionary[case_id]
        relation = DirectlyFollowsRelation(last_activity, activity)
        self.dictionary[case_id] = activity
        return relation

    def get_start_activities(self) -> Dict[str, int]:
        return self.start_activities

    def get_end_activities(self) -> Dict[str, int]:
        end_activities = dict()
        for case in self.dictionary:
            activity = self.dictionary[case]
            if activity in end_activities:
                end_activities[activity] += 1
            else:
                end_activities[activity] = 1

        return end_activities
