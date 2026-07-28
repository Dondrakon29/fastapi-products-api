# FastAPI Products API

A learning REST API for managing products.

This project is built with **FastAPI** and **SQLite**.  
It demonstrates basic backend logic: CRUD operations, data validation, filtering, searching, and persistent data storage.

## Features

- Get all products
- Get product by ID
- Create a new product
- Update an existing product
- Delete a product
- Store products in SQLite database
- Filter products by category
- Filter products by minimum price
- Search products by title
- Validate input data
- Return proper HTTP errors for invalid requests or missing products

## Technologies

- Python
- FastAPI
- Pydantic
- SQLite
- Uvicorn

## How to run

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the server:

```bash
python -m uvicorn main:app --reload
```

Open API documentation:

```text
http://127.0.0.1:8000/docs
```

## SQLite API endpoints

### Get all products

```http
GET /db/products
```

### Get product by ID

```http
GET /db/products/{product_id}
```

Example:

```http
GET /db/products/1
```

### Create product

```http
POST /db/products
```

Example body:

```json
{
  "title": "Mouse",
  "price": 1500,
  "category": "Tech"
}
```

### Update product

```http
PUT /db/products/{product_id}
```

Example:

```http
PUT /db/products/1
```

Example body:

```json
{
  "title": "Gaming Mouse",
  "price": 2500,
  "category": "Tech"
}
```

### Delete product

```http
DELETE /db/products/{product_id}
```

Example:

```http
DELETE /db/products/1
```

### Filter products by category

```http
GET /db/products?category=Tech
```

### Filter products by minimum price

```http
GET /db/products?min_price=1000
```

### Filter products by category and minimum price

```http
GET /db/products?category=Tech&min_price=1000
```

### Search products by title

```http
GET /db/products/search/key
```

This endpoint searches products by part of the title.

For example:

```http
GET /db/products/search/key
```

can find:

```json
[
  {
    "id": 2,
    "title": "Keyboard",
    "price": 3000,
    "category": "Tech"
  }
]
```

## Validation examples

If product price is less than or equal to zero:

```json
{
  "detail": "Price must be greater than zero"
}
```

If product title is empty:

```json
{
  "detail": "Title is required"
}
```

If product category is empty:

```json
{
  "detail": "Category is required"
}
```

If product is not found:

```json
{
  "detail": "Product not found"
}
```

If `min_price` is negative:

```json
{
  "detail": "min_price cannot be negative"
}
```

## Project status

Learning project.

The project includes SQLite-based endpoints with persistent product storage.  
It also demonstrates important backend concepts such as request handling, validation, database queries, and HTTP error responses.