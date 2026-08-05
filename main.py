from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import (setup_database, 
    get_products_from_db, 
    get_product_by_id_from_db, 
    create_product_in_db, 
    delete_product_from_db, 
    update_product_in_db, 
    search_products_by_title_from_db,
    get_products_stats_from_db,
    get_category_stats_from_db,
    get_top_expensive_products_from_db,
    get_top_cheap_products_from_db)

app = FastAPI()

setup_database()

products = [
    {
        "id": 1,
        "title": "Milk",
        "price": 80,
        "category": "Food"
    },
    {
        "id": 2,
        "title": "Keyboard",
        "price": 3000,
        "category": "Tech"
    }
]

class ProductCreate(BaseModel):
    title: str
    price: int
    category: str

def validate_product(product: ProductCreate):
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero")

    if product.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    if product.category.strip() == "":
        raise HTTPException(status_code=400, detail="Category is required")

def validate_limit(limit):
    if limit <=п 0:
        raise HTTPException(status_code=400, detail="limit must be greater than zero")
    if limit > 100:
        raise HTTPException(status_code=400, detail="limit cannot be greater than 100")    


def get_next_product_id():
    if len(products) == 0:
        return 1

    return max(product["id"] for product in products) + 1

categories = ["Food", "Tech"]

@app.get("/")
def read_root():
    return {"message": "Hello API"}


@app.get("/db/products")
def get_db_products(
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    limit: int | None = None,
    offset: int | None = None
):
    if category is not None:
        category = category.strip().capitalize()

        if category == "":
            category = None

    if min_price is not None and min_price < 0:
        raise HTTPException(status_code=400, detail="min_price cannot be negative")

    if max_price is not None and max_price < 0:
        raise HTTPException(status_code=400, detail="max_price cannot be negative")

    if max_price is not None and min_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")

    if sort_by is not None:
        sort_by = sort_by.strip().lower()

        if sort_by == "":
            sort_by = None
        elif sort_by not in ["price", "title", "category"]:
            raise HTTPException(status_code=400, detail="Invalid sort_by value")

    if sort_order is not None:
        sort_order = sort_order.strip().lower()

        if sort_order == "":
            sort_order = "asc"
        elif sort_order not in ["asc", "desc"]:
            raise HTTPException(status_code=400, detail="Invalid sort_order value")
    else:
        sort_order = "asc"

    if limit is not None and limit <= 0:
        raise HTTPException(status_code=400, detail="limit must be greater than zero")

    if offset is not None and offset < 0:
        raise HTTPException(status_code=400, detail="offset cannot be negative")    

    return get_products_from_db(
        category,
        min_price,
        max_price,
        sort_by,
        sort_order,
        limit,
        offset
    )


@app.get("/db/products/search/{search_text}")
def search_db_products(search_text: str):
    if search_text.strip() == "":
        raise HTTPException(status_code=400, detail="Search text is required")

    products = search_products_by_title_from_db(search_text)

    return products


@app.get("/db/products/stats")
def get_db_products_stats():
    return get_products_stats_from_db()


@app.get("/db/products/stats/categories")
def get_db_category_stats():
    return get_category_stats_from_db()


@app.get("/db/products/top")
def get_top_expensive_products(limit: int = 3):
    validate_limit(limit)

    return get_top_expensive_products_from_db(limit)


@app.get("/db/products/cheap")
def get_top_cheap_products(limit: int = 3):
    validate_limit(limit)

    return get_top_cheap_products_from_db(limit)


@app.get("/db/products/{product_id}")
def get_db_product(product_id: int):
    product = get_product_by_id_from_db(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@app.post("/db/products", status_code=201)
def create_db_product(product: ProductCreate):
    validate_product(product)

    created_product = create_product_in_db(
        product.title.strip().title(),
        product.price,
        product.category.strip().capitalize()
    )

    return created_product

@app.delete("/db/products/{product_id}")
def delete_db_product(product_id: int):
    is_deleted = delete_product_from_db(product_id)

    if not is_deleted:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted"}


@app.put("/db/products/{product_id}")
def update_db_product(product_id: int, product: ProductCreate):
    validate_product(product)

    updated_product = update_product_in_db(
       product_id,
        product.title.strip().title(),
        product.price,
        product.category.strip().capitalize()
    )

    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated_product


@app.get("/products")
def get_products(
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    search: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    limit: int | None = None,
    offset: int | None = None
):
    if min_price is not None and min_price < 0:
        raise HTTPException(status_code=400, detail="min_price cannot be negative")

    if max_price is not None and max_price < 0:
        raise HTTPException(status_code=400, detail="max_price cannot be negative")

    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")

    if search is not None:
        search = search.strip().lower()

        if search == "":
            search = None

    if sort_by is not None:
        sort_by = sort_by.strip().lower()

        if sort_by == "":
            sort_by = None

        elif sort_by != "price" and sort_by != "title" and sort_by != "category":
            raise HTTPException(status_code=400, detail="Invalid sort_by value")

    if sort_order is not None:
        sort_order = sort_order.strip().lower()

        if sort_order == "":
            sort_order = "asc"

        elif sort_order != "asc" and sort_order != "desc":
            raise HTTPException(status_code=400, detail="Invalid sort_order value")

    else:
        sort_order = "asc"

    if limit is not None and limit <= 0:
        raise HTTPException(status_code=400, detail="limit must be greater than zero")

    if offset is not None and offset < 0:
        raise HTTPException(status_code=400, detail="offset cannot be negative")    

    result = []

    for product in products:
        if category is not None and product["category"] != category.strip().capitalize():
            continue

        if min_price is not None and product["price"] < min_price:
            continue

        if max_price is not None and product["price"] > max_price:
            continue

        if search is not None and search not in product["title"].lower():
            continue

        result.append(product)

    if sort_by == "price":
        result.sort(key=lambda product: product["price"], reverse=sort_order == "desc")

    elif sort_by == "title":
        result.sort(key=lambda product: product["title"], reverse=sort_order == "desc")

    elif sort_by == "category":
        result.sort(key=lambda product: product["category"], reverse=sort_order == "desc")

    if offset is not None:
        result = result[offset:]

    if limit is not None:
        result = result[:limit]    

    return result


@app.get("/categories")
def get_categories():
    return categories


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    result = []

    for product in products:
        if product["category"] == category_name:
            result.append(product)

    return result


@app.get("/products/min-price/{min_price}")
def get_products_by_min_price(min_price: int):
    result = []

    for product in products:
        if product["price"] >= min_price:
            result.append(product)

    return result


@app.get("/products/max-price/{max_price}")
def get_products_by_max_price(max_price: int):
    result = []

    for product in products:
        if product["price"] <= max_price:
            result.append(product)

    return result


@app.get("/products/price-range/{min_price}/{max_price}")
def get_products_by_price_range(min_price: int, max_price: int):
    result = []

    for product in products:
        if product["price"] >= min_price and product["price"] <= max_price:
            result.append(product)

    return result


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    validate_product(product)

    new_product = {
        "id": get_next_product_id(),
        "title": product.title.strip().title(),
        "price": product.price,
        "category": product.category.strip().capitalize()
    }

    products.append(new_product)

    return new_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": "Product deleted"}

    raise HTTPException(status_code=404, detail="Product not found")


@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductCreate):
    validate_product(product)

    
    for existing_product in products:
        if existing_product["id"] == product_id:
            existing_product["title"] = product.title.strip().title()
            existing_product["price"] = product.price
            existing_product["category"] = product.category.strip().capitalize()

            return existing_product

    raise HTTPException(status_code=404, detail="Product not found")