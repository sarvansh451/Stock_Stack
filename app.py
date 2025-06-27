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
    """
    Get all items
    ---
    responses:
      200:
        description: List of items
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              quantity:
                type: integer
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    cur.close()
    items = [{'id': row[0], 'name': row[1], 'quantity': row[2]} for row in rows]
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def add_item():
    """
    Add a new item
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - quantity
          properties:
            name:
              type: string
            quantity:
              type: integer
    responses:
      201:
        description: Item added successfully
        schema:
          type: object
          properties:
            message:
              type: string
            id:
              type: integer
    """
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing data'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO items (name, quantity) VALUES (%s, %s)", (data['name'], data['quantity']))
    item_id = cur.lastrowid  # ✅ Get inserted ID
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item added successfully', 'id': item_id}), 201  # ✅ Return ID

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    Update an item
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            quantity:
              type: integer
    responses:
      200:
        description: Item updated successfully
    """
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET name=%s, quantity=%s WHERE id=%s", (data['name'], data['quantity'], item_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item updated successfully'})

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Delete an item
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Item deleted successfully
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE id=%s", (item_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item deleted successfully'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
