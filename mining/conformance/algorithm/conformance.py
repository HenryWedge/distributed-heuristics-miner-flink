import pm4py
from pm4py import Marking, PetriNet
from pm4py.objects.log.obj import EventLog

from mining.conformance.data_input import DataInput


class ConformanceMetrics:

    def __init__(self):
        self.precision_token_based_replay = 0.0
        self.fitness_token_based_replay = 0.0
        self.fitness_alignments = 0.0
        self.precision_alignments = 0.0
        self.data_input = DataInput()

    def get_precision(self, evaluation_function) -> float:
        try:
            return evaluation_function()
        except Exception as error:
            print(error)
            return 0.0

    def get_fitness(self, evaluation_function) -> float:
        try:
            return evaluation_function()["average_trace_fitness"]
        except Exception as error:
            print(error)
            return 0.0

    def calculate_metrics(self):
        event_log: EventLog = self.data_input.get_event_log()
        petri_net, initial_marking, final_marking = self.data_input.get_petri_net()

        self.precision_token_based_replay = self.get_precision(
            lambda: pm4py.precision_token_based_replay(event_log, petri_net, initial_marking, final_marking))
        self.fitness_token_based_replay = self.get_fitness(
            lambda: pm4py.fitness_token_based_replay(event_log, petri_net, initial_marking, final_marking))
        self.fitness_alignments = self.get_fitness(
            lambda: pm4py.fitness_alignments(event_log, petri_net, initial_marking, final_marking))
        self.precision_alignments = self.get_precision(
            lambda: pm4py.precision_alignments(event_log, petri_net, initial_marking, final_marking))
