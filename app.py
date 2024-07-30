# app.py
# setup_database.py

import sqlite3

def create_database():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Create table with specified columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        employee_id TEXT NOT NULL,
        contact_no TEXT NOT NULL,
        location TEXT NOT NULL CHECK (location IN ('offshore', 'onshore'))
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()




from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Database function to handle connections
def get_db_connection():
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def index():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

# Admin login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':  # Use your own auth mechanism
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid Credentials. Please try again.')
    return render_template('login.html')

# Admin route
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        employee_id = request.form['employee_id']
        contact_no = request.form['contact_no']
        location = request.form['location']
        conn.execute('INSERT INTO employees (name, employee_id, contact_no, location) VALUES (?, ?, ?, ?)',
                     (name, employee_id, contact_no, location))
        conn.commit()
        flash('Employee added successfully!')
        return redirect(url_for('admin'))

    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('admin.html', employees=employees)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Employee deleted successfully!')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
