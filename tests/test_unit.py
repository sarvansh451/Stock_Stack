import unittest
from unittest.mock import patch, MagicMock
from app import app, add_item
from flask import json

class UnitTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.mysql')
    def test_add_item_mocked(self, mock_mysql):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_mysql.connection = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        with app.test_request_context(json={'name': 'Mock Item', 'quantity': 3}):
            response, status_code = add_item()
            self.assertEqual(status_code, 201)
            self.assertEqual(response.json['message'], 'Item added successfully')

if __name__ == '__main__':
    unittest.main()
