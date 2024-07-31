from mining.heuristics.algorithms.petri_net_creator import PetriNetCreator

class PetriNetCreatorFlink:

    def __init__(self):
        self.petri_net_creator = PetriNetCreator()

    def process(self, heuristics_result: Heuri):
        self.heuristics_result = heuristics_result
        self.petri_net_creator.create_petri_net()