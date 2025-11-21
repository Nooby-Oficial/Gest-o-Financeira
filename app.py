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
            'postgresql://postgres.pseyjjtoufvhboqnsnsw:4*a26y%23W.z.Nx+9@aws-0-us-west-2.pooler.supabase.com:6543/postgres')
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
            value_type TEXT,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        # Add value_type column if it doesn't exist (migration)
        c.execute('''
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='expenses' AND column_name='value_type'
                ) THEN
                    ALTER TABLE expenses ADD COLUMN value_type TEXT;
                END IF;
            END $$;
        ''')
        
        # Add paid_date column if it doesn't exist (migration)
        c.execute('''
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='expenses' AND column_name='paid_date'
                ) THEN
                    ALTER TABLE expenses ADD COLUMN paid_date DATE;
                END IF;
            END $$;
        ''')
        
        # Add month column to expenses if it doesn't exist (migration)
        c.execute('''
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='expenses' AND column_name='month'
                ) THEN
                    ALTER TABLE expenses ADD COLUMN month TEXT;
                END IF;
            END $$;
        ''')
        
        # Add year column to expenses if it doesn't exist (migration)
        c.execute('''
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='expenses' AND column_name='year'
                ) THEN
                    ALTER TABLE expenses ADD COLUMN year INTEGER;
                END IF;
            END $$;
        ''')
        
        # Add current_installment column if it doesn't exist (migration)
        c.execute('''
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='expenses' AND column_name='current_installment'
                ) THEN
                    ALTER TABLE expenses ADD COLUMN current_installment INTEGER DEFAULT 1;
                END IF;
            END $$;
        ''')
        
        # Add parent_expense_id for tracking installments (migration)
        c.execute('''
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='expenses' AND column_name='parent_expense_id'
                ) THEN
                    ALTER TABLE expenses ADD COLUMN parent_expense_id INTEGER;
                END IF;
            END $$;
        ''')
        
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
    # Initialize database on first request
    try:
        init_db()
    except:
        pass
    
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
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        except psycopg2.IntegrityError as e:
            print(f"IntegrityError: {e}")
            flash('Email já cadastrado', 'error')
        except Exception as e:
            print(f"Erro ao registrar: {e}")
            flash(f'Erro ao criar conta: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        user_id = session['user_id']
        
        # Get selected month/year from query params or use current
        selected_month = request.args.get('month', datetime.now().strftime('%Y-%m'))
        year, month = selected_month.split('-')
        year = int(year)
        month = int(month)
        
        conn = get_db_connection()
        c = conn.cursor()
        
        # Get incomes for selected month
        c.execute('SELECT * FROM incomes WHERE user_id = %s AND month = %s ORDER BY created_at DESC', 
                 (user_id, selected_month))
        incomes = c.fetchall()
        
        # Get expenses for selected month
        c.execute('''SELECT * FROM expenses 
                     WHERE user_id = %s AND month = %s AND year = %s 
                     ORDER BY due_date DESC''', 
                 (user_id, selected_month, year))
        expenses = c.fetchall()
        
        conn.close()
        
        # Calculate summary
        total_income = sum(float(income['amount']) for income in incomes)
        total_expenses = sum(float(expense['total_amount']) for expense in expenses)
        
        # Calculate monthly expenses (sum of Valor/Mês column)
        total_monthly_expenses = 0
        for expense in expenses:
            if expense.get('value_type') == 'individual':
                # Se for individual, valor mensal é o total_amount
                total_monthly_expenses += float(expense['total_amount'])
            else:
                # Se for total ou None, valor mensal é o installment_value
                total_monthly_expenses += float(expense['installment_value'])
        
        # Calculate weekly expenses
        total_weekly_expenses = 0
        for expense in expenses:
            if expense.get('value_type') == 'individual':
                # Se for individual, valor semanal é o installment_value
                total_weekly_expenses += float(expense['installment_value'])
            else:
                # Se for total ou None, valor semanal é installment_value / 4
                total_weekly_expenses += float(expense['installment_value']) / 4
        
        # Calculate paid expenses percentage
        total_paid_expenses = sum(float(expense['total_amount']) for expense in expenses if expense['status'] == 'paid')
        percentage_paid = (total_paid_expenses / total_expenses * 100) if total_expenses > 0 else 0
        
        balance = total_income - total_expenses
        percentage_used = (total_expenses / total_income * 100) if total_income > 0 else 0
        
        summary = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_monthly_expenses': total_monthly_expenses,
            'total_weekly_expenses': total_weekly_expenses,
            'balance': balance,
            'percentage_used': round(percentage_used, 1),
            'percentage_paid': round(percentage_paid, 1)
        }
        
        return render_template('dashboard.html', 
                             incomes=incomes, 
                             expenses=expenses, 
                             summary=summary,
                             selected_month=selected_month,
                             now=datetime.now())
    except Exception as e:
        print(f"Erro no dashboard: {e}")
        flash(f'Erro ao carregar dashboard: {str(e)}', 'error')
        return redirect(url_for('login'))

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
    amount_input = float(request.form['total_amount'])
    installments = int(request.form['installments'])
    value_type = request.form.get('value_type', 'total') if installments > 1 else 'total'
    category = request.form.get('category', '')
    due_date_str = request.form['due_date']
    
    # Validate value_type is selected when installments > 1
    if installments > 1 and not value_type:
        flash('Selecione o tipo de valor (Total ou Individual)', 'error')
        return redirect(url_for('dashboard'))
    
    # Calculate total and installment values based on type
    if installments > 1 and value_type == 'individual':
        # User entered individual value, multiply by installments
        installment_value = amount_input
        total_amount = amount_input * installments
    else:
        # User entered total value (or single installment), divide by installments
        total_amount = amount_input
        installment_value = amount_input / installments
    
    # Parse due date
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create first expense (parent)
    month_str = due_date.strftime('%Y-%m')
    year = due_date.year
    
    c.execute('''INSERT INTO expenses 
                 (user_id, description, total_amount, installments, installment_value, category, 
                  value_type, due_date, status, month, year, current_installment) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id''',
              (user_id, description, installment_value, 1, installment_value, category, 
               value_type, due_date_str, 'pending', month_str, year, 1))
    
    parent_id = c.fetchone()['id']
    
    # If there are multiple installments, create future expenses
    if installments > 1:
        for i in range(2, installments + 1):
            # Add months manually
            next_month = due_date.month + (i - 1)
            next_year = due_date.year + ((next_month - 1) // 12)
            next_month = ((next_month - 1) % 12) + 1
            next_due_date = due_date.replace(year=next_year, month=next_month)
            next_month_str = next_due_date.strftime('%Y-%m')
            next_year_int = next_due_date.year
            next_due_date_str = next_due_date.strftime('%Y-%m-%d')
            
            c.execute('''INSERT INTO expenses 
                         (user_id, description, total_amount, installments, installment_value, category, 
                          value_type, due_date, status, month, year, current_installment, parent_expense_id) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                      (user_id, description, installment_value, 1, installment_value, category, 
                       value_type, next_due_date_str, 'pending', next_month_str, next_year_int, i, parent_id))
    
    conn.commit()
    conn.close()
    
    flash(f'Despesa adicionada com sucesso! {installments} parcela(s) criada(s).', 'success')
    return redirect(url_for('dashboard'))

@app.route('/edit_expense/<int:expense_id>', methods=['POST'])
@login_required
def edit_expense(expense_id):
    user_id = session['user_id']
    
    description = request.form['description']
    total_amount = float(request.form['total_amount'])
    installments = int(request.form['installments'])
    value_type = request.form.get('value_type', 'total')
    due_date = request.form['due_date']
    category = request.form.get('category', '')
    
    # Calculate installment value
    if installments > 1:
        if value_type == 'individual':
            installment_value = total_amount
            total_amount = total_amount * installments
        else:  # total
            installment_value = total_amount / installments
    else:
        installment_value = total_amount
        value_type = 'total'
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''UPDATE expenses 
                 SET description = %s, total_amount = %s, installments = %s, 
                     installment_value = %s, value_type = %s, due_date = %s, category = %s
                 WHERE id = %s AND user_id = %s''',
              (description, total_amount, installments, installment_value, 
               value_type, due_date, category, expense_id, user_id))
    conn.commit()
    conn.close()
    
    flash('Despesa atualizada com sucesso', 'success')
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
        
        if new_status == 'paid':
            # Registra a data de pagamento
            c.execute('UPDATE expenses SET status = %s, paid_date = CURRENT_DATE WHERE id = %s', 
                     (new_status, expense_id))
        else:
            # Remove a data de pagamento ao voltar para pendente
            c.execute('UPDATE expenses SET status = %s, paid_date = NULL WHERE id = %s', 
                     (new_status, expense_id))
        
        conn.commit()
    
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/duplicate_expense/<int:expense_id>')
@login_required
def duplicate_expense(expense_id):
    user_id = session['user_id']
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get original expense
    c.execute('SELECT * FROM expenses WHERE id = %s AND user_id = %s', (expense_id, user_id))
    original = c.fetchone()
    
    if original:
        # Calculate next month
        original_date = datetime.strptime(original['due_date'], '%Y-%m-%d')
        next_month = original_date.month + 1
        next_year = original_date.year + (next_month // 13)
        next_month = ((next_month - 1) % 12) + 1
        next_date = original_date.replace(year=next_year, month=next_month)
        next_month_str = next_date.strftime('%Y-%m')
        next_due_date_str = next_date.strftime('%Y-%m-%d')
        
        # Create duplicate for next month
        c.execute('''INSERT INTO expenses 
                     (user_id, description, total_amount, installments, installment_value, category, 
                      value_type, due_date, status, month, year, current_installment) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                  (user_id, original['description'], original['total_amount'], 
                   original['installments'], original['installment_value'], original['category'],
                   original.get('value_type', 'total'), next_due_date_str, 'pending', 
                   next_month_str, next_year, original.get('current_installment', 1)))
        
        conn.commit()
        flash(f'Despesa "{original["description"]}" duplicada para {next_month_str}', 'success')
    
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

