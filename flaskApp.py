from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from baseModel import getSize, draw_grid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Shree'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', file_url=None)

@app.route('/', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return redirect(request.url)

    file = request.files['photo']
    size = request.form.get("Size")
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = url_for('uploaded_file', filename=filename)
        print(file_url)
        displayPath = draw_grid()
        return render_template('index.html', file_url=file_url)

    return render_template('index.html', file_url=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
    for file in os.listdir("uploads"):
        os.remove(os.path.join("uploads",file))
