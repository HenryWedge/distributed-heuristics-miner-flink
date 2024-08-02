import pm4py
from pm4py.algo.discovery.heuristics.variants import classic as heu_algorithm

from mining.petri_net_creator import convert_to_petri_net, test_cliques


def import_xes(file_path):
    test_cliques()
    event_log = pm4py.read_xes(file_path)
    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    heuristics_net = pm4py.discover_heuristics_net(event_log)
    petrinet = convert_to_petri_net(heuristics_net)

    print("Start activities: {}\nEnd activities: {}".format(start_activities, end_activities))
    #pm4py.view_petri_net(petri_net[0])
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
    precision_alignment = pm4py.precision_alignments(event_log, petri_net, initial_marking, final_marking)
    precision_footprints = pm4py.precision_footprints(event_log, petri_net, initial_marking, final_marking)
    fitness_token_based_replay = pm4py.fitness_token_based_replay(event_log, petri_net, initial_marking, final_marking)
    fitness_alignment = pm4py.fitness_alignments(event_log, petri_net, initial_marking, final_marking)
    #fitness_footprints = pm4py.fitness_footprints(event_log, petri_net, initial_marking, final_marking)

    pm4py.convert_to_petri_net()
    print("Precision Token Based Replay: " + str(precision_token_based_replay))
    print("Precision Alignment: " + str(precision_alignment))
    #print("Precision Footprint: " + str(precision_footprints))


    print("Fitness Token Based Replay: " + str(fitness_token_based_replay))
    print("Fitness Alignment: " + str(fitness_alignment))
    #print("Fitness Footprint: " + str(fitness_footprints))
    pm4py.view_heuristics_net(heuristics_net)


if __name__ == "__main__":
    import_xes("/resources/running-example.xes")
