# there is a Python file
# https://flask.palletsprojects.com/en/1.1.x/config/
# production app configuration
# SERVER_NAME = '192.168.0.24:5001 nas.local:5001'
SERVER_NAME = 'localhost.home:5001'

HTTPS_ENABLE = False
SERVER_CA = '/home/pi/.ssh/ca.crt'
SERVER_CRT = '/home/pi/.ssh/nasserver.crt'
SERVER_KEY = '/home/pi/.ssh/nasserver.key'

# upload max 1 GB file
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024
JSON_AS_ASCII = True
# MY APP SETTINGS
ALLOWED_EXTENSIONS = {'image': ['jpg', 'jpeg', 'gif', 'png', 'dng'], 'video': ['mp4', 'avi', 'mkv'],
                      'doc': ['txt', 'pdf', 'odt', 'docx', 'doc']}
SAMBA_ROOT_FOLDER_PATH = '/media/nasraid1/shared/public'
