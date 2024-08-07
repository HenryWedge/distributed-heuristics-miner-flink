import os

from dotenv import load_dotenv
from flink.pipeline.flink_pipeline_factory import FlinkPipelineFactory


if __name__ == '__main__':
    #load_dotenv()

    factory = FlinkPipelineFactory(
        bootstrap_server=os.environ["bootstrap_server"],
        input_topic=os.environ["input_topic"],
        output_topic=os.environ["output_topic"],
        group=os.environ["group"],
        bucket_size=int(os.environ["bucket_size"]),
        parallelism=int(os.environ["parallelism"]),
        connect_jar_location=f"file://{os.environ['path_to_connect_jar']}/resources/flink-sql-connector-kafka-1.17.2.jar"
    )

    miner = factory.get_pipeline(variant="parallelized")
    miner.run()
