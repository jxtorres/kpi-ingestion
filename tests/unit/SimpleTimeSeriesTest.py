import unittest
from datetime import datetime
from src.data_processing.SimpleTimeSeries import SimpleTimeSeries

class TestSimpleTimeSeries(unittest.TestCase):
    def setUp(self):
        self.model = SimpleTimeSeries("Test Series")

    def test_initial_state(self):
        self.assertEqual(self.model.series_name, "Test Series")
        self.assertEqual(len(self.model.data_points), 0)

    def test_add_data_point(self):
        self.model.add_data_point(10.5, datetime(2023, 1, 1, 12, 0))
        self.assertEqual(len(self.model.data_points), 1)
        self.assertEqual(self.model.data_points[0].value, 10.5)
        self.assertEqual(self.model.data_points[0].date_time, datetime(2023, 1, 1, 12, 0))

    def test_add_multiple_data_points(self):
        data_points = [
            (15.0, datetime(2023, 1, 1, 12, 0)),
            (16.5, datetime(2023, 1, 2, 12, 0)),
            (14.5, datetime(2023, 1, 3, 12, 0))
        ]
        self.model.add_data_points(data_points)
        self.assertEqual(len(self.model.data_points), 3)

    def test_to_string(self):
        self.model.add_data_point(10.5, datetime(2023, 1, 1, 12, 0))
        expected_string = "Test Series: [(2023-01-01 12:00:00, 10.5)]"
        self.assertEqual(str(self.model), expected_string)

    def test_forecast(self):
        # Add some data points
        data_points = [
            (15.0, datetime(2023, 1, 1, 12, 0)),
            (16.5, datetime(2023, 1, 2, 12, 0)),
            (14.5, datetime(2023, 1, 3, 12, 0))
        ]
        self.model.add_data_points(data_points)
        
        # Test that forecast returns a non-None value
        forecast = self.model.forecast()
        self.assertIsNotNone(forecast)
        
        # You might want to add more specific tests for the forecast method
        # depending on how it's implemented in the SimpleTimeSeries class

if __name__ == '__main__':
    unittest.main()