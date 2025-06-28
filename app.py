from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flasgger import Swagger
import db_config

app = Flask(__name__)

# Swagger Template & Config
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Inventory API",
        "description": "API for managing items in inventory",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'openapi',
            "route": '/apidocs/openapi.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# MySQL Configuration
app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
app.config['MYSQL_USER'] = db_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = db_config.MYSQL_DB

mysql = MySQL(app)

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    cur.close()
    items = [{'id': row[0], 'name': row[1], 'quantity': row[2]} for row in rows]
    return jsonify(items), 200

@app.route('/api/items', methods=['POST'])
def add_item():
    """Add a new item"""
    raw_data = request.get_json()
    if not raw_data:
        return jsonify({'error': 'Missing JSON body'}), 400

    # Sanitize & filter only allowed fields
    data = {k: v for k, v in raw_data.items() if k in ['name', 'quantity']}
    name = data.get('name', '').strip()
    quantity = data.get('quantity')

    if not name or not isinstance(quantity, int) or quantity < 0:
        return jsonify({'error': 'Invalid input'}), 400

    cur = mysql.connection.cursor()

    # Check for duplicate names
    cur.execute("SELECT id FROM items WHERE name = %s", (name,))
    if cur.fetchone():
        cur.close()
        return jsonify({'error': 'Item with same name exists'}), 400

    cur.execute("INSERT INTO items (name, quantity) VALUES (%s, %s)", (name, quantity))
    item_id = cur.lastrowid
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item added successfully', 'id': item_id}), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an item (supports partial updates)"""
    raw_data = request.get_json()
    if not raw_data:
        return jsonify({'error': 'Missing JSON body'}), 400

    data = {k: v for k, v in raw_data.items() if k in ['name', 'quantity']}
    name = data.get('name', None)
    quantity = data.get('quantity', None)

    if name is not None and not name.strip():
        return jsonify({'error': 'Name cannot be empty'}), 400
    if quantity is not None and (not isinstance(quantity, int) or quantity < 0):
        return jsonify({'error': 'Invalid quantity'}), 400
    if name is None and quantity is None:
        return jsonify({'error': 'Nothing to update'}), 400

    cur = mysql.connection.cursor()
    if name is not None and quantity is not None:
        cur.execute("UPDATE items SET name=%s, quantity=%s WHERE id=%s", (name.strip(), quantity, item_id))
    elif name is not None:
        cur.execute("UPDATE items SET name=%s WHERE id=%s", (name.strip(), item_id))
    elif quantity is not None:
        cur.execute("UPDATE items SET quantity=%s WHERE id=%s", (quantity, item_id))

    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item updated successfully'}), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE id=%s", (item_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item deleted successfully'}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

