from src.monitoring.metrics import MetricsLogger

def handler(event, context):
    metrics_logger = MetricsLogger()
    metrics_logger.start_http_server(8000)

    # Your serverless function logic here
    
    # Example usage:
    metrics_logger.increment_plugin_api_errors('plugin_a')
    metrics_logger.increment_database_errors()
    
    # Clean up
    metrics_logger.stop()

    return {
        'statusCode': 200,
        'body': 'Function executed successfully'
    }
