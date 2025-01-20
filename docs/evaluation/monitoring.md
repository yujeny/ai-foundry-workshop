# 📈 Monitoring and Analysis 🔍

This section covers real-time monitoring and analysis of your AI agent's performance using Azure AI Evaluation. Keep your health advisor in peak condition! 💪 ⚡

## Real-time Monitoring

```python
# Import required packages
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import EvaluationClient
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from azure.core.tracing.opentelemetry import AzureMonitorTraceExporter
import azure.monitor.opentelemetry._autoinstrument

# Initialize OpenTelemetry
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
meter_provider = MeterProvider()
metrics.set_meter_provider(meter_provider)

# Configure Azure Monitor exporter
exporter = AzureMonitorTraceExporter(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
)

# Create monitoring aspects
monitoring_aspects = {
    'performance_tracking': True,   # Track response times
    'resource_utilization': True,   # Monitor CPU, memory
    'error_detection': True,        # Detect and log errors
    'alert_configuration': True,    # Set up alerts
    'response_timing': True,        # Track latencies
    'usage_patterns': True          # Monitor usage
}

# Initialize tracer
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Create metrics
response_time = meter.create_histogram(
    name="response_time",
    description="Time taken to process requests",
    unit="ms"
)

# Example monitoring implementation
def monitor_health_advisor():
    with tracer.start_as_current_span("health_advisor_monitoring") as span:
        try:
            # Monitor performance metrics
            span.set_attribute("monitoring_type", "health_advisor")
            
            # Record response time
            with response_time.record_duration():
                # Your health advice logic here
                pass
                
        except Exception as e:
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            span.record_exception(e)
```

### Key Monitoring Aspects
- Performance tracking
- Resource utilization
- Error detection
- Alert configuration
- Response timing
- Usage patterns

## Analysis Tools
- Performance dashboards
- Metric visualization
- Trend analysis
- Anomaly detection
- Resource optimization
- Cost analysis

## Interactive Workshop

To get hands-on experience with monitoring and analysis, we've prepared an interactive Jupyter notebook that will guide you through:
- Setting up real-time monitoring
- Configuring alerts and notifications
- Analyzing performance trends
- Creating dashboards
- Implementing continuous improvement

[Launch Monitoring Workshop](../2-notebooks/3-quality_attributes/1-Observability.ipynb)

This notebook provides a practical implementation of monitoring and analysis tools. You'll work directly with the Azure AI Evaluation SDK to track and optimize your health advisor's performance and safety measures in real-time. 📊

Next: [Conclusion](../conclusion.md)
