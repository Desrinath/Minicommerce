from flask import Flask, render_template, redirect, url_for, request, session
from models.product import Product
from models.user import User
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_products():
    conn = sqlite3.connect('data/products.db')
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, image FROM products")
    rows = cur.fetchall()
    conn.close()
    return [Product(*row) for row in rows]

@app.route('/')
def home():
    products = load_products()
    return render_template('home.html', products=products)

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    session.setdefault('cart', []).append(product_id)
    session.modified = True
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    products = load_products()
    cart_items = [p for p in products if p.id in session.get('cart', [])]
    total = sum(p.price for p in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [p for p in session['cart'] if p != product_id]
        session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'])
        user.save_to_db()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if User.authenticate(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/search')
def search():
    keyword = request.args.get('q', '').lower()
    products = load_products()
    filtered = [p for p in products if keyword in p.name.lower()]
    return render_template('home.html', products=filtered)

if __name__ == '__main__':
    app.run(debug=True)

