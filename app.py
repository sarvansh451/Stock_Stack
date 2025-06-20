from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import db_config

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
app.config['MYSQL_USER'] = db_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = db_config.MYSQL_DB

mysql = MySQL(app)

# Get all items
@app.route('/api/items', methods=['GET'])
def get_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    cur.close()
    items = [{'id': row[0], 'name': row[1], 'quantity': row[2]} for row in rows]
    return jsonify(items)

# Add a new item
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing data'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO items (name, quantity) VALUES (%s, %s)", (data['name'], data['quantity']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item added successfully'}), 201

# Update item
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET name=%s, quantity=%s WHERE id=%s", (data['name'], data['quantity'], item_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item updated successfully'})

# Delete item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE id=%s", (item_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Item deleted successfully'})

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
