import sqlite3


def get_connection():
    return sqlite3.connect("products.db")


def setup_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM products")
    products_count = cursor.fetchone()[0]

    if products_count == 0:
        cursor.executemany("""
            INSERT INTO products (title, price, category)
            VALUES (?, ?, ?)
        """, [
            ("Milk", 80, "Food"),
            ("Keyboard", 3000, "Tech"),
            ("Bread", 50, "Food")
        ])

    connection.commit()
    connection.close()

def get_products_from_db(category=None, min_price=None, max_price=None):
    connection = get_connection()
    cursor = connection.cursor()

    if category is None and min_price is None and max_price is None:
        cursor.execute("""
            SELECT id, title, price, category
            FROM products
        """)

    elif category is not None and min_price is None and max_price is None:
        cursor.execute("""
            SELECT id, title, price, category
            FROM products
            WHERE category = ?
        """, (category,))

    elif category is None and min_price is not None and max_price is None:
        cursor.execute("""
            SELECT id, title, price, category
            FROM products
            WHERE price >= ?
        """, (min_price,))

    elif category is None and min_price is None and max_price is not None:
        cursor.execute("""
            SELECT id, title, price, category
            FROM products
            WHERE price <= ?
        """, (max_price,))

    elif category is not None and min_price is None and max_price is not None:
        cursor.execute("""
            SELECT id, title, price, category
            FROM products
            WHERE category = ? AND price <= ?
        """, (category, max_price))

    elif category is None and min_price is not None and max_price is not None:
        cursor.execute("""
            SELECT id, title, price, category
            FROM products
            WHERE price >= ? AND price <= ?
        """, (min_price, max_price))                 

    elif category is not None and min_price is not None and max_price is None:
        cursor.execute("""
            SELECT id, title, price, category
            FROM products
            WHERE category = ? AND price >= ?
        """, (category, min_price))

    elif category is not None and min_price is not None and max_price is not None:
        cursor.execute("""
            SELECT id, title, price, category
            FROM products
            WHERE category = ? AND price >= ? AND price <= ?
        """, (category, min_price, max_price)) 
    
    rows = cursor.fetchall()

    products = []

    for row in rows:
        product = {
            "id": row[0],
            "title": row[1],
            "price": row[2],
            "category": row[3]
        }

        products.append(product)

    connection.close()

    return products

def search_products_by_title_from_db(search_text):
    connection = get_connection()
    cursor = connection.cursor()

    search_pattern = "%" + search_text.strip().lower() + "%"

    cursor.execute("""
        SELECT id, title, price, category
        FROM products
        WHERE lower(title) LIKE ?
    """, (search_pattern,))

    rows = cursor.fetchall()

    products = []

    for row in rows:
        product = {
            "id": row[0],
            "title": row[1],
            "price": row[2],
            "category": row[3]
        }

        products.append(product)

    connection.close()

    return products

def get_product_by_id_from_db(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, price, category
        FROM products
        WHERE id = ?
    """, (product_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    product = {
        "id": row[0],
        "title": row[1],
        "price": row[2],
        "category": row[3]
    }

    return product


def create_product_in_db(title, price, category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products (title, price, category)
        VALUES (?, ?, ?)
    """, (title, price, category))

    connection.commit()

    product_id = cursor.lastrowid

    connection.close()

    product = {
        "id": product_id,
        "title": title,
        "price": price,
        "category": category
    }

    return product

def delete_product_from_db(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))

    connection.commit()

    deleted_count = cursor.rowcount

    connection.close()

    if deleted_count == 0:
        return False

    return True


def update_product_in_db(product_id, title, price, category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE products
        SET title = ?, price = ?, category = ?
        WHERE id = ?
    """, (title, price, category, product_id))

    connection.commit()

    updated_count = cursor.rowcount

    connection.close()

    if updated_count == 0:
        return None

    product = {
        "id": product_id,
        "title": title,
        "price": price,
        "category": category
    }

    return product