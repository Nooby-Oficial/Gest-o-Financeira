from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database connection
def get_db_connection():
    try:
        database_url = os.environ.get('DATABASE_URL', 
            'postgresql://postgres.pseyjjtoufvhboqnsnsw:4*a26y%23W.z.Nx+9@aws-0-sa-east-1.pooler.supabase.com:6543/postgres')
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor, connect_timeout=10)
        return conn
    except Exception as e:
        print(f"Erro ao conectar banco: {e}")
        raise

# Database initialization
def init_db():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Incomes table
        c.execute('''CREATE TABLE IF NOT EXISTS incomes (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        # Expenses table
        c.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
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
        print("Banco de dados inicializado com sucesso!")
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
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, name FROM users WHERE email = %s AND password = %s', (email, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
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
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id', 
                     (name, email, password))
            user_id = c.fetchone()['id']
            conn.commit()
            conn.close()
            
            session['user_id'] = user_id
            session['user_name'] = name
            return redirect(url_for('dashboard'))
        except psycopg2.IntegrityError:
            flash('Email já cadastrado', 'error')
        except Exception as e:
            flash(f'Erro ao criar conta: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get incomes
    c.execute('SELECT * FROM incomes WHERE user_id = %s ORDER BY month DESC', (user_id,))
    incomes = c.fetchall()
    
    # Get expenses
    c.execute('SELECT * FROM expenses WHERE user_id = %s ORDER BY due_date DESC', (user_id,))
    expenses = c.fetchall()
    
    conn.close()
    
    # Calculate summary
    total_income = sum(float(income['amount']) for income in incomes)
    total_expenses = sum(float(expense['installment_value']) for expense in expenses)
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
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO incomes (user_id, description, amount, month) VALUES (%s, %s, %s, %s)',
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
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO expenses 
                 (user_id, description, total_amount, installments, installment_value, category, due_date, status) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
              (user_id, description, total_amount, installments, installment_value, category, due_date, 'pending'))
    conn.commit()
    conn.close()
    
    flash('Despesa adicionada com sucesso', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_expense/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    user_id = session['user_id']
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = %s AND user_id = %s', (expense_id, user_id))
    conn.commit()
    conn.close()
    
    flash('Despesa excluída com sucesso', 'success')
    return redirect(url_for('dashboard'))

@app.route('/toggle_status/<int:expense_id>')
@login_required
def toggle_status(expense_id):
    user_id = session['user_id']
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT status FROM expenses WHERE id = %s AND user_id = %s', (expense_id, user_id))
    expense = c.fetchone()
    
    if expense:
        new_status = 'paid' if expense['status'] == 'pending' else 'pending'
        c.execute('UPDATE expenses SET status = %s WHERE id = %s', (new_status, expense_id))
        conn.commit()
    
    conn.close()
    return redirect(url_for('dashboard'))

# Initialize database
try:
    init_db()
except Exception as e:
    print(f"Aviso: Banco não inicializado: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
