import json
import string

from heuristics.results.petri_net import SerializablePetriNet

class PetriNetSerializer:

    def serialize(self, petri_net: SerializablePetriNet) -> string:
        petri_net_dict = dict()
        petri_net_dict["places"] = list(petri_net.places)
        petri_net_dict["transitions"] = list(petri_net.transitions)
        petri_net_dict["arc_place_transition"] = list(petri_net.arc_place_transition)
        petri_net_dict["arc_transition_place"] = list(petri_net.arc_transition_place)
        petri_net_dict["start_activities"] = list(petri_net.start_activities)
        petri_net_dict["end_activities"] = list(petri_net.end_activities)

        return json.dumps(petri_net_dict)