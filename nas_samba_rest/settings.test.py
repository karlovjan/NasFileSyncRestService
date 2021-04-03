# there is a Python file
# https://flask.palletsprojects.com/en/1.1.x/config/
# test app configuration
ENV = 'development'
DEBUG = True

HTTPS_ENABLE = False
SERVER_CA = '/home/pi/.ssh/ca.crt'
SERVER_CRT = '/home/pi/.ssh/nasserver.crt'
SERVER_KEY = '/home/pi/.ssh/nasserver.key'
# SERVER_NAME = '192.168.0.24:5001'
# SERVER_NAME = 'nas.local:8443'

SERVER_NAME = 'localhost.home:5001'
# upload max 1 GB file
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024
JSON_AS_ASCII = True
# MY APP SETTINGS
ALLOWED_EXTENSIONS = {'image': ['jpg', 'jpeg', 'gif', 'png', 'dng'], 'video': ['mp4', 'avi', 'mkv'],
                      'doc': ['txt', 'pdf', 'odt', 'docx', 'doc']}
SAMBA_ROOT_FOLDER_PATH = '/media/nasraid1/shared/public'
