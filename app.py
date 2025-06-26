from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

users = ['Ikenna', 'John', 'Ada', 'Zee']  # Add your friends here
media_db = []  # Will hold file info in memory

@app.route('/')
def index():
    return render_template('index.html', users=users, media_db=media_db)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = request.form['username']
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            media_db.append({
                'username': username,
                'filename': filename,
                'likes': 0,
                'comments': []
            })
            return redirect(url_for('index'))
    return render_template('upload.html', users=users)

@app.route('/like/<int:index>', methods=['POST'])
def like(index):
    media_db[index]['likes'] += 1
    return redirect(url_for('index'))

@app.route('/comment/<int:index>', methods=['POST'])
def comment(index):
    comment_text = request.form['comment']
    media_db[index]['comments'].append(comment_text)
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

