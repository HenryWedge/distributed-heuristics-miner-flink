from flink.pipeline.heuristics_miner_flink import HeuristicsMinerFlinkSimple
from flink.pipeline.heuristics_miner_flink_parallelized import HeuristicsMinerFlinkParallelized


class FlinkPipelineFactory:

    def __init__(
            self,
            bootstrap_server,
            input_topic,
            output_topic,
            bucket_size,
            group,
            parallelism,
            connect_jar_location
    ):
        self.bootstrap_server = bootstrap_server
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.bucket_size = bucket_size
        self.group = group
        self.parallelism = parallelism
        self.connect_jar_location = connect_jar_location

    def get_pipeline(self, variant):
        registry = dict()
        registry["simple"] = HeuristicsMinerFlinkSimple(
            self.bootstrap_server,
            self.input_topic,
            self.output_topic,
            self.group,
            self.bucket_size,
            self.parallelism,
            self.connect_jar_location
        )
        registry["parallelized"] = HeuristicsMinerFlinkParallelized(
            self.bootstrap_server,
            self.input_topic,
            self.output_topic,
            self.group,
            self.bucket_size,
            self.parallelism,
            self.connect_jar_location
        )
        return registry[variant]
