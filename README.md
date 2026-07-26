# FastAPI Products API

A learning REST API for managing products.

This project is built with FastAPI and demonstrates basic backend logic: CRUD operations, data validation, filtering, searching, sorting, and pagination.

## Features

- Get all products
- Get a product by id
- Create a new product
- Update a product
- Delete a product
- Filter products by category
- Filter products by minimum and maximum price
- Search products by title
- Sort products by price, title, and category
- Limit results with `limit` and `offset`
- Return proper 400 and 404 errors

## Technologies

- Python
- FastAPI
- Pydantic
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

## Example requests

Get all products:

```text
GET /products
```

Get a product by id:

```text
GET /products/1
```

Create a product:

```text
POST /products
```

Request body:

```json
{
  "title": "Mouse",
  "price": 1500,
  "category": "Tech"
}
```

Filter, sort, and limit products:

```text
GET /products?category=Tech&sort_by=price&sort_order=desc&limit=2&offset=0
```

## Project status

Learning project.

Data is stored in memory and resets after server restart.