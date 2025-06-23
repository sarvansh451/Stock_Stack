import unittest
from app import app, mysql
from flask import json

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True

        # ✅ Use Flask application context
        with self.app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM items")
            mysql.connection.commit()
            cur.close()

    def test_crud_flow(self):
        # ✅ Wrap inside context because we'll hit DB
        with self.app.app_context():
            # 1. Create item (POST)
            res = self.client.post('/api/items', json={
                'name': 'Integration Pen',
                'quantity': 3
            })
            self.assertEqual(res.status_code, 201)

            # 2. Read items (GET)
            res = self.client.get('/api/items')
            self.assertEqual(res.status_code, 200)
            items = res.json
            self.assertGreaterEqual(len(items), 1)

            item_id = items[0]['id']

            # 3. Update item (PUT)
            res = self.client.put(f'/api/items/{item_id}', json={
                'name': 'Updated Pen',
                'quantity': 10
            })
            self.assertEqual(res.status_code, 200)

            # 4. Delete item (DELETE)
            res = self.client.delete(f'/api/items/{item_id}')
            self.assertEqual(res.status_code, 200)

            # 5. Confirm deletion
            res = self.client.get('/api/items')
            self.assertEqual(len(res.json), 0)

if __name__ == '__main__':
    unittest.main()
