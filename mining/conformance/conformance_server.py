import json

from flask import Flask

from mining.conformance.algorithm.conformance import ConformanceMetrics

app = Flask(__name__)

conformance_metrics = ConformanceMetrics()


@app.route("/metrics")
def metrics():
    conformance_metrics.calculate_metrics()

    return json.dumps(
        {
            "precision_token_based_replay": conformance_metrics.precision_token_based_replay,
            "fitness_token_based_replay": conformance_metrics.fitness_token_based_replay,
            "precision_alignments": conformance_metrics.precision_alignments,
            "fitness_alignments": conformance_metrics.fitness_alignments
        }
    )