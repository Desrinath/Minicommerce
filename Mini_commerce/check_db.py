import sqlite3

conn = sqlite3.connect('data/products.db')
cur = conn.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("✅ Tables:", tables)

# Show all products
cur.execute("SELECT * FROM products")
rows = cur.fetchall()
print("✅ Products:")
for row in rows:
    print(row)

conn.close()
