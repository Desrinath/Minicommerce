import sqlite3

conn = sqlite3.connect('data/products.db')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, image TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

products = [
    ("T-Shirt", 499, "tshirt.png"),
    ("Shoes", 999, "shoes.png"),
    ("Cap", 299, "cap.png")
]

cur.executemany("INSERT INTO products (name, price, image) VALUES (?, ?, ?)", products)
conn.commit()
conn.close()
