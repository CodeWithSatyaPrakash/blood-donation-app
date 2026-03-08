import os
import sqlite3
import psycopg2
from werkzeug.security import generate_password_hash

def init_db():
    db_url = os.environ.get('POSTGRES_URL', os.environ.get('DATABASE_URL'))
    conn = None
    
    try:
        if db_url:
            print("Connecting to Cloud PostgreSQL...")
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    blood_group TEXT NOT NULL,
                    last_donation_date TEXT
                )
            ''')
            
            cursor.execute('DROP TABLE IF EXISTS camps')
            cursor.execute('''
                CREATE TABLE camps (
                    id SERIAL PRIMARY KEY,
                    camp_name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            
            users = [
                ('John', 'Doe', 'john@example.com', generate_password_hash('password123'), 'O+', '2023-10-15'),
                ('Jane', 'Smith', 'jane@example.com', generate_password_hash('password123'), 'A-', '2024-01-20'),
                ('Alice', 'Johnson', 'alice@example.com', generate_password_hash('password123'), 'B+', '2023-11-05')
            ]
            cursor.executemany('''
                INSERT INTO users (first_name, last_name, email, password_hash, blood_group, last_donation_date) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                ON CONFLICT (email) DO NOTHING
            ''', users)
            
            camps = [
                ('City General Hospital Camp', '123 Main St, Downtown', '2024-05-15'),
                ('Community Center Drive', '456 Oak St, Suburbs', '2024-06-10'),
                ('University Blood Drive', 'Student Union Building', '2024-04-22')
            ]
            cursor.executemany('INSERT INTO camps (camp_name, location, date) VALUES (%s, %s, %s)', camps)
            print("Cloud Database initialized and seeded.")

        else:
            print("Connecting to Local SQLite...")
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    blood_group TEXT NOT NULL,
                    last_donation_date TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS camps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    camp_name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            
            users = [
                ('John', 'Doe', 'john@example.com', generate_password_hash('password123'), 'O+', '2023-10-15'),
                ('Jane', 'Smith', 'jane@example.com', generate_password_hash('password123'), 'A-', ''),
                ('Alice', 'Johnson', 'alice@example.com', generate_password_hash('password123'), 'B+', '2023-11-05')
            ]
            cursor.executemany('INSERT OR IGNORE INTO users (first_name, last_name, email, password_hash, blood_group, last_donation_date) VALUES (?, ?, ?, ?, ?, ?)', users)
            
            camps = [
                ('City General Hospital Camp', '123 Main St, Downtown', '2025-05-15'),
                ('Community Center Drive', '456 Oak St, Suburbs', '2025-06-10'),
                ('University Blood Drive', 'Student Union Building', '2025-04-22')
            ]
            # Delete old camps to re-seed 2025 camps
            cursor.execute('DELETE FROM camps')
            cursor.executemany('INSERT INTO camps (camp_name, location, date) VALUES (?, ?, ?)', camps)
            print("Local SQLite initialized and seeded.")

        conn.commit()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db()
