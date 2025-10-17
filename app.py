from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from datetime import datetime
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    date TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT SUM(quantity) FROM products')
    total_items = c.fetchone()[0] or 0
    c.execute('SELECT COUNT(*) FROM products WHERE quantity < 10')
    low_stock_count = c.fetchone()[0] or 0
    conn.close()
    return render_template('index.html', total_items=total_items, low_stock_count=low_stock_count)

@app.route('/api/all-items')
def all_items():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    items = c.fetchall()
    conn.close()
    return jsonify([{'id': item[0], 'name': item[1], 'category': item[2], 'quantity': item[3], 'price': item[4], 'date': item[5]} for item in items])

@app.route('/api/recent-products')
def recent_products():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products ORDER BY id DESC LIMIT 6')
    items = c.fetchall()
    conn.close()
    return jsonify([{'id': item[0], 'name': item[1], 'category': item[2], 'quantity': item[3], 'price': item[4], 'date': item[5]} for item in items])

@app.route('/api/low-stock')
def low_stock():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE quantity < 10 ORDER BY quantity ASC LIMIT 6')
    items = c.fetchall()
    conn.close()
    return jsonify([{'id': item[0], 'name': item[1], 'category': item[2], 'quantity': item[3], 'price': item[4], 'date': item[5]} for item in items])

@app.route('/inventory')
def inventory():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()

    # Fetch all items
    c.execute('SELECT * FROM products')
    items = c.fetchall()

    # Total number of items
    c.execute('SELECT SUM(quantity) FROM products')
    total_items = c.fetchone()[0] or 0

    # Low stock items (quantity < 10)
    c.execute('SELECT COUNT(*) FROM products WHERE quantity < 10')
    low_stock_count = c.fetchone()[0] or 0

    # Fetch distinct categories for the carousel
    c.execute('SELECT DISTINCT category FROM products')
    categories = [row[0] for row in c.fetchall()]

    conn.close()
    return render_template('inventory.html', items=items, total_items=total_items, low_stock_count=low_stock_count, categories=categories)

@app.route('/edit_product/<int:item_id>')
def edit_product(item_id):
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id = ?', (item_id,))
    item = c.fetchone()
    conn.close()
    return render_template('edit_product.html', item=item)

@app.route('/update_product/<int:item_id>', methods=['POST'])
def update_product(item_id):
    name = request.form['item_name']
    category = request.form['category']
    quantity = request.form['quantity']
    price = request.form['price']
    date = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('UPDATE products SET name = ?, category = ?, quantity = ?, price = ?, date = ? WHERE id = ?',
              (name, category, quantity, price, date, item_id))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory'))


@app.route('/api/category/<category>')
def items_by_category(category):
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE category = ?', (category,))
    items = c.fetchall()
    conn.close()
    return jsonify([{'id': item[0], 'name': item[1], 'category': item[2], 'quantity': item[3], 'price': item[4], 'date': item[5]} for item in items])

@app.route('/delete_product/<int:item_id>', methods=['POST'])
def delete_product(item_id):
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory'))

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['item_name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        date = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect('database/inventory.db')
        c = conn.cursor()
        c.execute('INSERT INTO products (name, category, quantity, price, date) VALUES (?, ?, ?, ?, ?)',
                  (name, category, quantity, price, date))
        conn.commit()
        conn.close()
        return redirect(url_for('inventory'))
    return render_template('add_product.html')

@app.route('/api/item/<item_name>')
def get_item(item_name):
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE name = ?', (item_name,))
    item = c.fetchone()
    conn.close()
    if item:
        return jsonify({'id': item[0], 'name': item[1], 'category': item[2], 'quantity': item[3], 'price': item[4]})
    return jsonify({'error': 'Item not found'}), 404

@app.route('/billing')
def billing():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT id, name, category, price FROM products WHERE quantity > 0')
    items = [{'id': item[0], 'name': item[1], 'category': item[2], 'price': item[3]} for item in c.fetchall()]
    conn.close()
    return render_template('billing.html', items=items)

@app.route('/checkout', methods=['POST'])
def checkout():
    items = request.json
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()

    try:
        for item in items:
            date = datetime.now().strftime('%Y-%m-%d')
            c.execute('SELECT quantity FROM products WHERE id = ?', (item['id'],))
            current_quantity = c.fetchone()[0]

            if current_quantity < item['quantity']:
                return jsonify({'message': f'Insufficient stock for {item["name"]}'}), 400

            c.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (item['quantity'], item['id']))

            c.execute('INSERT INTO sales (name, category, quantity, price, date) VALUES (?, ?, ?, ?, ?)',
                      (item['name'], item['category'], item['quantity'], item['price'] * item['quantity'], date))

        conn.commit()
        return jsonify({'message': 'Checkout successful'})

    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Checkout failed', 'error': str(e)}), 500

    finally:
        conn.close()


@app.route('/report')
def report():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()

    c.execute('SELECT DISTINCT category FROM sales')
    categories = [row[0] for row in c.fetchall()]

    c.execute('SELECT * FROM sales')
    sales_report = c.fetchall()

    conn.close()
    return render_template('report.html', categories=categories, sales_report=sales_report)

@app.route('/api/sales-report')
def get_sales_report():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT id, name, category, quantity, price, date FROM sales')
    sales = c.fetchall()
    conn.close()
    return jsonify([
        {'id': sale[0], 'name': sale[1], 'category': sale[2], 'quantity_sold': sale[3], 'total_price': sale[4], 'date': sale[5]}
        for sale in sales
    ])

@app.route('/api/sales-categories')
def get_sales_categories():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT category FROM sales')
    categories = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify(categories)

@app.route('/api/sales-report/<category>')
def get_sales_by_category(category):
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT id, name, category, quantity, price, date FROM sales WHERE category = ?', (category,))
    sales = c.fetchall()
    conn.close()
    return jsonify([
        {'id': sale[0], 'name': sale[1], 'category': sale[2], 'quantity_sold': sale[3], 'total_price': sale[4], 'date': sale[5]}
        for sale in sales
    ])

@app.route('/download_report')
def download_report():
    conn = sqlite3.connect('database/inventory.db')
    c = conn.cursor()
    c.execute('SELECT id, name, category, quantity, price, date FROM sales')
    sales = c.fetchall()
    conn.close()

    report_path = "D:/Karuna/Inventory Management System/Report downloads/sales_report.pdf"

    doc = SimpleDocTemplate(report_path, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph("<b>Sales Report</b>", styles['Title'])
    elements.append(title)

    data = [["Sale ID", "Product Name", "Category", "Quantity", "Total Price (₹)", "Date"]] + sales
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.burlywood),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    doc.build(elements)

    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)