import unittest
from unittest.mock import Mock, patch
from src.data_processing.IngestFunction import IngestFunction



# Summary: Test the serverless function Ingest, Calling the function
# should trigger runs of the plugins, and it should generate some timeseries
# and then the Data layer will be invoked to write to the database. Setup
# will require a mock of the Data layer, and a mock of the plugins.
# the plugins should not be setup with real API keys, but should check that 
# the run method is called in a way that exercises the plugin logic.
class TestIngestFunction(unittest.TestCase):
    def setUp(self):
        self.function = IngestFunction()
        
        # Mock the Data layer
        self.mock_data_layer = Mock()
        
        # Mock the plugins
        self.mock_plugin1 = Mock()
        self.mock_plugin2 = Mock()
        
        # Set up mock plugins with dummy data
        self.mock_plugin1.run.return_value = [{'timestamp': '2023-04-01', 'value': 10}]
        self.mock_plugin2.run.return_value = [{'timestamp': '2023-04-01', 'value': 20}]
        
        # Patch the necessary components
        self.data_layer_patcher = patch('src.data_processing.IngestFunction.DataLayer', return_value=self.mock_data_layer)
        self.plugin1_patcher = patch('src.data_processing.IngestFunction.Plugin1', return_value=self.mock_plugin1)
        self.plugin2_patcher = patch('src.data_processing.IngestFunction.Plugin2', return_value=self.mock_plugin2)
        
        # Start the patchers
        self.data_layer_patcher.start()
        self.plugin1_patcher.start()
        self.plugin2_patcher.start()
    
    def tearDown(self):
        # Stop the patchers
        self.data_layer_patcher.stop()
        self.plugin1_patcher.stop()
        self.plugin2_patcher.stop()

    def test_process(self):
        # Call the process method
        result = self.function.process()
        
        # Assert that the process method returns True
        self.assertTrue(result)
        
        # Assert that the run method was called for each plugin
        self.mock_plugin1.run.assert_called_once()
        self.mock_plugin2.run.assert_called_once()
        
        # Assert that the Data layer's write method was called with the expected data
        expected_data = [
            {'timestamp': '2023-04-01', 'value': 10},
            {'timestamp': '2023-04-01', 'value': 20}
        ]
        self.mock_data_layer.write.assert_called_once_with(expected_data)

if __name__ == '__main__':
    unittest.main()
