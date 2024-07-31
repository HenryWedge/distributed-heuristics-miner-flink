import json

from pyflink.common import WatermarkStrategy, Duration, SimpleStringSchema, Time
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.window import TumblingEventTimeWindows

from mining.flink.wrapper.heuristics_discovery_flink import DirectlyFollowsGrapgCreator
from mining.flink import MyTimestampAssigner, Event, SumWindowFunction

class HeuristicsMinerFlink:

    def __init__(self, bootstrap_server, topics, group, bucket_size, parallelism):
        self.bootstrap_server = bootstrap_server
        self.topics = topics
        self.group = group
        self.bucket_size = bucket_size
        self.parallelism = parallelism

    def mine(self):
        print("start")
        env = StreamExecutionEnvironment.get_execution_environment()
        env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
        env.add_jars("file:///home/hre/Programs/flink-sql-connector-kafka-1.17.2.jar")
        # TODO adjust parallelism
        env.set_parallelism(1)

        watermark_strategy = WatermarkStrategy \
        .for_bounded_out_of_orderness(Duration.of_seconds(1)) \
        .with_timestamp_assigner(MyTimestampAssigner())

        source = KafkaSource.builder() \
            .set_bootstrap_servers(self.bootstrap_server) \
            .set_topics(self.topics) \
            .set_group_id(self.group) \
            .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
            .set_value_only_deserializer(SimpleStringSchema()) \
            .build()

        heuristics_discovery2 = DirectlyFollowsGrapgCreator(self.bucket_size)

        env.from_source(
            source,
            WatermarkStrategy.for_monotonous_timestamps(),
            "kafka-source")\
        .map(lambda json_string: Event(**json.loads(json_string)))\
        .assign_timestamps_and_watermarks(watermark_strategy)\
        .map(lambda event: heuristics_discovery2.process(event))\
        .key_by(lambda result: 0) \
        .window(TumblingEventTimeWindows.of(Time.minutes(1)))\
        .apply(SumWindowFunction()) \
        .print()

        env.execute()