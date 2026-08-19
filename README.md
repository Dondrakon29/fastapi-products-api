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
- Paginate products with limit and offset

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

### Get product statistics

```http
GET /db/products/stats
```
Example:

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

### Sort products

```http
GET /db/products?sort_by=price&sort_order=desc
```

### Get product count by category

`GET /db/products/categories/{category}/count`

Returns the number of products in a specific category.

Example:

`GET /db/products/categories/Food/count`

Response:

```json
{
  "category": "Food",
  "products_count": 1
}
```

### Get total price by category

`GET /db/products/categories/{category}/total-price`

Returns the total price of products in a specific category.

Example:

`GET /db/products/categories/Food/total-price`

Response:

```json
{
  "category": "Food",
  "total_price": 120
}
```

### Get average price by category

`GET /db/products/categories/{category}/average-price`

Returns the average price of products in a specific category.

Example:

`GET /db/products/categories/Food/average-price`

Response:

```json
{
  "category": "Food",
  "average_price": 120
}
```

### Pagination

```http
GET /db/products?limit=2&offset=0
```
limit controls how many products are returned.

offset controls how many products are skipped.

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