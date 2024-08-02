from pyflink.common import WatermarkStrategy, Types

from flink.pipeline.flink_pipeline_base import FlinkPipelineBase
from flink.wrapper.heuristics_discovery_flink import DirectlyFollowsGraphCreatorFlink
from flink.wrapper.heuristics_net_creator import HeuristicsNetCreatorFlink
from flink.wrapper.petri_net_creator_flink import PetriNetCreatorFlink


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
        petri_net_creator = PetriNetCreatorFlink()

        env.from_source(source, WatermarkStrategy.no_watermarks(), "kafka-source") \
            .map(lambda event:
                 directly_follows_graph_creator.process(event), Types.STRING()) \
            .map(lambda directly_follows_graph:
                 heuristics_net_creator.process(directly_follows_graph), Types.STRING()) \
            .map(lambda heuristics_net:
                 petri_net_creator.process(heuristics_net), Types.STRING()) \
            .sink_to(sink)

        env.execute()
