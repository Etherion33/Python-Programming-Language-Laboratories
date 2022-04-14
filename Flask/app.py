# Importing flask module 

from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask import Flask, session
from flask_session import Session
import sqlite3

# App creation
app = Flask("Flask - Lab")

# Session creation
sess = Session()

def addUser(username,password, isAdmin):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('INSERT INTO USERS(username,password,isAdmin) VALUES(?,?,?)', (username, password,isAdmin))
    con.commit()
    con.close()

def getUser(username: str):
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM USERS WHERE username = '{username}'")
    user = cursor.fetchall()
    con.close()
    print(user)
    if len(user) >= 1:
        return user[0]
    return None

def getBook(title: str):
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM BOOKS WHERE title = '{title}'")
    book = cursor.fetchall()
    con.close()
    print(book)
    if len(book) >= 1:
        return book[0]
    return None
    
def get_everything(table: str):
    sql_con = sqlite3.connect(DATABASE)
    cursor = sql_con.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    sql_con.close()
    return rows


@app.route('/', methods=['GET', 'POST'])
def index():
    books = get_everything("BOOKS")
    # Check if the username is stored in the sesion variable
    if 'username' in session:
        return render_template('mainpage.html', userdata=session['username'], books = books)
    else:
        return render_template('login.html')
    #    return render_template('t4.html', users = users)


@app.route('/login', methods=['POST'])
def login():
    # Create a session for the client and store the username
    username: str = request.form['login']
    passwd = request.form['password']
    print(username)
    user = getUser(username.lower())
    if user is not None:
        password = user[2]
        if password is not None and password == passwd:
            session['username'] = username
            session['admin'] = user[3]
            return index()
    return "<h1>Wrong username/password combination! Try again!</h1>" + render_template("login.html")


@app.route('/logout', methods=['GET'])
def logout():
    # If the user session exists - remove it
    if 'username' in session:
        session.pop('username')
        session['admin'] = False
    return "Logged out <br>  <a href='/'> Main page </a>"

# SqlLite db file path
DATABASE = 'database.db'

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    genre = request.form['genre']
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if getBook(title):
        return f"<h2>Book {title} already exists in the database</h2><br>" + index()
    else:
        cur.execute("INSERT INTO books (title,genre) VALUES (?,?)",(title,genre) )
        con.commit()
        con.close()
        return f"<h2>Book {title} successfully added to the database</h2><br>" + index()

@app.route('/delete_book', methods=['GET'])
def delete_book():
    book = request.args.get('book')
    con = sqlite3.connect(DATABASE)
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM books where ID=?",book)
        con.commit()
    except:
        print("Failed to delete " + str(book))
    finally:
        con.close()
        return index()


@app.route('/create_database', methods=['GET', 'POST'])
def create_db():
    # Db connection
    conn = sqlite3.connect(DATABASE)
    # Create tables with sqlite3
    conn.execute('DROP TABLE IF EXISTS users')
    conn.execute('DROP TABLE IF EXISTS books')
    conn.execute('CREATE TABLE users (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,username TEXT, password TEXT, isAdmin BOOL DEFAULT FALSE)')
    conn.execute('CREATE TABLE books(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,title TEXT, genre TEXT)')

    conn.execute("INSERT INTO users (username, password, isAdmin) VALUES ('admin','admin',TRUE)")
    conn.commit()
    # Terminate the db connection
    conn.close()
    
    return index()


@app.route('/userprofile/<username>')
def userprofile(username):
    if session.keys().__contains__('admin'):
        if session['admin']:
            user = getUser(username)
            print(user)
            return render_template('userprofile.html', user=user)
    return "<h2>You need admin privileges to access this page</h2><br><a href='/'>Main Page</a>"

@app.route('/users')
def users():
    if session.keys().__contains__('admin'):
        if session['admin']:
            all_users = get_everything("USERS")
            return render_template('users.html', users=all_users)
    return "<h2>Admin rights required to visit this page!</h2><br><a href='/'>Main Page</a>"

@app.route('/add_user', methods=['POST'])
def add_user():
    login = request.form['login']
    password = request.form['password']
    isAdmin = True if request.form.get('admin') else False

    if getUser(login):
        return f"<h2>User {login} already exists in the database</h2><br>" + users()
    else:
        addUser(login, password, isAdmin)
        return f"<h2>User {login} successfully added to the database</h2><br>" + users()

# Running the app in debug mode
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)
app.config.from_object(__name__)
app.debug = True
app.run()