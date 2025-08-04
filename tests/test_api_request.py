import unittest
from api_request.api_request import connect_to_db, fetch_data, mock_fetch_data

class TestAPIRequestFunctions(unittest.TestCase):

    def test_mock_fetch_data(self):
        """Test mock_fetch_data returns expected structure."""
        data = mock_fetch_data()
        self.assertIn('location', data)
        self.assertIsInstance(data['location'], dict)
        self.assertIn('name', data['location'])

    def test_db_connection(self):
        """Test database connection opens and closes cleanly."""
        try:
            conn = connect_to_db()
            self.assertIsNotNone(conn)
            conn.close()
        except Exception as e:
            self.fail(f"DB connection raised an exception: {e}")

    def test_fetch_data_structure(self):
        """Test real fetch_data call (optional, real API key required)."""
        try:
            data = fetch_data()
            self.assertIn('location', data)
            self.assertIn('name', data['location'])
        except Exception as e:
            self.fail(f"Real fetch_data failed: {e}")

if __name__ == '__main__':
    unittest.main()
