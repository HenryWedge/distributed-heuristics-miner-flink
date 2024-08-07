import json

from kafka import KafkaConsumer

from conformance.source.model.model_source import ModelSource
from flink.wrapper.petri_net_serializer import PetriNetSerDes
from heuristics.results.petri_net import SerializablePetriNet


class KafkaModelSource(ModelSource):

    def __init__(self, topic, bootstrap_server, group_id):
        self.petri_net = None
        self.model_kafka_consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_server,
            group_id=group_id,
        )
        self.last_petri_net = None

    def get_petri_net(self) -> SerializablePetriNet | None:
        result = self.model_kafka_consumer.poll()
        for partition in result:
            consumed_records = result[partition]
            latest_record = consumed_records[-1]
            petri_net = PetriNetSerDes().deserialize(latest_record.value.decode())
            self.last_petri_net = petri_net
            return petri_net

        return self.last_petri_net
