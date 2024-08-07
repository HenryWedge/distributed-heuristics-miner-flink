import os
import random

from flask import Flask

from conformance.algorithm.conformance import ConformanceMetrics
from conformance.source.event_log.kafka_event_log_source import KafkaEventLogSource
from conformance.source.model.kafka_model_source import KafkaModelSource
from prometheus_flask_exporter import PrometheusMetrics


model_topic = os.environ["MODEL_TOPIC"]
validation_topic = os.environ["VALIDATION_TOPIC"]
bootstrap_server = os.environ["BOOTSTRAP_SERVER"]
conformance_metrics = ConformanceMetrics(
    model_source=KafkaModelSource(
        topic=model_topic,
        bootstrap_server=bootstrap_server,
        group_id="metrics_model"
    ),
    event_log_source=KafkaEventLogSource(
        topic=validation_topic,
        bootstrap_server=bootstrap_server,
        group_id="metrics_log"
    )
)


def fetch():
    conformance_metrics.calculate_metrics()
    return 0.0


def get_precision_token_based_replay():
    return conformance_metrics.precision_token_based_replay


def get_precision_alignments():
    return conformance_metrics.precision_alignments


def get_fitness_token_based_replay():
    return conformance_metrics.fitness_token_based_replay


def get_fitness_alignments():
    return conformance_metrics.fitness_alignments


app = Flask(__name__)
metrics = PrometheusMetrics(app)
a = metrics.info('a', '').set_function(fetch)
precision_token_based_replay = metrics.info('precision_token_based_replay', 'Application info').set_function(get_precision_token_based_replay)
fitness_token_based_replay = metrics.info('fitness_token_based_replay', 'Application info2').set_function(get_fitness_token_based_replay)
precision_alignments = metrics.info('precision_alignments', 'Application info3').set_function(get_precision_alignments)
fitness_alignments = metrics.info('fitness_alignments', 'Application info4').set_function(get_fitness_alignments)

metrics.start_http_server(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)