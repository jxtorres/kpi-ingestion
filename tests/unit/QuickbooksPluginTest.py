import unittest
import os
from unittest.mock import Mock
from src.plugins.QuickbooksPlugin import QuickbooksPlugin
from quickbooks import QuickBooksClient

class TestQuickbooksPlugin(unittest.TestCase):
    def setUp(self):
        QUICKBOOKS_API_KEY = os.getenv("QUICKBOOKS_API_KEY")
        QUICKBOOKS_API_SECRET = os.getenv("QUICKBOOKS_API_SECRET")
        
        # Create real client
        self.real_client = QuickBooksClient(
            client_id=QUICKBOOKS_API_KEY,
            client_secret=QUICKBOOKS_API_SECRET,
            environment='sandbox'
        )
        
        # Create mock client
        self.mock_client = Mock(spec=QuickBooksClient)
        
        # Initialize plugin with real client
        self.plugin = QuickbooksPlugin(self.real_client)
        
        # Initialize plugin with mock client for testing
        self.mock_plugin = QuickbooksPlugin(self.mock_client)

    def test_connection(self):
        self.assertTrue(self.plugin.connect())

    def test_get_data_last_day_revenue(self):
        # Setup mock return value
        mock_time_series = {
            "net_revenue": Mock(dataPoints=[1, 2, 3])
        }
        self.mock_client.get_data_last_day.return_value = mock_time_series
        
        timeSeriesList = self.mock_plugin.get_data_last_day()
        self.assertIsNotNone(timeSeriesList)
        self.assertTrue(len(timeSeriesList) > 0)
        self.assertTrue("net_revenue" in timeSeriesList)
        self.assertTrue(len(timeSeriesList["net_revenue"].dataPoints) > 0)

if __name__ == '__main__':
    unittest.main()
