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
    "service.name": "{{SERVICE_NAME}}"
})

trace.set_tracer_provider(
    TracerProvider(resource=resource)
)

tracer_provider = trace.get_tracer_provider()

otlp_exporter = OTLPSpanExporter(
    endpoint="{{OTEL_ENDPOINT}}",
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
    return "Welcome tooo {{SERVICE_NAME}}"

@app.route("/health")
def health():
    return "Healthy"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port={{PORT}}) # nosec B104