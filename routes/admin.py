from flask import Flask, request, redirect,render_template,session, flash
import sqlite3
app = Flask(__name__)
app.secret_key = 'password'

#initialize database

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT  -- Storing passwords in plaintext (very insecure!)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

#vulnerable login 

@app.route('/', methods=['GET','POST'])

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #SQL INJECTION HERE

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query) # inserting user input into SQL 
        user = cursor.fetchone()
        conn.close()

        if user:
            #weak management
            session['username'] = username 
            return redirect('/dashboard')
        else:
            flash('Invalid username or password')
    
    return render_template('login template HERE')