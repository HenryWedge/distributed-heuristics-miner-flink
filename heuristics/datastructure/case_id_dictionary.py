from typing import Dict

from heuristics.datastructure.directly_follows_relation import DirectlyFollowsRelation


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
        start_activities = []
        for start_activity_key in self.start_activities:
            start_activities.append(self.start_activities[start_activity_key])
        return start_activities

    def get_end_activities(self) -> Dict[str, int]:
        end_activities = dict()
        for case in self.dictionary:
            activity = self.dictionary[case]
            if activity in end_activities:
                end_activities[activity] += 1
            else:
                end_activities[activity] = 1

        return end_activities
