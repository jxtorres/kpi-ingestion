import unittest
from unittest.mock import Mock, patch
from src.data_processing.MetricDataLayer import MetricDataLayer
from src.models.SimpleTimeSeries import SimpleTimeSeries

# Testing the MetricDataLayer class. Methods under test should include write_time_series_data.
# It should trigger calls to a mock sql client. The function should write to the database or try to.
# The function should have an argument for an instance of SimpleTimeSeries. It should append these 
# data points to the SimpleTimeSeries in the database.
class TestMetricDataLayer(unittest.TestCase):
    def setUp(self):
        self.mock_sql_client = Mock()
        self.data_layer = MetricDataLayer(sql_client=self.mock_sql_client)

    def test_get_metrics(self):
        self.assertIsNotNone(self.data_layer.get_metrics())

    @patch('src.data_processing.MetricDataLayer.SimpleTimeSeries')
    def test_write_time_series_data(self, mock_simple_time_series):
        # Arrange
        mock_time_series = Mock(spec=SimpleTimeSeries)
        mock_time_series.metric_id = 1
        mock_time_series.data_points = [(1620000000, 10.5), (1620086400, 11.2)]
        
        # Act
        self.data_layer.write_time_series_data(mock_time_series)

        # Assert
        self.mock_sql_client.execute.assert_called_once()
        call_args = self.mock_sql_client.execute.call_args[0]
        self.assertIn("INSERT INTO time_series_data", call_args[0])
        self.assertIn("VALUES", call_args[0])
        self.assertEqual(len(call_args[1]), 6)  # 2 data points * 3 values each (metric_id, timestamp, value)

    def test_write_time_series_data_empty(self):
        # Arrange
        mock_time_series = Mock(spec=SimpleTimeSeries)
        mock_time_series.metric_id = 1
        mock_time_series.data_points = []

        # Act
        self.data_layer.write_time_series_data(mock_time_series)

        # Assert
        self.mock_sql_client.execute.assert_not_called()

    def test_write_time_series_data_error(self):
        # Arrange
        mock_time_series = Mock(spec=SimpleTimeSeries)
        mock_time_series.metric_id = 1
        mock_time_series.data_points = [(1620000000, 10.5)]
        self.mock_sql_client.execute.side_effect = Exception("Database error")

        # Act & Assert
        with self.assertRaises(Exception):
            self.data_layer.write_time_series_data(mock_time_series)

if __name__ == '__main__':
    unittest.main()
