import json
from datetime import datetime
from typing import Any, Iterable

from pyflink.common import WatermarkStrategy, Types, SimpleStringSchema, Time, Duration
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode, WindowFunction
from pyflink.datastream.connectors.kafka import FlinkKafkaProducer, KafkaSource, \
    KafkaOffsetsInitializer
from pyflink.datastream.formats.json import JsonRowSerializationSchema
from pyflink.datastream.window import TumblingEventTimeWindows, CountWindow

from mining.datastructure import Event
from mining.flink.wrapper.heuristics_discovery_flink import DirectlyFollowsGrapgCreator


class MyTimestampAssigner(TimestampAssigner):

    def extract_timestamp(self, value: Any, record_timestamp: int) -> int:
        return int(datetime.strptime(str(value.timestamp), '%Y-%m-%d %H:%M:%S').timestamp()) * 1000


def write_to_kafka(env):
    type_info = Types.ROW([Types.INT(), Types.STRING()])
    ds = env.from_collection(
        [(1, 'hi'), (2, 'hello'), (3, 'hi'), (4, 'hello'), (5, 'hi'), (6, 'hello'), (6, 'hello')],
        type_info=type_info)

    serialization_schema = JsonRowSerializationSchema.Builder() \
        .with_type_info(type_info) \
        .build()
    kafka_producer = FlinkKafkaProducer(
        topic='test_json_topic',
        serialization_schema=serialization_schema,
        producer_config={'bootstrap.servers': 'localhost:9092', 'group.id': 'test_group'}
    )

    # note that the output type of ds must be RowTypeInfo
    ds.add_sink(kafka_producer)
    env.execute()


class SumWindowFunction(WindowFunction[Event, Event, str, CountWindow]):
    def apply(self, key: str, window: CountWindow, inputs: Iterable[Event]):
        result = []
        for i in inputs:
            result.append(i)
        return result


def mine_model():
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
        .set_bootstrap_servers("kube1-1:30376") \
        .set_topics("process2") \
        .set_group_id("group-0") \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    heuristics_discovery = DirectlyFollowsGrapgCreator(20)

    env.from_source(
        source,
        WatermarkStrategy.for_monotonous_timestamps(),
        "kafka-source")\
    .map(lambda json_string: Event(**json.loads(json_string)))\
    .assign_timestamps_and_watermarks(watermark_strategy)\
    .map(lambda event: heuristics_discovery.process(event))\
    .key_by(lambda result: 0) \
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))\
    .apply(SumWindowFunction()) \
    .print()

    env.execute()

#mine_model()