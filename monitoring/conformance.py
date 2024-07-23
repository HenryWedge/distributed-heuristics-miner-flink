from typing import List

from pandas import Timestamp, DataFrame
from pm4py.algo.discovery.heuristics.variants import classic as heu_algorithm
import pm4py

from algorithms.datastructure import Event


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


def calculate_metrics():
    event_log = DataFrame.from_dict(build_event_log_from_datastream())
    dfg = dict()
    dfg[('check ticket', 'decide')] = 6
    dfg[('check ticket', 'examine casually')] = 2
    dfg[('check ticket', 'examine thoroughly')] = 1
    dfg[('decide', 'pay compensation')] = 3
    dfg[('decide', 'reinitiate request')] = 3
    dfg[('decide', 'reject request')] = 3
    dfg[('examine casually', 'check ticket')] = 4
    dfg[('examine casually', 'decide')] = 2
    dfg[('examine thoroughly', 'check ticket')] = 2
    dfg[('examine thoroughly', 'decide')] = 1
    dfg[('register request', 'check ticket')] = 2
    dfg[('register request', 'examine casually')] = 3
    dfg[('register request', 'examine thoroughly')] = 1
    dfg[('reinitiate request', 'check ticket')] = 1
    dfg[('reinitiate request', 'examine casually')] = 1
    dfg[('reinitiate request', 'examine thoroughly')] = 1
    heuristics_net = heu_algorithm.apply_heu_dfg(dfg=dfg)
    petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(heuristics_net)

    precision_token_based_replay = pm4py.precision_token_based_replay(event_log, petri_net, initial_marking, final_marking)
    print(precision_token_based_replay)
    fitness_token_based_replay = pm4py.fitness_token_based_replay(event_log, petri_net, initial_marking, final_marking)
    print(fitness_token_based_replay)

    fitness_alignment = pm4py.fitness_alignments(event_log, petri_net, initial_marking, final_marking)
    print(fitness_alignment)
    precision_alignment = pm4py.precision_alignments(event_log, petri_net, initial_marking, final_marking)
    print(precision_alignment)

    #precision_footprints = pm4py.precision_footprints(event_log, petri_net, initial_marking, final_marking)
    #print(precision_footprints)
    #fitness_footprints = pm4py.fitness_footprints(event_log, petri_net, initial_marking, final_marking)
    #print(fitness_footprints)


if __name__ == '__main__':
    calculate_metrics()
