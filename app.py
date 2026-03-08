import os
import psycopg2
import psycopg2.extras
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key_blood_donation_app' # Change this in production

def execute_query(query, params=(), commit=False, fetchone=False, fetchall=False):
    db_url = os.environ.get('POSTGRES_URL', os.environ.get('DATABASE_URL'))
    conn = None
    try:
        if db_url:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            query = query.replace('?', '%s')
        else:
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
        cursor.execute(query, params)
        if commit:
            conn.commit()
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
    finally:
        if conn:
            conn.close()

@app.route('/')
def home():
    try:
        camps = execute_query('SELECT * FROM camps ORDER BY date ASC', fetchall=True)
    except Exception as e:
        print(f"Database error: {e}")
        camps = []
    
    return render_template('index.html', camps=camps)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        blood_group = request.form['blood_group']
        last_donation_date = request.form.get('last_donation_date', '')

        if not first_name or not last_name or not email or not password or not blood_group:
            flash('All required fields must be filled!', 'error')
            return redirect(url_for('register'))

        try:
            execute_query('INSERT INTO users (first_name, last_name, email, password_hash, blood_group, last_donation_date) VALUES (?, ?, ?, ?, ?, ?)',
                         (first_name, last_name, email, generate_password_hash(password), blood_group, last_donation_date), commit=True)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            error_str = str(e).lower()
            if 'unique' in error_str or 'duplicate key' in error_str:
                flash('An account with this email already exists.', 'error')
                return redirect(url_for('register'))
            
            print(f"Registration error: {e}")
            flash('An expected database error occurred.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            user = execute_query('SELECT * FROM users WHERE email = ?', (email,), fetchone=True)

            if user is None or not check_password_hash(user['password_hash'], password):
                flash('Invalid email or password.', 'error')
                return redirect(url_for('login'))
            
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Login error: {e}")
            flash('A database error occurred during login.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        user = execute_query('SELECT * FROM users WHERE id = ?', (session['user_id'],), fetchone=True)
        
        if user is None:
            session.clear()
            return redirect(url_for('login'))

        return render_template('dashboard.html', user=user)
    except Exception as e:
        print(f"Dashboard error: {e}")
        session.clear()
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
