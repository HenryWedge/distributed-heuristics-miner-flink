import json

from kafka import KafkaConsumer

from conformance.source.event_log.event_log_source import EventLogSource
from heuristics.datastructure.event import Event
from heuristics.results.event_log import SerializableEventLog


class KafkaEventLogSource(EventLogSource):

    def __init__(self, topic, bootstrap_server, group_id):
        self.log_kafka_consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_server,
            group_id=group_id,
        )
        self.last_event_log = None

    def get_event_log(self):
        result = self.log_kafka_consumer.poll(max_records=10)
        for partition in result:
            consumed_records = result[partition]
            log = []
            for record in consumed_records:
                record_dict = json.loads(record.value.decode())
                log.append(
                    Event(
                        timestamp=record_dict["timestamp"],
                        sensor_value=record_dict["sensor_value"],
                        sensor_name=record_dict["sensor_name"],
                        case_id=record_dict["case_id"]
                    )
                )
            event_log = SerializableEventLog(log)
            self.last_event_log = event_log
            return event_log
        return self.last_event_log
