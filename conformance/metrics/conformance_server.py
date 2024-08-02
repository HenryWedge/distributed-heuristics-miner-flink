from flask_classful import FlaskView


class MetricsView(FlaskView):

    def __init__(self, conformance_metrics):
        self.conformance_metrics = conformance_metrics

    def metrics(self):
        return self.conformance_metrics.calculate_metrics()
