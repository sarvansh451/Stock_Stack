# 📘 API Documentation – StockStack

Base URL: `http://localhost:5000`

---

## 🔍 GET `/api/items`

Fetches all items from the inventory database.

- **Method:** `GET`
- **Request Body:** ❌ None
- **Success Response:**
```json
[
  { "id": 1, "name": "Pen", "quantity": 10 },
  { "id": 2, "name": "Notebook", "quantity": 5 }
]
```

---

## ➕ POST `/api/items`

Adds a new item to the inventory.

- **Method:** `POST`
- **Headers:**  
  `Content-Type: application/json`
- **Request Body Example:**
```json
{
  "name": "Marker",
  "quantity": 15
}
```
- **Success Response:**
```json
{
  "message": "Item added successfully"
}
```

---

## ✏️ PUT `/api/items/<id>`

Updates an existing item's name and quantity.

- **Method:** `PUT`
- **URL Param:**  
  `id`: The ID of the item to update
- **Headers:**  
  `Content-Type: application/json`
- **Request Body Example:**
```json
{
  "name": "Blue Marker",
  "quantity": 25
}
```
- **Success Response:**
```json
{
  "message": "Item updated successfully"
}
```

---

## ❌ DELETE `/api/items/<id>`

Deletes an item from the inventory.

- **Method:** `DELETE`
- **URL Param:**  
  `id`: The ID of the item to delete
- **Success Response:**
```json
{
  "message": "Item deleted successfully"
}
```

---

## 🛠️ Example `curl` Commands

### ➕ Add an item
```bash
curl -X POST http://localhost:5000/api/items ^
-H "Content-Type: application/json" ^
-d "{\"name\":\"Pen\", \"quantity\":10}"
```

### 📋 View all items
```bash
curl http://localhost:5000/api/items
```

### ✏️ Update item with ID 1
```bash
curl -X PUT http://localhost:5000/api/items/1 ^
-H "Content-Type: application/json" ^
-d "{\"name\":\"Updated Pen\", \"quantity\":12}"
```

### ❌ Delete item with ID 1
```bash
curl -X DELETE http://localhost:5000/api/items/1
```
