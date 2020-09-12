import logging
import os
from logging import handlers

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('ENV_APP_SETTINGS')

log = logging.getLogger('Rest_Api_app')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                              datefmt='%Y-%m-%d %H:%M:%S')

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(formatter)

roleFileHandler = handlers.TimedRotatingFileHandler('logs/app.log',
                                                    encoding='utf8',
                                                    when='midnight',
                                                    interval=1,
                                                    backupCount=20)
roleFileHandler.setLevel(logging.INFO)
roleFileHandler.setFormatter(formatter)

log.addHandler(roleFileHandler)
log.addHandler(consoleHandler)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    log.debug('test debug')
    log.warning('test warn')
    return 'Api is running...', 200


def get_file_items(folder_path):
    items = []
    with os.scandir(folder_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                from filesync.file_item import FileItem
                items.append(FileItem(entry.name, os.lstat(os.path.join(folder_path, entry.name)).st_mtime))

    return items


# curl -d path=/home/mbaros/Documents/scripts http://127.0.0.1:5001/folderItems


@app.route('/folderItems', methods=['POST'])
def get_folder_items():
    if request.method == 'POST':
        if 'path' not in request.form:
            # Bad request, 400
            return jsonify(message='ERROR - path attribute is missing'), 400
        path = request.form['path']
        log.info(f'path: {path}')
        if path == '':
            # Bad request, 400
            return jsonify(message='ERROR - dest attribute is empty'), 400
        return jsonify([e.serialize() for e in get_file_items(path)])
    else:
        return jsonify({}), 400


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # Bad request, 400
            return jsonify(message='ERROR - file attribute is missing'), 400
        f = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        log.info(f'file name: {f.filename}')
        if f.filename == '':
            return jsonify(message='ERROR - file attribute is empty'), 400
        if 'dest' not in request.form:
            # Bad request, 400
            return jsonify(message='ERROR - dest attribute is missing'), 400
        dest = request.form['dest']
        log.info(f'dest: {dest}')
        if dest == '':
            # Bad request, 400
            return jsonify(message='ERROR - dest attribute is empty'), 400
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(dest, filename))
            return jsonify(message='OK'), 200


if __name__ == '__main__':
    app.run()
