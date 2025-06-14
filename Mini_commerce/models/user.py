import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        conn = sqlite3.connect('data/products.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, self.password))
        conn.commit()
        conn.close()

    @staticmethod
    def authenticate(username, password):
        conn = sqlite3.connect('data/products.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()
        return user is not None
