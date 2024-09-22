import unittest
import os
from unittest.mock import Mock
from src.plugins.MondayPlugin import MondayPlugin
from monday import MondayClient

class TestMondayPlugin(unittest.TestCase):
    def setUp(self):
        MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
        
        # Create real client
        self.real_client = MondayClient(
            api_key=MONDAY_API_KEY
        )
        
        # Create mock client
        self.mock_client = Mock(spec=MondayClient)
        
        # Initialize plugin with real client
        self.plugin = MondayPlugin(self.real_client)
        
        # Initialize plugin with mock client for testing
        self.mock_plugin = MondayPlugin(self.mock_client)

    def test_connection(self):
        self.assertTrue(self.plugin.connect())

    def test_get_data_last_day_project_hours(self):
        # Setup mock return value
        mock_time_series = {
            "total_project_hours_logged": Mock(dataPoints=[4, 5, 6])
        }
        self.mock_client.get_data_last_day.return_value = mock_time_series
        
        timeSeriesList = self.mock_plugin.get_data_last_day()
        self.assertIsNotNone(timeSeriesList)
        self.assertTrue(len(timeSeriesList) > 0)
        self.assertTrue("total_project_hours_logged" in timeSeriesList)
        self.assertTrue(len(timeSeriesList["total_project_hours_logged"].dataPoints) > 0)

if __name__ == '__main__':
    unittest.main()