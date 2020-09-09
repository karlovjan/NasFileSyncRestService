import os

from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('ENV_APP_SETTINGS')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'OK'


test_items = [
    {
        'name': '1',
        'modified': datetime.now()
    },
    {
        'name': '2',
        'modified': datetime(2020, 9, 1, 16, 29, 43, 79043)
    }
]

# curl -d path=install http://127.0.0.1:5001/folderItems


@app.route('/folderItems', methods=['POST'])
def get_folder_items():
    if request.method == 'POST':
        if 'path' not in request.form:
            # Bad request, 400
            return jsonify({'error': 'ERROR - path attribut is missing'}), 400
        path = request.form['path']
        if path == '':
            # Bad request, 400
            return jsonify({'error': 'ERROR - dest attribut is empty'}), 400
        return jsonify({'items': test_items})
    else:
        return jsonify({}), 400


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # Bad request, 400
            return 'ERROR - file attribut is missing', 400
        f = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if f.filename == '':
            return 'ERROR - file attribut is empty', 400
        if 'dest' not in request.form:
            # Bad request, 400
            return 'ERROR - dest attribut is missing', 400
        dest = request.form['dest']
        if dest == '':
            # Bad request, 400
            return 'ERROR - dest attribut is empty', 400
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(dest, filename))
            return 'OK', 200


if __name__ == '__main__':
    app.run()
