from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import hashlib
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database path - use /tmp in serverless
DB_PATH = '/tmp/financeiro.db' if os.path.exists('/tmp') else 'financeiro.db'

# Database initialization
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Incomes table
        c.execute('''CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        # Expenses table
        c.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            total_amount REAL NOT NULL,
            installments INTEGER NOT NULL DEFAULT 1,
            installment_value REAL NOT NULL,
            category TEXT,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, name FROM users WHERE email = ? AND password = ?', (email, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha inválidos', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            conn.commit()
            
            # Get user id
            c.execute('SELECT id FROM users WHERE email = ?', (email,))
            user = c.fetchone()
            conn.close()
            
            session['user_id'] = user[0]
            session['user_name'] = name
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            flash('Email já cadastrado', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get incomes
    c.execute('SELECT * FROM incomes WHERE user_id = ? ORDER BY month DESC', (user_id,))
    incomes = c.fetchall()
    
    # Get expenses
    c.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY due_date DESC', (user_id,))
    expenses = c.fetchall()
    
    conn.close()
    
    # Calculate summary
    total_income = sum(income[3] for income in incomes)
    total_expenses = sum(expense[5] for expense in expenses)
    balance = total_income - total_expenses
    percentage_used = (total_expenses / total_income * 100) if total_income > 0 else 0
    
    summary = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'percentage_used': round(percentage_used, 1)
    }
    
    return render_template('dashboard.html', 
                         incomes=incomes, 
                         expenses=expenses, 
                         summary=summary)

@app.route('/add_income', methods=['POST'])
@login_required
def add_income():
    user_id = session['user_id']
    description = request.form['description']
    amount = float(request.form['amount'])
    month = request.form['month']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO incomes (user_id, description, amount, month) VALUES (?, ?, ?, ?)',
              (user_id, description, amount, month))
    conn.commit()
    conn.close()
    
    flash('Receita adicionada com sucesso', 'success')
    return redirect(url_for('dashboard'))

@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    user_id = session['user_id']
    description = request.form['description']
    total_amount = float(request.form['total_amount'])
    installments = int(request.form['installments'])
    installment_value = total_amount / installments
    category = request.form.get('category', '')
    due_date = request.form['due_date']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO expenses 
                 (user_id, description, total_amount, installments, installment_value, category, due_date, status) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (user_id, description, total_amount, installments, installment_value, category, due_date, 'pending'))
    conn.commit()
    conn.close()
    
    flash('Despesa adicionada com sucesso', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_expense/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
    conn.commit()
    conn.close()
    
    flash('Despesa excluída com sucesso', 'success')
    return redirect(url_for('dashboard'))

@app.route('/toggle_status/<int:expense_id>')
@login_required
def toggle_status(expense_id):
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT status FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
    expense = c.fetchone()
    
    if expense:
        new_status = 'paid' if expense[0] == 'pending' else 'pending'
        c.execute('UPDATE expenses SET status = ? WHERE id = ?', (new_status, expense_id))
        conn.commit()
    
    conn.close()
    return redirect(url_for('dashboard'))

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
