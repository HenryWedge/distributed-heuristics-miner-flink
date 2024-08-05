import os

from dotenv import load_dotenv

from conf import bootstrap_server
from flink.pipeline.flink_pipeline_factory import FlinkPipelineFactory


if __name__ == '__main__':
    load_dotenv()

    factory = FlinkPipelineFactory(
        bootstrap_server=bootstrap_server,
        input_topic="process",
        output_topic="petri-net",
        group="my-group",
        bucket_size=20,
        parallelism=1,
        connect_jar_location=f"file://{os.environ['path_to_connect_jar']}/resources/flink-sql-connector-kafka-1.17.2.jar"
    )

    miner = factory.get_pipeline(variant="parallelized")
    miner.run()
