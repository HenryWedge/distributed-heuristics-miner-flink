import random
import string
import pm4py
from heuristics.results.event_log import SerializableEventLog
from heuristics.results.petri_net import SerializablePetriNet


class ConformanceMetrics:

    def __init__(self, model_source, event_log_source):
        self.precision_token_based_replay = 0.0
        self.fitness_token_based_replay = 0.0
        self.fitness_alignments = 0.0
        self.precision_alignments = 0.0
        self.model_source = model_source
        self.event_log_source = event_log_source
        self.random = random.random()

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
        serializable_event_log: SerializableEventLog = self.event_log_source.get_event_log()
        model: SerializablePetriNet = self.model_source.get_petri_net()

        if serializable_event_log and model:
            event_log = serializable_event_log.to_pm4py_event_log()
            petri_net, initial_marking, final_marking = model.to_pm4py_petri_net()

            self.precision_token_based_replay = self.get_precision(
                lambda: pm4py.precision_token_based_replay(event_log, petri_net, initial_marking, final_marking))
            self.fitness_token_based_replay = self.get_fitness(
                lambda: pm4py.fitness_token_based_replay(event_log, petri_net, initial_marking, final_marking))
            self.fitness_alignments = self.get_fitness(
                lambda: pm4py.fitness_alignments(event_log, petri_net, initial_marking, final_marking))
            self.precision_alignments = self.get_precision(
                lambda: pm4py.precision_alignments(event_log, petri_net, initial_marking, final_marking))
