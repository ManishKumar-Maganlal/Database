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
        associateid TEXT NOT NULL,
        associatename TEXT NOT NULL,
        departmentdescription TEXT NOT NULL,
        finalmisdepartment TEXT NOT NULL,
        practicename TEXT NOT NULL,
        projectid TEXT NOT NULL,
        projectname TEXT NOT NULL,
        location TEXT NOT NULL,
        region TEXT NOT NULL,
        country TEXT NOT NULL,
        city TEXT NOT NULL,
        citydescription TEXT NOT NULL,
        emailid TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()




from flask import Flask, render_template, request, redirect, url_for, flash, session


app = Flask(__name__)
app.secret_key = '12345'  # Replace with a strong secret key
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
        associateid = request.form['associateid']
        associatename = request.form['associatename']
        departmentdescription = request.form['departmentdescription']
        finalmisdepartment = request.form['finalmisdepartment']
        practicename = request.form['practicename']
        projectid = request.form['projectid']
        projectname = request.form['projectname']
        location = request.form['location']
        region = request.form['region']
        country = request.form['country']
        city = request.form['city']
        citydescription = request.form['citydescription']
        emailid = request.form['emailid']
        try:
            conn.execute('INSERT INTO employees (associateid,associatename,departmentdescription,finalmisdepartment,practicename,projectid,projectname,location,region,country,city,citydescription,emailid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (associateid, associatename, departmentdescription, finalmisdepartment, practicename, projectid, projectname, location, region, country, city, citydescription, emailid))
            conn.commit()
            flash('Employee added successfully!')
        except Exception as e:
            flash('Error adding employee: {}'.format(e))
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
