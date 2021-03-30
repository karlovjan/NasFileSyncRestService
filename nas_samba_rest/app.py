import datetime
import logging
import os
import ssl
from logging import handlers

from flask import Flask, request, jsonify
from flask_cors import cross_origin
from flask_talisman import Talisman
from werkzeug.utils import secure_filename

# https://docs.python.org/3/library/ssl.html

# https://flask-cors.readthedocs.io/en/latest/
# TODO bezpecnost - security, mam povoleny CORS pro vsechny Origins

app = Flask(__name__)
Talisman(app)

# documentation to the configuration https://flask.palletsprojects.com/en/1.1.x/api/#configuration

# before starting the app run in shell a command > export ENV_APP_SETTINGS='/path/to/config/file'
envConfigFile = os.environ['ENV_APP_SETTINGS']

if envConfigFile:
    app.config.from_pyfile(envConfigFile)
else:
    app.config.from_pyfile('settings.py')

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

log = logging.getLogger('Rest_Api_app')
log.setLevel(logging.DEBUG)
log.addHandler(roleFileHandler)
log.addHandler(consoleHandler)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config.get("ALLOWED_EXTENSIONS")


@app.route('/')
def index():
    log.info('test request to the root')
    return 'Api is running...', 200


class FileItem:
    """A file info class"""

    def __init__(self, file_name, last_modified):
        self.name = file_name
        self.mtime = last_modified

    def serialize(self):
        return {
            'name': self.name,
            'mtime': self.mtime
        }


def get_file_items(folder_path):
    items = []
    root_path = app.config["SAMBA_ROOT_FOLDER_PATH"]
    with os.scandir(os.path.join(root_path, folder_path)) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file() and allowed_file(entry.name):
                items.append(FileItem(entry.name, datetime.datetime.fromtimestamp(
                    os.lstat(os.path.join(root_path, folder_path, entry.name)).st_mtime).strftime('%Y-%m-%d %H:%M:%S')))

    return items


# curl -d path=Documents/scripts http://127.0.0.1:5001/folderItems


@app.route('/folderItems', methods=['POST'])
@cross_origin()
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
        # TODO spatna cestina u nazvu souboru, UTF8?
        return jsonify([e.serialize() for e in get_file_items(path)])
        # Enable Access-Control-Allow-Origin
        # response.headers.add("Access-Control-Allow-Origin", "*")
        # return response
    else:
        return jsonify({}), 400


@app.route('/upload', methods=['POST'])
@cross_origin()
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
        if 'mtime' not in request.form:
            # Bad request, 400
            return jsonify(message='ERROR - mtime attribute is missing'), 400
        dest = request.form['dest']
        log.info(f'dest: {dest}')
        mtime = request.form['mtime']
        log.info(f'dest: {mtime} in seconds')
        mtimint = int(mtime)
        if dest == '':
            # Bad request, 400
            return jsonify(message='ERROR - dest attribute is empty'), 400
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config["SAMBA_ROOT_FOLDER_PATH"], dest, filename)
            f.save(filepath)
            os.utime(filepath, mtimint, mtimint)
            return jsonify(message='OK'), 200


context = None

if app.config.get("HTTPS_ENABLE"):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=app.config.get("SERVER_CA"))
    context.verify_mode = ssl.CERT_REQUIRED

    try:
        # context.load_cert_chain(certfile=app.config.get("SERVER_CRT"), keyfile=app.config.get("SERVER_KEY"),
        # password=app.config.get("SERVER_KEY_PSW"))
        context.load_cert_chain(certfile=app.config.get("SERVER_CRT"), keyfile=app.config.get("SERVER_KEY"))
    except Exception as e:
        log.error("Error starting flask server. Missing cert or key. Details: {}", e)


if __name__ == '__main__':
    app.run(ssl_context=context)
