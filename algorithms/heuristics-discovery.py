import os

from datastructure import LossyCountingDictionary, CaseIdDictionary, Event, MiningResult


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


#if __name__ == '__main__':
#    heuristics_miner = HeuristicsDiscovery(3)
#    activities = ["A", "B", "C", "D", "E"]
#    i = 0
#    while True:
#        time.sleep(1)
#        print(heuristics_miner.process(Event(i, f"Activity {activities[int(random.uniform(0, len(activities)))]}")))

    #start_activities = heuristics_miner.start_activities
    #end_activities = heuristics_miner.end_activities
    #graph = heuristics_miner.relations
#
    #graphAsCounter = dict()
    #for relation in heuristics_miner.relations:
    #    graphAsCounter[(relation.predecessor, relation.successor)] = heuristics_miner.relations[relation].frequency
#
    #dfg = DirectlyFollowsGraph(
    #    graph=graphAsCounter,
        #start_activities=Counter(start_activities),
        #end_activities=Counter(end_activities)
    #)

    #pm4py.view_dfg(graphAsCounter, start_activities, end_activities)
    #petri_net = pm4py.convert_to_petri_net(graphAsCounter)
    #pm4py.view_petri_net(petri_net=petri_net[0])
    #pm4py.conformance_diagnostics_token_based_replay()