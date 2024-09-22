import unittest
from unittest.mock import Mock, patch
from src.database.TestDBCreate import TestDBCreate
import psycopg2
import os

class TestTestDBCreate(unittest.TestCase):
    def setUp(self):
        # Set up mock connection for unit tests
        self.mock_conn = Mock()
        self.mock_cursor = Mock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.db_creator_mock = TestDBCreate(connection=self.mock_conn)

        # Set up real connection for integration tests
        db_name = os.getenv('DB_NAME', 'testdb')
        db_user = os.getenv('DB_USER', 'testuser')
        db_password = os.getenv('DB_PASSWORD', 'testpass')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        
        self.real_conn_string = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"
        self.db_creator_real = TestDBCreate(connection_string=self.real_conn_string)

    def test_create_db_with_mock(self):
        # Call the create_test_db method on the mock instance
        result = self.db_creator_mock.create_test_db()

        # Assert that the method returned True
        self.assertTrue(result)

        # Check that necessary methods were called
        self.mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS dataSeries (...)")
        self.mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS dataPoints (...)")
        
        # Check that test data points were added
        self.mock_cursor.execute.assert_any_call("INSERT INTO dataPoints (...) VALUES (...)")

        # Verify the number of times execute was called
        self.assertGreaterEqual(self.mock_cursor.execute.call_count, 3)

    @unittest.skipIf(not os.environ.get('RUN_INTEGRATION_TESTS'), "Integration test")
    def test_create_db_integration(self):
        # This test will use a real database connection
        result = self.db_creator_real.create_test_db()
        self.assertTrue(result)

        # Verify the database structure and content
        with psycopg2.connect(self.real_conn_string) as conn:
            with conn.cursor() as cur:
                # Check if tables exist
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'dataseries')")
                self.assertTrue(cur.fetchone()[0])
                
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'datapoints')")
                self.assertTrue(cur.fetchone()[0])

                # Check if test data points were added
                cur.execute("SELECT COUNT(*) FROM datapoints")
                self.assertGreater(cur.fetchone()[0], 0)

if __name__ == '__main__':
    unittest.main()