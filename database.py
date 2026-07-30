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

def row_to_product(row):
    return {
        "id": row[0],
        "title": row[1],
        "price": row[2],
        "category": row[3]
    }

def get_products_from_db(category=None, min_price=None, max_price=None, sort_by=None,
    sort_order="asc", limit=None, offset=None):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, title, price, category
        FROM products
        WHERE 1 = 1
    """

    params = []

    if category is not None:
        query += " AND category = ?"
        params.append(category)

    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)

    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    if sort_by is not None:
        query += " ORDER BY " + sort_by + " " + sort_order

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    if offset is not None:
        if limit is None:
            query += " LIMIT -1"

        query += " OFFSET ?"
        params.append(offset)

    cursor.execute(query, params)
    
    rows = cursor.fetchall()

    products = []

    for row in rows:
        product = row_to_product(row)

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
        product = row_to_product(row)
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

    product = row_to_product(row)
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


def get_products_stats_from_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*), SUM(price), AVG(price), MIN(price), MAX(price)
        FROM products
    """)

    row = cursor.fetchone()

    stats = {
        "products_count": row[0],
        "total_price": row[1],
        "average_price": row[2],
        "min_price": row[3],
        "max_price": row[4]
    }

    connection.close()

    return stats


def get_category_stats_from_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, COUNT(*), SUM(price), AVG(price), MIN(price), MAX(price)
        FROM products
        GROUP BY category
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        category_stats = {
            "category": row[0],
            "products_count": row[1],
            "total_price": row[2],
            "average_price": row[3],
            "min_price": row[4],
            "max_price": row[5]
        }

        result.append(category_stats)

    connection.close()

    return result


def get_top_expensive_products_from_db(limit):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, price, category
        FROM products
        ORDER BY price DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    products = []

    for row in rows:
        product = row_to_product(row)
        products.append(product)

    connection.close()

    return products