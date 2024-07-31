from pyflink.common import WatermarkStrategy, Types

from mining.flink.pipeline.flink_pipeline_base import FlinkPipelineBase
from mining.flink.wrapper.heuristics_discovery_flink import DirectlyFollowsGraphCreatorFlink
from mining.flink.wrapper.heuristics_net_creator import HeuristicsNetCreatorFlink

class HeuristicsMinerFlinkSimple:

    def __init__(self, bootstrap_server, input_topic, output_topic, group, bucket_size, parallelism,
                 connect_jar_location):
        self.flink_pipeline = FlinkPipelineBase(
            bootstrap_server,
            input_topic,
            output_topic,
            group,
            parallelism,
            connect_jar_location
        )
        self.bucket_size = bucket_size

    def run(self):
        env = self.flink_pipeline.get_env()
        source = self.flink_pipeline.get_kafka_source()
        sink = self.flink_pipeline.get_kafka_sink()

        directly_follows_graph_creator = DirectlyFollowsGraphCreatorFlink(self.bucket_size)
        heuristics_net_creator = HeuristicsNetCreatorFlink(0.5, 0.5)

        env.from_source(source, WatermarkStrategy.no_watermarks(), "kafka-source") \
            .map(lambda event:
                 directly_follows_graph_creator.process(event), Types.STRING()) \
            .map(lambda directly_follows_graph:
                 heuristics_net_creator.process(directly_follows_graph), Types.STRING()) \
            .print()
            #.sink_to(sink)

        env.execute()
