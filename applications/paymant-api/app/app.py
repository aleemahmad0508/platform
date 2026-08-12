from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# -----------------------------
# Prometheus Metrics
# -----------------------------
metrics = PrometheusMetrics(app)

# -----------------------------
# OpenTelemetry Configuration
# -----------------------------
resource = Resource.create({
    "service.name": "paymant-api"
})

trace.set_tracer_provider(
    TracerProvider(resource=resource)
)

tracer_provider = trace.get_tracer_provider()

otlp_exporter = OTLPSpanExporter(
    endpoint="otel-collector-collector.observability.svc.cluster.local:4317",
    insecure=True
)

tracer_provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Automatically trace Flask requests
FlaskInstrumentor().instrument_app(app)

# -----------------------------
# Starter Route
# -----------------------------
@app.route("/")
def home():
    return "Welcome to paymant-api"

@app.route("/health")
def health():
    return "Healthy khan khan "

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # nosec B104