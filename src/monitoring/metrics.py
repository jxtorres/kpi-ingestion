# Utility class for logging timeseries metrics for observability of the framework.
# Metrics tracked will include:
# - Number of PLUGIN API ERRORS
# - Number of Database Errors
# - Number of Grafana API Errors

# - Resource utilization of Database docker resources
# - Resource utilization of Grafana docker resources

# - Number of PLUGIN Ingest Function invocations
# - Number of Data records (KPIs) written to the database

import prometheus_client
from prometheus_client import Counter, Gauge
import docker
import threading
import time

class MetricsLogger:
    def __init__(self):
        # Counters for errors and invocations
        self.database_errors = Counter('database_errors', 'Number of Database Errors')
        self.grafana_api_errors = Counter('grafana_api_errors', 'Number of Grafana API Errors')
        self.ingest_function_invocations = Counter('ingest_function_invocations', 'Number of Plugin Ingest Function invocations')
        self.data_records_written = Counter('data_records_written', 'Number of Data records (KPIs) written to the database')

        # Gauges for resource utilization
        self.db_cpu_usage = Gauge('db_cpu_usage', 'CPU usage of Database container')
        self.db_memory_usage = Gauge('db_memory_usage', 'Memory usage of Database container')
        self.grafana_cpu_usage = Gauge('grafana_cpu_usage', 'CPU usage of Grafana container')
        self.grafana_memory_usage = Gauge('grafana_memory_usage', 'Memory usage of Grafana container')

        # Initialize Docker client
        self.docker_client = docker.from_env()

        # Start the background thread for updating utilization stats
        self.stop_thread = threading.Event()
        self.bg_thread = threading.Thread(target=self._update_utilization_periodically)
        self.bg_thread.start()

        # Replace the single plugin_api_errors counter with a dict
        self.plugin_api_errors = {}

    def increment_plugin_api_errors(self, plugin_name, quantity=1):
        """
        Increment the plugin API error counter for a specific plugin.
        
        :param plugin_name: The name of the plugin
        :param quantity: The number of errors to add (default is 1)
        """
        if plugin_name not in self.plugin_api_errors:
            self.plugin_api_errors[plugin_name] = Counter(
                'plugin_api_errors',
                'Number of Plugin API Errors',
                ['plugin_name']
            )
        self.plugin_api_errors[plugin_name].labels(plugin_name=plugin_name).inc(quantity)

    def increment_database_errors(self):
        self.database_errors.inc()

    def increment_grafana_api_errors(self):
        self.grafana_api_errors.inc()

    def increment_ingest_function_invocations(self):
        self.ingest_function_invocations.inc()

    def increment_data_records_written(self, count=1):
        self.data_records_written.inc(count)

    def update_resource_utilization(self):
        try:
            # Update Database container metrics
            db_container = self.docker_client.containers.get('database')  # Assuming 'database' is the container name
            db_stats = db_container.stats(stream=False)
            self.db_cpu_usage.set(db_stats['cpu_stats']['cpu_usage']['total_usage'])
            self.db_memory_usage.set(db_stats['memory_stats']['usage'])

            # Update Grafana container metrics
            grafana_container = self.docker_client.containers.get('grafana')  # Assuming 'grafana' is the container name
            grafana_stats = grafana_container.stats(stream=False)
            self.grafana_cpu_usage.set(grafana_stats['cpu_stats']['cpu_usage']['total_usage'])
            self.grafana_memory_usage.set(grafana_stats['memory_stats']['usage'])
        except Exception as e:
            print(f"Error updating resource utilization: {str(e)}")

    def _update_utilization_periodically(self):
        while not self.stop_thread.is_set():
            self.update_resource_utilization()
            time.sleep(60)  # Sleep for 60 seconds

    def start_http_server(self, port=8000):
        prometheus_client.start_http_server(port)

    def stop(self):
        self.stop_thread.set()
        self.bg_thread.join()

# Usage example:
# metrics_logger = MetricsLogger()
# metrics_logger.start_http_server()
# 
# # Your application code here
# 
# # When shutting down:
# metrics_logger.stop()



# Plugin API USAGE Example
##
# # Increment error count for 'plugin_a' by 1
# metrics_logger.increment_plugin_api_errors('plugin_a')
#
# # Increment error count for 'plugin_b' by 3
# metrics_logger.increment_plugin_api_errors('plugin_b', 3)

