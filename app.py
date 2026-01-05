from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
DB_NAME = 'finance.db'
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', False)

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL
                    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        type TEXT NOT NULL,  -- 'income' or 'expense'
                        amount REAL NOT NULL,
                        category_id INTEGER,
                        date TEXT NOT NULL,
                        description TEXT,
                        FOREIGN KEY (category_id) REFERENCES categories (id)
                    )''')
    # Insert default categories
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Alimentação')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Transporte')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Salário')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Outros')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Aluguel')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Cartão')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Financiamento')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Impostos')")
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Moradia')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def dashboard():
    month = request.args.get('month')
    conn = get_db()
    if month:
        # Filtrar por mês
        income = conn.execute("SELECT SUM(amount) as total FROM transactions WHERE type='income' AND strftime('%Y-%m', date) = ?", (month,)).fetchone()['total'] or 0
        expense = conn.execute("SELECT SUM(amount) as total FROM transactions WHERE type='expense' AND strftime('%Y-%m', date) = ?", (month,)).fetchone()['total'] or 0
        expenses_by_cat = conn.execute('''
            SELECT c.name, SUM(t.amount) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.type='expense' AND strftime('%Y-%m', t.date) = ?
            GROUP BY c.name
        ''', (month,)).fetchall()
    else:
        income = conn.execute("SELECT SUM(amount) as total FROM transactions WHERE type='income'").fetchone()['total'] or 0
        expense = conn.execute("SELECT SUM(amount) as total FROM transactions WHERE type='expense'").fetchone()['total'] or 0
        expenses_by_cat = conn.execute('''
            SELECT c.name, SUM(t.amount) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.type='expense'
            GROUP BY c.name
        ''').fetchall()
    
    # Últimas 10 transações
    latest_transactions = conn.execute('''
        SELECT t.id, t.type, t.amount, c.name as category, t.date, t.description
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        ORDER BY t.date DESC, t.id DESC
        LIMIT 10
    ''').fetchall()
    
    balance = income - expense
    conn.close()
    return render_template('index.html', income=income, expense=expense, balance=balance, 
                         expenses_by_cat=expenses_by_cat, latest_transactions=latest_transactions)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        type_ = request.form['type']
        amount = float(request.form['amount'])
        category_id = int(request.form['category'])
        date_str = request.form['date']
        description = request.form.get('description', '')
        recurrent = request.form.get('recurrent') == 'on'
        frequency = request.form.get('frequency', 'monthly')
        repetitions_str = request.form.get('repetitions', '1')
        try:
            repetitions = int(repetitions_str) if repetitions_str else 1
        except ValueError:
            repetitions = 1

        conn = get_db()
        base_date = datetime.strptime(date_str, '%Y-%m-%d')

        for i in range(repetitions):
            if frequency == 'daily':
                delta = timedelta(days=i)
            elif frequency == 'weekly':
                delta = timedelta(weeks=i)
            elif frequency == 'monthly':
                delta = timedelta(days=i*30)  # approx
            else:
                delta = timedelta(days=i)

            trans_date = base_date + delta
            date_formatted = trans_date.strftime('%Y-%m-%d')

            conn.execute('INSERT INTO transactions (type, amount, category_id, date, description) VALUES (?, ?, ?, ?, ?)',
                         (type_, amount, category_id, date_formatted, description))

        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    conn = get_db()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('add_transaction.html', categories=categories)

@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    conn = get_db()
    conn.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    conn = get_db()
    if request.method == 'POST':
        type_ = request.form['type']
        amount = float(request.form['amount'])
        category_id = int(request.form['category'])
        date_str = request.form['date']
        description = request.form.get('description', '')
        
        conn.execute('UPDATE transactions SET type=?, amount=?, category_id=?, date=?, description=? WHERE id=?',
                     (type_, amount, category_id, date_str, description, transaction_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    
    transaction = conn.execute('''
        SELECT * FROM transactions WHERE id = ?
    ''', (transaction_id,)).fetchone()
    
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    
    if not transaction:
        return redirect(url_for('dashboard'))
    
    return render_template('edit_transaction.html', transaction=transaction, categories=categories)

@app.route('/api/chart_data')
def chart_data():
    month = request.args.get('month')
    conn = get_db()
    if month:
        data = conn.execute('''
            SELECT c.name, SUM(t.amount) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.type='expense' AND strftime('%Y-%m', t.date) = ?
            GROUP BY c.name
        ''', (month,)).fetchall()
    else:
        data = conn.execute('''
            SELECT c.name, SUM(t.amount) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.type='expense'
            GROUP BY c.name
        ''').fetchall()
    conn.close()
    labels = [row['name'] for row in data]
    values = [row['total'] for row in data]
    return jsonify({'labels': labels, 'values': values})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)