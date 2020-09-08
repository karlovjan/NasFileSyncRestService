import os

from flask import Flask, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024
app.secret_key = "baros753123"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'OK'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # Bad request, 400
            return 'ERROR - file atribut is missing', 400
        f = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if f.filename == '':
            return 'ERROR - file atribut is empty', 400
        if 'dest' not in request.form:
            # Bad request, 400
            return 'ERROR - dest atribut is missing', 400
        dest = request.form['dest']
        if dest == '':
            # Bad request, 400
            return 'ERROR - dest atribut is empty', 400
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(dest, filename))
            return 'OK', 200


if __name__ == '__main__':
    app.run(port=5001, debug=True)
