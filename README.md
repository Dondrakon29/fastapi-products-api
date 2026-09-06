# FastAPI Products API

A learning REST API for managing products.

This project is built with **FastAPI** and **SQLite**.

It demonstrates basic backend logic: CRUD operations, data validation, filtering, searching, sorting, pagination, statistics, and persistent data storage.

## Features

- Get all products
- Get product by ID
- Create a new product
- Update an existing product
- Delete a product
- Store products in SQLite database
- Filter products by category
- Filter products by minimum price
- Filter products by maximum price
- Search products by title
- Sort products by price, title, or category
- Paginate products with limit and offset
- Get product statistics
- Get category statistics
- Get product count by category
- Get total price by category
- Get average price by category
- Get category summary
- Get price summary
- Get unique product categories
- Validate input data
- Return proper HTTP errors for invalid requests or missing products
- Health check endpoint

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

## System endpoints

### API info

```http
GET /
```

Returns general information about the API.

Example response:

```json
{
  "message": "FastAPI Products API",
  "version": "1.0",
  "docs": "/docs",
  "main_endpoint": "/db/products"
}
```

### Health check

```http
GET /health
```

Returns API health status.

Example response:

```json
{
  "status": "ok"
}
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

## Filtering, searching, sorting and pagination

### Filter products by category

```http
GET /db/products?category=Tech
```

### Filter products by minimum price

```http
GET /db/products?min_price=1000
```

### Filter products by maximum price

```http
GET /db/products?max_price=5000
```

### Filter products by category and minimum price

```http
GET /db/products?category=Tech&min_price=1000
```

### Search products by title

```http
GET /db/products?search=key
```

Example response:

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

### Sort products

```http
GET /db/products?sort_by=price&sort_order=desc
```

Available `sort_by` values:

```text
price
title
category
```

Available `sort_order` values:

```text
asc
desc
```

### Pagination

```http
GET /db/products?limit=2&offset=0
```

`limit` controls how many products are returned.

`offset` controls how many products are skipped.

### Combined example

```http
GET /db/products?category=Tech&search=key&sort_by=price&sort_order=desc&limit=2&offset=0
```

## Statistics endpoints

### Get product statistics

```http
GET /db/products/stats
```

Example response:

```json
{
  "products_count": 3,
  "total_price": 15120,
  "average_price": 5040,
  "min_price": 120,
  "max_price": 12000
}
```

### Get category statistics

```http
GET /db/products/stats/categories
```

Example response:

```json
[
  {
    "category": "Food",
    "products_count": 1,
    "total_price": 120,
    "average_price": 120,
    "min_price": 120,
    "max_price": 120
  },
  {
    "category": "Tech",
    "products_count": 2,
    "total_price": 15000,
    "average_price": 7500,
    "min_price": 3000,
    "max_price": 12000
  }
]
```

### Get price summary

```http
GET /db/products/price-summary
```

Returns product count, total price, average price, minimum price and maximum price for all products.

Example response:

```json
{
  "products_count": 3,
  "total_price": 15120,
  "average_price": 5040,
  "min_price": 120,
  "max_price": 12000
}
```

## Category endpoints

### Get all categories

```http
GET /db/products/categories
```

Returns a list of unique product categories.

Example response:

```json
[
  "Food",
  "Tech"
]
```

### Get product count by category

```http
GET /db/products/categories/{category}/count
```

Example:

```http
GET /db/products/categories/Food/count
```

Example response:

```json
{
  "category": "Food",
  "products_count": 1
}
```

### Get total price by category

```http
GET /db/products/categories/{category}/total-price
```

Example:

```http
GET /db/products/categories/Food/total-price
```

Example response:

```json
{
  "category": "Food",
  "total_price": 120
}
```

### Get average price by category

```http
GET /db/products/categories/{category}/average-price
```

Example:

```http
GET /db/products/categories/Food/average-price
```

Example response:

```json
{
  "category": "Food",
  "average_price": 120
}
```

### Get category summary

```http
GET /db/products/categories/{category}/summary
```

Returns product count, total price, average price, minimum price and maximum price for a specific category.

Example:

```http
GET /db/products/categories/Tech/summary
```

Example response:

```json
{
  "category": "Tech",
  "products_count": 2,
  "total_price": 15000,
  "average_price": 7500,
  "min_price": 3000,
  "max_price": 12000
}
```

## Top products endpoints

### Get top expensive products

```http
GET /db/products/top?limit=3
```

Example response:

```json
[
  {
    "id": 4,
    "title": "Monitor",
    "price": 12000,
    "category": "Tech"
  },
  {
    "id": 2,
    "title": "Keyboard",
    "price": 3000,
    "category": "Tech"
  },
  {
    "id": 1,
    "title": "Milk Big",
    "price": 120,
    "category": "Food"
  }
]
```

### Get top cheap products

```http
GET /db/products/cheap?limit=3
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Milk Big",
    "price": 120,
    "category": "Food"
  },
  {
    "id": 2,
    "title": "Keyboard",
    "price": 3000,
    "category": "Tech"
  },
  {
    "id": 4,
    "title": "Monitor",
    "price": 12000,
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

If `max_price` is negative:

```json
{
  "detail": "max_price cannot be negative"
}
```

If `min_price` is greater than `max_price`:

```json
{
  "detail": "min_price cannot be greater than max_price"
}
```

If `limit` is less than or equal to zero:

```json
{
  "detail": "limit must be greater than zero"
}
```

If `limit` is greater than 100:

```json
{
  "detail": "limit cannot be greater than 100"
}
```

If `offset` is negative:

```json
{
  "detail": "offset cannot be negative"
}
```

If `sort_by` value is invalid:

```json
{
  "detail": "Invalid sort_by value"
}
```

If `sort_order` value is invalid:

```json
{
  "detail": "Invalid sort_order value"
}
```

## Project status

Learning backend project.

The project includes SQLite-based endpoints with persistent product storage.

It demonstrates important backend concepts such as request handling, validation, database queries, CRUD operations, filtering, searching, sorting, pagination, statistics, and HTTP error responses.