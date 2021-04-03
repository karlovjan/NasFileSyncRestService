# there is a Python file
# https://flask.palletsprojects.com/en/1.1.x/config/
# default app configuration
ENV = 'development'
DEBUG = True

HTTPS_ENABLE = False
SERVER_CA = 'certs/ca.crt'
SERVER_CRT = 'certs/nasserver.crt'
SERVER_KEY = 'certs/nasserver.key'
# SSL_CONTEXT = ('certs/nasserver.crt', 'certs/nasserver.key', 'certs/ca.crt')
SERVER_NAME = 'localhost.localdomain:5001'
# upload max 1 GB file
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024
JSON_AS_ASCII = True
# MY APP SETTINGS
ALLOWED_EXTENSIONS = {'image': ['jpg', 'jpeg', 'gif', 'png', 'dng'], 'video': ['mp4', 'avi', 'mkv'],
                      'doc': ['txt', 'pdf', 'odt', 'docx', 'doc']}
# SAMBA_ROOT_FOLDER_PATH = '/media/nasraid1/shared/public'
SAMBA_ROOT_FOLDER_PATH = '/home/mbaros'
