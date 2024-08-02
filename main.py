from conf import bootstrap_server, connect_jar_location
from flink.pipeline.heuristics_miner_flink import HeuristicsMinerFlinkSimple


if __name__ == '__main__':
    miner = HeuristicsMinerFlinkSimple(
        bootstrap_server=bootstrap_server,
        input_topic="process",
        output_topic="petri-net",
        group="my-group",
        bucket_size=20,
        parallelism=1,
        connect_jar_location=connect_jar_location
    )
    miner.run()


