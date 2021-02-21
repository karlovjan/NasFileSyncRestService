# there is a Python file
# default app configuration
ENV = 'development'
DEBUG = True
# SERVER_NAME = '127.0.0.1:5001'
SERVER_NAME = '192.168.0.24:5001'
# upload max 1 GB file
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024
# MY APP SETTINGS
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
SAMBA_ROOT_FOLDER_PATH = '/media/nasraid1/shared/public'
# SAMBA_ROOT_FOLDER_PATH = '/home/mbaros'
# DEBUG = False
# SECRET_KEY =
