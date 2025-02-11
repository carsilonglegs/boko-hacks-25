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
    
    return render_template('adminlogin.html')

@app.route('/register', methods =['GET', 'POST'])

def register():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSER INTO users (username, paswrod) VALUES (?,?)',(username,password))
            conn.commit()
            flash('Registration success! now login.', 'success')
        except:
            flash('Username already exists', 'danger')

        conn.close()
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return f"Welcome, {session['username']}!<br><a href='/logout'>Logout</a>"


