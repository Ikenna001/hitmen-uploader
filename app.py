from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('data', exist_ok=True)

# DB Setup
def init_db():
    with sqlite3.connect('data/database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            filename TEXT,
            likes INTEGER DEFAULT 0,
            comments TEXT DEFAULT ""
        )''')
        conn.commit()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('data/database.db')
    uploads = conn.execute('SELECT * FROM uploads ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', uploads=uploads)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = request.form['username']
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            conn = sqlite3.connect('data/database.db')
            conn.execute('INSERT INTO uploads (username, filename) VALUES (?, ?)', (username, filename))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/like/<int:upload_id>')
def like(upload_id):
    conn = sqlite3.connect('data/database.db')
    conn.execute('UPDATE uploads SET likes = likes + 1 WHERE id = ?', (upload_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/comment/<int:upload_id>', methods=['POST'])
def comment(upload_id):
    comment = request.form['comment']
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('SELECT comments FROM uploads WHERE id = ?', (upload_id,))
    old_comments = c.fetchone()[0] or ""
    new_comments = old_comments + f"\n- {comment}"
    c.execute('UPDATE uploads SET comments = ? WHERE id = ?', (new_comments, upload_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
