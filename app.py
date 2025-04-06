from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import os
import markdown2
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "changeme")

# Ensure DB exists
if not os.path.exists('database.db'):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    tags TEXT
                )""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<category>')
def show_category(category):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE category=? ORDER BY created_at DESC", (category,))
    posts = c.fetchall()
    conn.close()
    return render_template('category.html', posts=posts, category=category)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = c.fetchone()
    conn.close()
    html_content = markdown2.markdown(post[2])
    return render_template('post.html', post=post, content=html_content)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        tags = request.form['tags']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content, category, created_at, tags) VALUES (?, ?, ?, ?, ?)",
                  (title, content, category, created_at, tags))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new_post.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == os.getenv("BLOG_ADMIN_PASSWORD", "admin"):
            session['logged_in'] = True
            return redirect(url_for('new_post'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
