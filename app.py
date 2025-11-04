from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from passlib.hash import argon2
import os
from crypto.argon2i import hash_password, verify_password

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB_PATH = "database/cmail.db"

# Pastikan folder database ada
os.makedirs("database", exist_ok=True)

# ====== Setup Database ======
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password_hash TEXT,
        profile_pic TEXT DEFAULT 'default.png',
        public_key TEXT,
        private_key TEXT,
        created_at TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        receiver_id INTEGER,
        subject TEXT,
        content_encrypted BLOB,
        status TEXT,
        timestamp TEXT,
        is_read INTEGER DEFAULT 0
    )''')

    conn.commit()
    conn.close()

init_db()
# ============================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# ====== Register ======
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        password_hash = argon2.hash(password)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                           (username, email, password_hash))
            conn.commit()
            flash("Akun berhasil dibuat! Silakan login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username sudah digunakan.", "danger")
        finally:
            conn.close()
    return render_template('register.html')

# ====== Login ======
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and argon2.verify(password, user[1]):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Login gagal. Username atau password salah.", "danger")

    return render_template('login.html')

# ====== Dashboard ======
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/inbox')
def inbox():
    if 'username' not in session:
        return redirect('/login')
    return render_template('inbox.html', username=session['username'])

@app.route('/sent')
def sent():
    if 'username' not in session:
        return redirect('/login')
    return render_template('sent.html', username=session['username'])

@app.route('/draft')
def draft():
    if 'username' not in session:
        return redirect('/login')
    return render_template('draft.html', username=session['username'])

@app.route('/starred')
def starred():
    if 'username' not in session:
        return redirect('/login')
    return render_template('starred.html', username=session['username'])

@app.route('/deleted')
def deleted():
    if 'username' not in session:
        return redirect('/login')
    return render_template('deleted.html', username=session['username'])

@app.route('/compose')
def compose():
    if 'username' not in session:
        return redirect('/login')
    return render_template('compose.html', username=session['username'])

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/login')
    return render_template('profile.html', username=session['username'])


# ====== Logout ======
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
