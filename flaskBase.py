import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerField
from baseModel import draw_grid, getSize

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Shreeyanshu'
app.config['UPLOAD_FOLDER'] = 'uploads'
allowed_extensions = {'jpeg', 'jpg', 'png'}

class UploadFileForm(FlaskForm):
    file = FileField('Choose File')
    size = IntegerField('Grid Size', default=100)
    upload_submit = SubmitField('Upload')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()

    if 'image_path' not in session:
        session['image_path'] = None

    if form.validate_on_submit():
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = "upload_img.jpeg"
            file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_save_path)
            session['image_path'] = file_save_path

            display_path = draw_grid(file_save_path, 'static/sample4.jpg', 100)
            size_tuple = getSize(display_path)

            if form.size.data:
                grid_size = int(form.size.data)
                grid_url = draw_grid(session['image_path'], 'static/sample4.jpg', grid_size)
                return render_template('index.html', file_url=session['image_path'], grid_url=grid_url, form=form,
                                       size_display=size_tuple)

            return render_template('index.html', file_url=session['image_path'], grid_url=None, form=form,
                                   size_display=size_tuple)

        else:
            return render_template('index.html', file_url=None, grid_url=None, form=form)

    return render_template('index.html', form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

    for file in os.listdir("uploads"):
        os.remove(os.path.join("uploads", file))

    for file in os.listdir("static"):
        if allowed_file(file):
            os.remove(os.path.join("static", file))
