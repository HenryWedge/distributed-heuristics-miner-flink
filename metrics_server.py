from flask import Flask

from conf import bootstrap_server
from conformance.algorithm.conformance import ConformanceMetrics
from conformance.metrics.conformance_server import MetricsView
from conformance.source.event_log.kafka_event_log_source import KafkaEventLogSource
from conformance.source.model.kafka_model_source import KafkaModelSource


if __name__ == '__main__':
    app = Flask(__name__)
    conformance_metrics = ConformanceMetrics(
        model_source=KafkaModelSource(
            topic="petri-net",
            bootstrap_server=bootstrap_server,
            group_id="metrics_model"
        ),
        event_log_source=KafkaEventLogSource(
            topic="process2",
            bootstrap_server=bootstrap_server,
            group_id="metrics_log"
        )
    )
    MetricsView.register(app, init_argument=conformance_metrics, route_base="/")
    app.run()
