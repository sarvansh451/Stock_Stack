import unittest
from app import app
from flask import json

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_items(self):
        response = self.app.get('/api/items')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_add_item(self):
        data = {'name': 'Test Item', 'quantity': 10}
        response = self.app.post('/api/items',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.json)

    def test_update_item(self):
        data = {'name': 'Updated Item', 'quantity': 15}
        response = self.app.put('/api/items/1',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        response = self.app.delete('/api/items/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
