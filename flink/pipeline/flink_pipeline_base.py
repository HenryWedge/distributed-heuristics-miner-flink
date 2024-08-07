from pyflink.common import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer, KafkaRecordSerializationSchema, \
    KafkaSink


class FlinkPipelineBase:

    def __init__(self,
                 bootstrap_server,
                 input_topic,
                 output_topic,
                 group,
                 parallelism,
                 connect_jar_location):
        self.bootstrap_server = bootstrap_server
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group = group
        self.parallelism = parallelism
        self.connect_jar_location = connect_jar_location

    def get_kafka_source(self):
        return KafkaSource.builder() \
            .set_bootstrap_servers(self.bootstrap_server) \
            .set_topics(self.input_topic) \
            .set_group_id(self.group) \
            .set_property("enable.auto.commit", "true")\
            .set_value_only_deserializer(SimpleStringSchema()) \
            .build()

    def get_kafka_sink(self):
        record_serializer = KafkaRecordSerializationSchema.builder() \
            .set_topic(self.output_topic) \
            .set_value_serialization_schema(SimpleStringSchema()) \
            .build()

        return KafkaSink.builder() \
            .set_bootstrap_servers(self.bootstrap_server) \
            .set_record_serializer(record_serializer) \
            .build()

    def get_env(self):
        env = StreamExecutionEnvironment.get_execution_environment()
        env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
        env.add_jars(self.connect_jar_location)
        return env
