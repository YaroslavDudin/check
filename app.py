from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import html

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    # Проверим, есть ли уже admin, если нет - добавим
    cur.execute("SELECT * FROM users WHERE name = ?", ('admin',))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (name) VALUES (?)", ('admin',))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    name = request.args.get('name', '')
    safe_name = html.escape(name)  # предотвращаем Reflected XSS
    return render_template_string(f"""
    <html>
      <head>
        <title>Hello</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 40px; }}
          input, button {{ padding: 8px; margin: 5px 0; width: 300px; }}
          .form-container {{ max-width: 320px; }}
        </style>
      </head>
      <body>
        <h1>Hello, {safe_name}!</h1>
        <div class="form-container">
          <form action="{{{{ url_for('register') }}}}" method="post">
            <label for="username">Register new user:</label><br>
            <input type="text" id="username" name="username" required><br>
            <button type="submit">Register</button>
          </form>
        </div>
      </body>
    </html>
    """)

@app.route('/user')
def user_lookup():
    username = request.args.get('name', '')
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # Используем параметризированный запрос — предотвращаем SQL Injection
    cur.execute("SELECT * FROM users WHERE name = ?", (username,))
    result = cur.fetchall()
    conn.close()
    return {'result': result}

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    if not username:
        return redirect(url_for('index'))
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # Вставка с параметром
    cur.execute("INSERT INTO users (name) VALUES (?)", (username,))
    conn.commit()
    conn.close()
    return redirect(url_for('index', name=username))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
