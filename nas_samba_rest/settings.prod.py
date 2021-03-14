# there is a Python file
# https://flask.palletsprojects.com/en/1.1.x/config/
# production app configuration
# SERVER_NAME = '192.168.0.24:5001 nas.local:5001'
SERVER_NAME = 'smbrest:5443'


SERVER_CA = '/home/pi/.ssh/ca.crt'
SERVER_CRT = '/home/pi/.ssh/nasserver.crt'
SERVER_KEY = '/home/pi/.ssh/nasserver.key'

# upload max 1 GB file
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024
JSON_AS_ASCII = True
# MY APP SETTINGS
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi'}
SAMBA_ROOT_FOLDER_PATH = '/media/nasraid1/shared/public'
SECRET_KEY = b'g~\xf6R\xd6\xa6\x9da\x0f\x9b\xf1\xc2\xba</l'
