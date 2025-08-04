import unittest
from unittest.mock import MagicMock, patch
from api_request.insert_records import create_table, insert_records, main

class TestETLFunctions(unittest.TestCase):

    def setUp(self):
        # Setup mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor

        self.valid_data = {
            'location': {
                'name': 'New York',
                'region': 'New York',
                'country': 'USA',
                'localtime': '2025-07-21 23:37',
                'utc_offset': '-4.0'
            }
        }

        self.invalid_data = {
            'location': {
                'name': 'New York',
                'country': 'USA',
                'localtime': '2025-07-21 23:37'
                # missing region, utc_offset
            }
        }

    def test_create_table_runs_sql(self):
        create_table(self.mock_conn)
        self.mock_cursor.execute.assert_called_once()
        self.mock_conn.commit.assert_called_once()

    def test_insert_records_with_valid_data(self):
        insert_records(self.mock_conn, self.valid_data)
        self.mock_cursor.execute.assert_called_once()
        self.mock_conn.commit.assert_called_once()

    def test_insert_records_with_missing_keys_raises(self):
        with self.assertRaises(ValueError) as context:
            insert_records(self.mock_conn, self.invalid_data)
        self.assertIn("Missing required keys", str(context.exception))

    @patch('api_request.insert_records.connect_to_db')
    @patch('api_request.insert_records.fetch_data')
    @patch('api_request.insert_records.mock_fetch_data')
    def test_main_runs_with_mock_data(self, mock_mock_fetch, mock_fetch, mock_connect):
        mock_connect.return_value = self.mock_conn
        mock_mock_fetch.return_value = self.valid_data

        main(use_mock=True)

        # Check table creation occurred
        calls = [call[0][0] for call in self.mock_cursor.execute.call_args_list]
        matched = any("CREATE TABLE IF NOT EXISTS weather_data" in c for c in calls)
        self.assertTrue(matched, "CREATE TABLE was not executed")

        # Ensure connection closed
        self.assertTrue(self.mock_conn.close.called) 

if __name__ == "__main__":
    unittest.main()
